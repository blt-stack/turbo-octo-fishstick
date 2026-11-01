"""
Writer for the shared objection cache.

Skill #10 (Review Response Writer) writes; downstream skills (Ad Creative
Generator, Landing Page Copywriter, Product Description Writer) read from
this cache to address customer doubts proactively.

Path convention:
    ~/.the-ecommerce-seller/cache/objections/{product-identifier}.json

Schema:
    {
      "product_identifier": "river-stone-pour-over",
      "product_name": "River Stone Pour-Over",
      "last_updated": "2026-05-22T16:30:00Z",
      "objections": [
        {
          "objection": "Shipping is unreliable",
          "surface_complaint": "Took 3 weeks to arrive with no updates",
          "issue_category": "shipping",
          "specific_failure_mode": "carrier delay no proactive comms",
          "platform_source": "trustpilot",
          "platform_review_id": "...",
          "reviewer_first_name": "Marcus",
          "star_rating": 1,
          "review_date": "2026-05-15",
          "objection_strength": 88,
          "frequency_tag": "novel" | "emerging" | "systemic",
          "do_not_mine": false,
          "downstream_handling_suggestions": {
            "ad_creative": "...",
            "landing_page_faq": "...",
            "product_description": "..."
          },
          "added_at": "2026-05-22T16:30:00Z",
          "added_by": "review-response-writer"
        },
        ...
      ]
    }

Usage:
    from objection_cache import save_objections, load_objections, top_objections

    save_objections("river-stone-pour-over", "River Stone Pour-Over", objections)
    payload = load_objections("river-stone-pour-over")
    top = top_objections(payload, n=10, min_frequency="emerging")
"""

import os
import shutil
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CACHE_SUBDIR = "cache/objections"

FREQUENCY_ORDER = {"novel": 0, "emerging": 1, "systemic": 2}


def find_plugin_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".claude-plugin" / "plugin.json").exists():
            return parent
    raise FileNotFoundError(
        f"Could not locate plugin root walking up from {here}."
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


def cache_dir() -> Path:
    return data_root() / CACHE_SUBDIR


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
        "objections": [],
    }


def load_objections(product_identifier: str) -> dict | None:
    path = cache_path_for(product_identifier)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[objection_cache] Failed to load {path}: {exc}", file=sys.stderr)
        return None


def _recompute_frequency_tags(objections: list[dict]) -> list[dict]:
    """
    Group existing objections by (issue_category, normalized objection text)
    and re-tag frequency:
      - 1 entry  → novel
      - 2-3      → emerging
      - 4+       → systemic
    """
    groups: dict[tuple[str, str], list[dict]] = {}
    for o in objections:
        cat = (o.get("issue_category") or "").strip().lower()
        text = (o.get("objection") or "").strip().lower()
        groups.setdefault((cat, text), []).append(o)

    for group_key, group in groups.items():
        size = len(group)
        if size == 1:
            tag = "novel"
        elif size <= 3:
            tag = "emerging"
        else:
            tag = "systemic"
        for o in group:
            o["frequency_tag"] = tag

    return objections


def _objection_already_cached(existing: list[dict], new_obj: dict) -> bool:
    new_id = new_obj.get("platform_review_id")
    new_text = (new_obj.get("objection") or "").strip().lower()
    for e in existing:
        if new_id and e.get("platform_review_id") == new_id and (e.get("objection") or "").strip().lower() == new_text:
            return True
    return False


def save_objections(
    product_identifier: str,
    product_name: str,
    new_objections: list[dict],
    merge: bool = True,
) -> Path:
    path = cache_path_for(product_identifier)
    path.parent.mkdir(parents=True, exist_ok=True)

    if merge and path.exists():
        existing = load_objections(product_identifier) or _empty_payload(product_identifier, product_name)
    else:
        existing = _empty_payload(product_identifier, product_name)

    existing["product_identifier"] = product_identifier
    existing["product_name"] = product_name or existing.get("product_name", "")
    existing["last_updated"] = _now_iso()

    existing.setdefault("objections", [])
    for o in (new_objections or []):
        o_copy = dict(o)
        o_copy.setdefault("added_at", _now_iso())
        o_copy.setdefault("added_by", "review-response-writer")
        o_copy.setdefault("do_not_mine", False)
        if not _objection_already_cached(existing["objections"], o_copy):
            existing["objections"].append(o_copy)

    # Recompute frequency_tag across the merged set so emerging/systemic tags stay accurate
    existing["objections"] = _recompute_frequency_tags(existing["objections"])

    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def top_objections(
    payload: dict,
    n: int = 10,
    min_frequency: str | None = None,
    issue_category: str | None = None,
) -> list[dict]:
    """Return top-N objections by strength, optionally filtered by frequency tier or issue category."""
    if not payload:
        return []
    items = [o for o in payload.get("objections", []) if not o.get("do_not_mine")]
    if min_frequency:
        min_rank = FREQUENCY_ORDER.get(min_frequency, 0)
        items = [o for o in items if FREQUENCY_ORDER.get(o.get("frequency_tag", "novel"), 0) >= min_rank]
    if issue_category:
        items = [o for o in items if o.get("issue_category", "").lower() == issue_category.lower()]
    items.sort(key=lambda o: o.get("objection_strength", 0), reverse=True)
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
            print("No objection artifacts cached yet.")
            print(f"Cache dir: {cache_dir()}")
        else:
            print(f"{len(cached)} cached objection artifact(s):")
            for c in cached:
                print(f"  - {c}")
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: objection_cache.py show <product_identifier>")
            sys.exit(1)
        payload = load_objections(sys.argv[2])
        if not payload:
            print(f"No objections for '{sys.argv[2]}'")
            sys.exit(1)
        print(json.dumps(payload, indent=2))
    elif cmd == "top":
        if len(sys.argv) < 3:
            print("Usage: objection_cache.py top <product_identifier> [min_frequency] [issue_category]")
            sys.exit(1)
        payload = load_objections(sys.argv[2])
        if not payload:
            print(f"No objections for '{sys.argv[2]}'")
            sys.exit(1)
        min_freq = sys.argv[3] if len(sys.argv) >= 4 else None
        cat = sys.argv[4] if len(sys.argv) >= 5 else None
        for o in top_objections(payload, n=10, min_frequency=min_freq, issue_category=cat):
            print(f"  [{o.get('frequency_tag', '?'):>9}] {o.get('objection', '')}  (cat: {o.get('issue_category', '')})")
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: objection_cache.py [list | show <id> | top <id> [min_frequency] [issue_category]]")
        sys.exit(1)
