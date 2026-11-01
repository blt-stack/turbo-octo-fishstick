"""
Orchestration helpers for bulk-mode product description runs.

This file is intentionally lightweight — the actual copy generation is done by
the LLM driving the skill, not by code. What lives here is the deterministic
plumbing:

  - Parse a buyer-supplied CSV into a list of product dicts
  - Chunk a large product list into batches for parallel generation
  - Validate character limits after generation
  - Roll generated copy into the bulk-output JSON shape that
    render_bulk_xlsx.py expects

Usage from another script:
    from bulk_processor import (
        parse_csv_products,
        chunk_for_batching,
        validate_lengths,
        assemble_bulk_payload,
    )

Or as a CLI:
    python bulk_processor.py parse <csv_path>
    python bulk_processor.py validate <bulk_json_path>
"""

import csv
import json
import sys
from pathlib import Path
from typing import Iterable


DEFAULT_BATCH_SIZE = 10


# Limits used during validation — keep aligned with the platform format guides
# in templates/. Any field not listed here is treated as unbounded.
FIELD_LIMITS: dict[str, dict[str, int]] = {
    "shopify": {"meta_description": 160},
    "amazon": {"title": 200, "description": 2000, "search_terms": 250},
    "etsy": {"title": 140},
    "ebay": {"title": 80},
    "walmart": {"title": 200},
    "tiktok_shop": {"title": 34, "description": 800},
}


def parse_csv_products(csv_path: Path) -> list[dict]:
    """
    Parse a CSV of products. Expected columns (case-insensitive, any order):
      product_name (required)
      sku, description, materials, dimensions, price, category, image_urls,
      keywords, notes, source

    Any column not in this list is preserved under product["extra"][col].
    """
    known = {
        "product_name",
        "sku",
        "description",
        "materials",
        "dimensions",
        "price",
        "category",
        "image_urls",
        "keywords",
        "notes",
        "source",
    }
    products: list[dict] = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
            if not normalized.get("product_name"):
                continue  # skip rows without a name
            product = {k: normalized[k] for k in known if k in normalized}
            extras = {k: v for k, v in normalized.items() if k not in known}
            if extras:
                product["extra"] = extras
            # Split listy fields
            if product.get("image_urls"):
                product["image_urls"] = [u.strip() for u in product["image_urls"].split("|") if u.strip()]
            if product.get("keywords"):
                product["keywords"] = [k.strip() for k in product["keywords"].split(",") if k.strip()]
            products.append(product)
    return products


def chunk_for_batching(products: list[dict], batch_size: int = DEFAULT_BATCH_SIZE) -> Iterable[list[dict]]:
    """Yield batches so the caller can dispatch parallel subagents."""
    for i in range(0, len(products), batch_size):
        yield products[i : i + batch_size]


def validate_lengths(bulk_payload: dict) -> list[dict]:
    """
    Walk the bulk payload and return a list of issues:
      [{"product_name": "...", "platform": "amazon", "variant": "v1",
        "field": "title", "length": 213, "limit": 200}]
    Empty list means everything is within limits.
    """
    issues = []
    for product in bulk_payload.get("products", []):
        name = product.get("product_name", "?")
        for platform, variants in product.get("platforms", {}).items():
            field_limits = FIELD_LIMITS.get(platform, {})
            for variant_key, variant in variants.items():
                for field, limit in field_limits.items():
                    value = str(variant.get(field, "") or "")
                    if len(value) > limit:
                        issues.append(
                            {
                                "product_name": name,
                                "platform": platform,
                                "variant": variant_key,
                                "field": field,
                                "length": len(value),
                                "limit": limit,
                            }
                        )
    return issues


def assemble_bulk_payload(
    store_name: str,
    generated_at: str,
    products: list[dict],
    voice_profile_version: str,
) -> dict:
    """
    Build the bulk-output JSON expected by render_bulk_xlsx.py.
    Each product in `products` should already have a `platforms` dict
    populated by the LLM generation step.
    """
    enriched = []
    for product in products:
        enriched.append(
            {
                "product_name": product.get("product_name", ""),
                "sku": product.get("sku", ""),
                "source": product.get("source", "Pasted"),
                "voice_profile_version": voice_profile_version,
                "keywords_used": product.get("keywords", []),
                "notes": product.get("notes", ""),
                "generated_at": generated_at,
                "platforms": product.get("platforms", {}),
            }
        )
    return {
        "store_name": store_name,
        "generated_at": generated_at,
        "products": enriched,
    }


def _cli_parse(csv_path: str):
    products = parse_csv_products(Path(csv_path))
    print(json.dumps(products, indent=2))


def _cli_validate(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    issues = validate_lengths(data)
    if not issues:
        print("All fields within limits.")
    else:
        print(f"Found {len(issues)} length issue(s):")
        for issue in issues:
            print(
                f"  - {issue['product_name']} | {issue['platform']} {issue['variant']} "
                f"| {issue['field']}: {issue['length']}/{issue['limit']}"
            )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python bulk_processor.py parse <csv_path>")
        print("  python bulk_processor.py validate <bulk_json_path>")
        sys.exit(1)
    cmd, arg = sys.argv[1], sys.argv[2]
    if cmd == "parse":
        _cli_parse(arg)
    elif cmd == "validate":
        _cli_validate(arg)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
