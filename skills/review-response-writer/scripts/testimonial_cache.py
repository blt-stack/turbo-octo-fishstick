"""
Writer for the shared testimonial cache.

Skill #10 (Review Response Writer) is the primary writer; downstream skills
(Landing Page Copywriter, A+ Content Creator, Ad Creative Generator) read from
this cache.

Path convention:
    <plugin-root>/.cache/testimonials/{product-identifier}.json

Schema:
    {
      "product_identifier": "river-stone-pour-over",
      "product_name": "River Stone Pour-Over",
      "last_updated": "2026-05-22T16:30:00Z",
      "testimonials": [
        {
          "quote": "Hearing that the grip feels balanced from the first pour is exactly what we hoped for.",
          "reviewer_first_name": "Sam",
          "reviewer_last_initial": "K",
          "reviewer_full_attribution": "Sam K., verified purchase, Brooklyn NY",
          "platform_source": "judge_me",
          "platform_review_id": "...",
          "star_rating": 5,
          "review_date": "2026-05-10",
          "quote_score": 87,
          "specificity_tags": ["feature", "feeling"],
          "use_cases": ["landing_page_testimonial", "amazon_a_plus_module", "ad_creative_testimonial"],
          "do_not_amplify": false,
          "consent_note": "Standard public-review usage",
          "added_at": "2026-05-22T16:30:00Z",
          "added_by": "review-response-writer"
        },
        ...
      ]
    }

Usage:
    from testimonial_cache import save_testimonials, load_testimonials, top_testimonials

    save_testimonials("river-stone-pour-over", "River Stone Pour-Over", quotes)
    payload = load_testimonials("river-stone-pour-over")
    top = top_testimonials(payload, n=10, use_case="landing_page_testimonial")
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CACHE_SUBDIR = ".cache/testimonials"


def find_plugin_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / "plugin.json").exists():
            return parent
    raise FileNotFoundError(
        f"Could not locate plugin root walking up from {here}."
    )


def cache_dir() -> Path:
    return find_plugin_root() / CACHE_SUBDIR


def slugify(text: str, max_len: int = 80) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled-product"


def cache_path_for(product_identifier: str) -> Path:
    return cache_dir() / f"{product_identifier}.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _empty_payload(product_identifier: str, product_name: str) -> dict:
    return {
        "product_identifier": product_identifier,
        "product_name": product_name,
        "last_updated": _now_iso(),
        "testimonials": [],
    }


def load_testimonials(product_identifier: str) -> dict | None:
    path = cache_path_for(product_identifier)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[testimonial_cache] Failed to load {path}: {exc}", file=sys.stderr)
        return None


def find_testimonials_for_product(
    shopify_handle: str | None = None,
    amazon_asin: str | None = None,
    product_name: str | None = None,
) -> dict | None:
    candidates: list[str] = []
    if shopify_handle and shopify_handle.strip():
        candidates.append(slugify(shopify_handle))
    if amazon_asin and amazon_asin.strip():
        candidates.append(amazon_asin.strip().upper())
    if product_name and product_name.strip():
        candidates.append(slugify(product_name))
    for ident in candidates:
        payload = load_testimonials(ident)
        if payload:
            return payload
    return None


def _quote_already_cached(existing: list[dict], new_quote: dict) -> bool:
    """Dedupe by (platform_review_id, quote text)."""
    new_id = new_quote.get("platform_review_id")
    new_text = (new_quote.get("quote") or "").strip().lower()
    for e in existing:
        if new_id and e.get("platform_review_id") == new_id and (e.get("quote") or "").strip().lower() == new_text:
            return True
    return False


def save_testimonials(
    product_identifier: str,
    product_name: str,
    new_testimonials: list[dict],
    merge: bool = True,
) -> Path:
    """
    Save testimonials to the cache. Default merges into existing entries.
    Each new entry gets `added_at` and `added_by` auto-stamped if absent.
    """
    path = cache_path_for(product_identifier)
    path.parent.mkdir(parents=True, exist_ok=True)

    if merge and path.exists():
        existing = load_testimonials(product_identifier) or _empty_payload(product_identifier, product_name)
    else:
        existing = _empty_payload(product_identifier, product_name)

    existing["product_identifier"] = product_identifier
    existing["product_name"] = product_name or existing.get("product_name", "")
    existing["last_updated"] = _now_iso()

    existing.setdefault("testimonials", [])
    for t in (new_testimonials or []):
        t_copy = dict(t)
        t_copy.setdefault("added_at", _now_iso())
        t_copy.setdefault("added_by", "review-response-writer")
        t_copy.setdefault("do_not_amplify", False)
        t_copy.setdefault("use_cases", ["landing_page_testimonial"])
        if not _quote_already_cached(existing["testimonials"], t_copy):
            existing["testimonials"].append(t_copy)

    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def top_testimonials(payload: dict, n: int = 20, use_case: str | None = None) -> list[dict]:
    """Return top-N testimonials by score, optionally filtered to a use case."""
    if not payload:
        return []
    items = [t for t in payload.get("testimonials", []) if not t.get("do_not_amplify")]
    if use_case:
        items = [t for t in items if use_case in (t.get("use_cases", []) or [])]
    items.sort(key=lambda t: t.get("quote_score", 0), reverse=True)
    return items[:n]


def list_cached() -> list[str]:
    d = cache_dir()
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.json"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        cached = list_cached()
        if not cached:
            print("No testimonial artifacts cached yet.")
            print(f"Cache dir: {cache_dir()}")
        else:
            print(f"{len(cached)} cached testimonial artifact(s):")
            for c in cached:
                print(f"  - {c}")
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: testimonial_cache.py show <product_identifier>")
            sys.exit(1)
        payload = load_testimonials(sys.argv[2])
        if not payload:
            print(f"No testimonials for '{sys.argv[2]}'")
            sys.exit(1)
        print(json.dumps(payload, indent=2))
    elif cmd == "top":
        if len(sys.argv) < 3:
            print("Usage: testimonial_cache.py top <product_identifier> [use_case]")
            sys.exit(1)
        payload = load_testimonials(sys.argv[2])
        if not payload:
            print(f"No testimonials for '{sys.argv[2]}'")
            sys.exit(1)
        use_case = sys.argv[3] if len(sys.argv) >= 4 else None
        for t in top_testimonials(payload, n=10, use_case=use_case):
            attr = t.get("reviewer_full_attribution") or t.get("reviewer_first_name", "?")
            print(f"  [{t.get('quote_score', '?'):>2}] \"{t.get('quote', '')}\" — {attr}")
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: testimonial_cache.py [list | show <id> | top <id> [use_case]]")
        sys.exit(1)
