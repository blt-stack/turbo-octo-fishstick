"""
Shared reader/writer for the UGC hooks cache. The same file ships in every
skill that touches the cache (Ad Creative Generator, UGC Creator Brief Writer,
Email Flow Architect, Campaign Calendar Planner) — keep the copies identical.

Ad Creative Generator (#5) and UGC Creator Brief Writer (#6) both write hooks;
every skill above can read them. The "context" field on each hook records
which side wrote it:
  - "ad_caption"     — written by Ad Creative Generator
  - "creator_script" — written by UGC Creator Brief Writer

save_hooks() stamps "source" with the calling skill's folder name and picks
the matching default context automatically, so callers rarely need to pass
either. Hooks whose text already exists in the same archetype are skipped,
so re-running a skill doesn't pile up duplicates.

When skill #5 reads from the cache, it prefers "creator_script" hooks for
video-wrapper ad copy (since the creator's actual delivered line matters) and
falls back to "ad_caption" hooks if no creator_script hooks exist.

When skill #6 reads from the cache, it reuses its own "creator_script" hooks
for consistency and adapts "ad_caption" hooks into spoken, on-camera lines.

Path convention:
    ~/.the-ecommerce-seller/cache/ugc_hooks/{product-identifier}.json

Schema:
    {
      "product_identifier": "river-stone-pour-over",
      "product_name": "River Stone Pour-Over",
      "last_updated": "2026-05-22T16:00:00Z",
      "hooks_by_archetype": {
        "problem_aware": [
          {"text": "...", "source": "ad-creative-generator",
           "context": "ad_caption", "platform": "meta", "added_at": "..."}
        ],
        "social_proof": [...],
        "transformation": [...],
        "curiosity_gap": [...],
        "contrarian": [...]
      }
    }
"""

import os
import shutil
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CACHE_SUBDIR = "cache/ugc_hooks"

SKILL_NAME = Path(__file__).resolve().parent.parent.name

CREATOR_SCRIPT_WRITERS = {"ugc-creator-brief-writer"}

ARCHETYPES = (
    "problem_aware",
    "social_proof",
    "transformation",
    "curiosity_gap",
    "contrarian",
)


def find_plugin_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".claude-plugin" / "plugin.json").exists():
            return parent
    raise FileNotFoundError(
        "Could not locate plugin root (no .claude-plugin/plugin.json found walking up from "
        f"{here})."
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


def _norm(text: str) -> str:
    return " ".join(text.lower().split())


def _empty_payload(product_identifier: str, product_name: str) -> dict:
    return {
        "product_identifier": product_identifier,
        "product_name": product_name,
        "last_updated": _now_iso(),
        "hooks_by_archetype": {a: [] for a in ARCHETYPES},
    }


def load_hooks(product_identifier: str) -> dict | None:
    """
    Load the hooks cache for this product. Returns None if missing.
    The returned dict's hooks_by_archetype always has all 5 archetype keys
    (with empty lists where no hooks exist) for safer caller iteration.
    """
    path = cache_path_for(product_identifier)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[ugc_hook_cache] Failed to load {path}: {exc}", file=sys.stderr)
        return None
    # Normalize missing archetype keys to empty lists
    data.setdefault("hooks_by_archetype", {})
    for a in ARCHETYPES:
        data["hooks_by_archetype"].setdefault(a, [])
    return data


def find_hooks_for_product(
    shopify_handle: str | None = None,
    amazon_asin: str | None = None,
    product_name: str | None = None,
) -> dict | None:
    """Try each identifier in priority order, return first artifact found."""
    candidates: list[str] = []
    if shopify_handle and shopify_handle.strip():
        candidates.append(slugify(shopify_handle))
    if amazon_asin and amazon_asin.strip():
        candidates.append(amazon_asin.strip().upper())
    if product_name and product_name.strip():
        candidates.append(slugify(product_name))
    for ident in candidates:
        loaded = load_hooks(ident)
        if loaded:
            return loaded
    return None


def hooks_filtered_by_context(payload: dict, prefer_context: str = "creator_script") -> dict[str, list[dict]]:
    """
    Returns hooks_by_archetype but prioritizing the preferred context.
    If preferred context has hooks for an archetype, only those are returned.
    If preferred context is empty for that archetype, all hooks (any context)
    are returned as fallback.
    """
    if not payload:
        return {a: [] for a in ARCHETYPES}
    out: dict[str, list[dict]] = {}
    for archetype in ARCHETYPES:
        all_hooks = payload.get("hooks_by_archetype", {}).get(archetype, [])
        preferred = [h for h in all_hooks if h.get("context") == prefer_context]
        out[archetype] = preferred if preferred else list(all_hooks)
    return out


def save_hooks(
    product_identifier: str,
    product_name: str,
    new_hooks: dict[str, list[dict]],
    source: str | None = None,
    merge: bool = True,
) -> Path:
    """
    Save hooks to the cache.

    new_hooks shape: {archetype_key: [{"text": "...", "context": "...", "platform": "..."}, ...]}

    Each new hook gets "source", "context" and "added_at" auto-stamped if not
    present. source defaults to the calling skill's folder name; context
    defaults to "creator_script" for the UGC Creator Brief Writer and
    "ad_caption" for everything else. Hooks whose text (ignoring case and
    spacing) already exists in that archetype are skipped.

    When merge=True (default), new hooks are appended to existing ones from
    other writers (preserving skill #6's writes). When merge=False, the file
    is fully overwritten.
    """
    path = cache_path_for(product_identifier)
    path.parent.mkdir(parents=True, exist_ok=True)

    if merge and path.exists():
        existing = load_hooks(product_identifier) or _empty_payload(product_identifier, product_name)
    else:
        existing = _empty_payload(product_identifier, product_name)

    # Update top-level fields
    existing["product_identifier"] = product_identifier
    existing["product_name"] = product_name or existing.get("product_name", "")
    existing["last_updated"] = _now_iso()

    source = source or SKILL_NAME
    default_context = "creator_script" if source in CREATOR_SCRIPT_WRITERS else "ad_caption"

    for archetype in ARCHETYPES:
        new_list = new_hooks.get(archetype, []) or []
        bucket = existing["hooks_by_archetype"].setdefault(archetype, [])
        seen = {_norm(h.get("text", "")) for h in bucket}
        for hook in new_list:
            key = _norm(hook.get("text", ""))
            if not key or key in seen:
                continue
            hook_copy = dict(hook)
            hook_copy.setdefault("source", source)
            hook_copy.setdefault("added_at", _now_iso())
            hook_copy.setdefault("context", default_context)
            bucket.append(hook_copy)
            seen.add(key)

    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


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
            print("No hooks artifacts cached yet.")
            print(f"Cache dir: {cache_dir()}")
        else:
            print(f"{len(cached)} cached UGC hooks artifact(s):")
            for c in cached:
                print(f"  - {c}")
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: ugc_hook_cache.py show <product_identifier>")
            sys.exit(1)
        payload = load_hooks(sys.argv[2])
        if not payload:
            print(f"No hooks for '{sys.argv[2]}'")
            sys.exit(1)
        print(json.dumps(payload, indent=2))
    elif cmd == "find":
        if len(sys.argv) < 3:
            print("Usage: ugc_hook_cache.py find <handle_or_name>")
            sys.exit(1)
        query = sys.argv[2]
        payload = find_hooks_for_product(shopify_handle=query) or find_hooks_for_product(product_name=query)
        if not payload:
            print(f"No hooks for '{query}'")
            sys.exit(1)
        print(f"Found: {payload.get('product_name')} ({payload.get('product_identifier')})")
        for archetype in ARCHETYPES:
            hooks = payload.get("hooks_by_archetype", {}).get(archetype, [])
            print(f"  {archetype}: {len(hooks)} hooks")
            for h in hooks[:3]:
                ctx = h.get("context", "?")
                src = h.get("source", "?")
                text = h.get("text", "")[:60]
                print(f"    [{ctx} by {src}] {text}")
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: ugc_hook_cache.py [list | show <id> | find <handle_or_name>]")
        sys.exit(1)
