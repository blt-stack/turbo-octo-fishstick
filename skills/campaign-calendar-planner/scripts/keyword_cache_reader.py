"""
Read the shared keywords.json cache written by the Listing SEO Optimizer (skill #2).

The Landing Page Copywriter calls this on every run. If a fresh keywords artifact
exists for the product being optimized, the keywords are woven into the hero,
value props, and FAQ blocks for organic SEO lift without compromising
conversion.

Path convention (must match keyword_artifact_writer.py in skill #2):
    ~/.the-ecommerce-seller/cache/keywords/{product-identifier}.json

Usage from another script:
    from keyword_cache_reader import (
        find_keywords_for_product,
        load_keywords_artifact,
        top_keywords,
        is_artifact_fresh,
    )

    artifact = find_keywords_for_product(
        shopify_handle="river-stone-pour-over",
        amazon_asin=None,
        product_name="River Stone Pour-Over",
    )
    if artifact:
        kws = top_keywords(artifact, n=10)
        # use kws in the page draft

CLI:
    python keyword_cache_reader.py list
    python keyword_cache_reader.py show <product_identifier>
    python keyword_cache_reader.py find <shopify_handle_or_product_name>
"""

import os
import shutil
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CACHE_SUBDIR = "cache/keywords"


def find_plugin_root(start: Path | None = None) -> Path:
    """Walk up from this script until we find a directory containing .claude-plugin/plugin.json."""
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".claude-plugin" / "plugin.json").exists():
            return parent
    raise FileNotFoundError(
        "Could not locate plugin root (no .claude-plugin/plugin.json found walking up from "
        f"{here}). The keyword cache reader needs to live inside the plugin tree."
    )

# --- Permanent data folder (shared by every script in this plugin) ---------
# Config and caches live outside the plugin folder: plugin updates install
# into a new version folder, which would otherwise reset setup and wipe
# everything the skills have learned. Override with THE_ECOMMERCE_SELLER_DATA.

DATA_DIR_ENV = "THE_ECOMMERCE_SELLER_DATA"
DEFAULT_DATA_DIR = Path.home() / ".the-ecommerce-seller"
PLUGIN_NAME = "the-ecommerce-seller"
_LEGACY_DIRS = ((".config", "config"), (".cache", "cache"))


def data_root() -> Path:
    """Return the permanent data folder, copying in data from older
    in-plugin locations the first time it is used."""
    override = os.environ.get(DATA_DIR_ENV, "").strip()
    root = Path(override).expanduser() if override else DEFAULT_DATA_DIR
    if not root.exists():
        _migrate_legacy_data(root)
    return root


def _migrate_legacy_data(root: Path) -> None:
    """Copy .config/ and .cache/ from the plugin folder (or, for a versioned
    install, the most recently used sibling version) into root. Copies only,
    so the old folders stay as a backup."""
    try:
        plugin_root = find_plugin_root()
    except FileNotFoundError:
        return
    candidates = [plugin_root]
    if plugin_root.parent.name == PLUGIN_NAME:  # .../<plugin>/<version>/
        candidates += [p for p in plugin_root.parent.iterdir() if p.is_dir() and p != plugin_root]

    def last_used(folder: Path) -> float:
        times = [f.stat().st_mtime for old, _ in _LEGACY_DIRS if (folder / old).is_dir()
                 for f in (folder / old).rglob("*") if f.is_file()]
        return max(times, default=-1.0)

    used = [(last_used(c), c) for c in candidates]
    used = [u for u in used if u[0] >= 0]
    if not used:
        return
    source = max(used)[1]
    for old, new in _LEGACY_DIRS:
        if (source / old).is_dir():
            shutil.copytree(source / old, root / new, dirs_exist_ok=True)
            print(f"[{PLUGIN_NAME}] Copied {source / old} -> {root / new}", file=sys.stderr)


def keyword_cache_dir() -> Path:
    return data_root() / CACHE_SUBDIR


def slugify(text: str, max_len: int = 80) -> str:
    """Filesystem-safe identifier — matches the slugify in keyword_artifact_writer.py."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled-product"


def load_keywords_artifact(product_identifier: str) -> dict | None:
    """Load a specific cached artifact by identifier. Returns None if missing."""
    path = keyword_cache_dir() / f"{product_identifier}.json"
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[keyword_cache_reader] Failed to load {path}: {exc}", file=sys.stderr)
        return None


def find_keywords_for_product(
    shopify_handle: str | None = None,
    amazon_asin: str | None = None,
    product_name: str | None = None,
) -> dict | None:
    """
    Try each identifier in the same priority order as skill #2 writes them.
    Returns the first artifact found, or None.
    """
    candidates: list[str] = []
    if shopify_handle and shopify_handle.strip():
        candidates.append(slugify(shopify_handle))
    if amazon_asin and amazon_asin.strip():
        candidates.append(amazon_asin.strip().upper())
    if product_name and product_name.strip():
        candidates.append(slugify(product_name))

    for ident in candidates:
        artifact = load_keywords_artifact(ident)
        if artifact:
            return artifact
    return None


def top_keywords(artifact: dict, n: int = 10) -> list[dict]:
    """Return the top-N keywords from an artifact, sorted by their rank field."""
    keywords = artifact.get("keywords_ranked", [])
    sorted_kws = sorted(keywords, key=lambda k: k.get("rank", 999))
    return sorted_kws[:n]


def is_artifact_fresh(artifact: dict, max_age_days: int = 30) -> bool:
    """
    Check whether the artifact is recent enough to trust. Default cutoff = 30 days.
    Older artifacts may not reflect current search trends.
    """
    generated_at = artifact.get("generated_at")
    if not generated_at:
        return False
    try:
        # Accept both Z-suffixed UTC and offset-bearing strings
        ts = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    except ValueError:
        return False
    age = datetime.now(timezone.utc) - ts
    return age.days <= max_age_days


def list_cached_products() -> list[str]:
    """List all product_identifiers with a cached keywords.json."""
    cache_dir = keyword_cache_dir()
    if not cache_dir.exists():
        return []
    return sorted(p.stem for p in cache_dir.glob("*.json"))


def keywords_for_placement(artifact: dict, placement: str) -> list[str]:
    """
    Return all keywords from the artifact whose recommended_placement list
    includes the given placement string (e.g., 'shopify_title', 'amazon_bullet_1').
    """
    result: list[str] = []
    for kw in artifact.get("keywords_ranked", []):
        placements = kw.get("recommended_placement", []) or []
        if placement in placements:
            result.append(kw.get("keyword", ""))
    return [k for k in result if k]


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        cached = list_cached_products()
        if not cached:
            print("No keyword artifacts cached yet.")
            print(f"Cache dir: {keyword_cache_dir()}")
        else:
            print(f"{len(cached)} cached keyword artifact(s):")
            for c in cached:
                print(f"  - {c}")
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: keyword_cache_reader.py show <product_identifier>")
            sys.exit(1)
        artifact = load_keywords_artifact(sys.argv[2])
        if not artifact:
            print(f"No artifact for '{sys.argv[2]}'")
            sys.exit(1)
        print(json.dumps(artifact, indent=2))
    elif cmd == "find":
        if len(sys.argv) < 3:
            print("Usage: keyword_cache_reader.py find <shopify_handle_or_product_name>")
            sys.exit(1)
        query = sys.argv[2]
        # Try as handle first, then as product name
        artifact = find_keywords_for_product(shopify_handle=query) or find_keywords_for_product(product_name=query)
        if not artifact:
            print(f"No artifact found for '{query}'")
            sys.exit(1)
        fresh = is_artifact_fresh(artifact)
        print(f"Found: {artifact.get('product_name')} ({artifact.get('product_identifier')})")
        print(f"Generated: {artifact.get('generated_at')} ({'fresh' if fresh else 'STALE — re-run SEO skill'})")
        print(f"Keywords ({len(artifact.get('keywords_ranked', []))}):")
        for kw in top_keywords(artifact, n=10):
            placements = ", ".join(kw.get("recommended_placement", []))
            print(f"  {kw.get('rank', '?'):>2}. {kw.get('keyword', '')}  →  {placements}")
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: keyword_cache_reader.py [list | show <id> | find <handle_or_name>]")
        sys.exit(1)
