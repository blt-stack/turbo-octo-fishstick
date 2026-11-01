"""
Write the keywords.json artifact that the Product Description Writer skill picks up.

Path convention:
    <plugin-root>/.cache/keywords/{product-identifier}.json

Where product-identifier is, in priority order:
    1. Shopify product handle (preferred — stable + human-readable)
    2. Amazon ASIN
    3. slugified product name (fallback)

This file is shared infrastructure between skills. Don't change the schema
without coordinating with the Product Description Writer's pickup logic.

Usage:
    from keyword_artifact_writer import write_keywords_artifact, slugify

    path = write_keywords_artifact(
        product_identifier="river-stone-pour-over",
        product_name="River Stone Pour-Over",
        voice_profile_version="v2026-05-21",
        keywords_ranked=[...],
        platforms_optimized=["shopify", "amazon", "etsy"],
    )
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CACHE_SUBDIR = ".cache/keywords"


def find_plugin_root(start: Path | None = None) -> Path:
    """Walk up from this script until we find a directory containing .claude-plugin/plugin.json."""
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".claude-plugin" / "plugin.json").exists():
            return parent
    raise FileNotFoundError(
        "Could not locate plugin root (no .claude-plugin/plugin.json found walking up from "
        f"{here}). The keyword artifact writer needs to live inside the plugin tree."
    )


def keyword_cache_dir() -> Path:
    return find_plugin_root() / CACHE_SUBDIR


def slugify(text: str, max_len: int = 80) -> str:
    """Make a filesystem-safe identifier from a free-text product name."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled-product"


def resolve_product_identifier(
    shopify_handle: str | None = None,
    amazon_asin: str | None = None,
    product_name: str | None = None,
) -> str:
    """Apply the priority order for picking the artifact filename."""
    if shopify_handle and shopify_handle.strip():
        return slugify(shopify_handle)
    if amazon_asin and amazon_asin.strip():
        return amazon_asin.strip().upper()
    if product_name and product_name.strip():
        return slugify(product_name)
    raise ValueError("Need at least one of: shopify_handle, amazon_asin, product_name")


def write_keywords_artifact(
    product_identifier: str,
    product_name: str,
    voice_profile_version: str,
    keywords_ranked: list[dict],
    platforms_optimized: list[str],
    extra: dict | None = None,
) -> Path:
    """
    Write the artifact and return its path. Will create the cache directory
    if it doesn't exist. Overwrites any existing artifact at the same path
    (refreshing keywords is the expected behavior).
    """
    cache_dir = keyword_cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "product_identifier": product_identifier,
        "product_name": product_name,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "voice_profile_version": voice_profile_version,
        "keywords_ranked": keywords_ranked,
        "platforms_optimized": platforms_optimized,
    }
    if extra:
        payload.update(extra)

    path = cache_dir / f"{product_identifier}.json"
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def read_keywords_artifact(product_identifier: str) -> dict | None:
    """Read an existing artifact. Returns None if missing."""
    path = keyword_cache_dir() / f"{product_identifier}.json"
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def list_cached_products() -> list[str]:
    """List all product_identifiers with a cached keywords.json."""
    cache_dir = keyword_cache_dir()
    if not cache_dir.exists():
        return []
    return sorted(p.stem for p in cache_dir.glob("*.json"))


if __name__ == "__main__":
    # CLI: python keyword_artifact_writer.py list | show <id> | path
    cmd = sys.argv[1] if len(sys.argv) > 1 else "path"
    if cmd == "list":
        cached = list_cached_products()
        if not cached:
            print("No keyword artifacts cached yet.")
        else:
            print(f"{len(cached)} cached keyword artifact(s):")
            for c in cached:
                print(f"  - {c}")
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: keyword_artifact_writer.py show <product_identifier>")
            sys.exit(1)
        artifact = read_keywords_artifact(sys.argv[2])
        if artifact is None:
            print(f"No artifact found for '{sys.argv[2]}'")
            sys.exit(1)
        print(json.dumps(artifact, indent=2))
    else:
        print(f"Cache directory: {keyword_cache_dir()}")
