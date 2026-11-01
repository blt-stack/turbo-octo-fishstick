"""
Bundle cache writer/reader for the shared bundles store at
~/.the-ecommerce-seller/cache/bundles/{bundle-slug}.json

Downstream consumers (Landing Page Copywriter, Product Description Writer,
Ad Creative Generator, Campaign Calendar Planner) read from this cache.
"""

import os
import shutil
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CACHE_SUBDIR = "cache/bundles"


def find_plugin_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".claude-plugin" / "plugin.json").exists():
            return parent
    raise FileNotFoundError(f"Could not locate plugin root walking up from {here}.")

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
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled-bundle"


def cache_path_for(bundle_id: str) -> Path:
    return cache_dir() / f"{bundle_id}.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_bundle(bundle: dict) -> Path:
    """Save a single bundle to the cache."""
    bundle_id = bundle.get("bundle_id") or slugify(bundle.get("bundle_name_descriptive", "untitled"))
    bundle["bundle_id"] = bundle_id
    bundle.setdefault("created_at", _now_iso())
    bundle["last_updated"] = _now_iso()
    bundle.setdefault("created_by", "bundle-builder")
    bundle.setdefault("downstream_consumed_by", [])
    bundle.setdefault("_schema_version", 1)

    path = cache_path_for(bundle_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def save_bundles(bundles: list[dict]) -> list[Path]:
    """Save multiple bundles. Returns list of paths."""
    return [save_bundle(b) for b in bundles]


def load_bundle(bundle_id: str) -> dict | None:
    path = cache_path_for(bundle_id)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def list_bundles(active_only: bool = True) -> list[dict]:
    d = cache_dir()
    if not d.exists():
        return []
    bundles = []
    for path in sorted(d.glob("*.json")):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if active_only and not data.get("is_active", True):
            continue
        bundles.append(data)
    return bundles


def deactivate_bundle(bundle_id: str) -> bool:
    bundle = load_bundle(bundle_id)
    if not bundle:
        return False
    bundle["is_active"] = False
    save_bundle(bundle)
    return True


def mark_consumed_by(bundle_id: str, skill_name: str, output_path: str | None = None) -> bool:
    """Mark that a downstream skill consumed this bundle."""
    bundle = load_bundle(bundle_id)
    if not bundle:
        return False
    bundle.setdefault("downstream_consumed_by", []).append({
        "skill": skill_name,
        "consumed_at": _now_iso(),
        "output_path": output_path or "",
    })
    save_bundle(bundle)
    return True


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        bundles = list_bundles(active_only=False)
        if not bundles:
            print("No bundles cached yet.")
            print(f"Cache dir: {cache_dir()}")
        else:
            print(f"{len(bundles)} cached bundle(s):")
            for b in bundles:
                active = "active" if b.get("is_active") else "inactive"
                score = (b.get("discovery_evidence") or {}).get("composite_score", 0)
                print(f"  [{active:8s}] {b.get('bundle_id'):40s} score={score:5.1f}  type={b.get('bundle_type_primary')}")
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: bundle_cache.py show <bundle_id>")
            sys.exit(1)
        bundle = load_bundle(sys.argv[2])
        if not bundle:
            print(f"No bundle for '{sys.argv[2]}'")
            sys.exit(1)
        print(json.dumps(bundle, indent=2))
    elif cmd == "deactivate":
        if len(sys.argv) < 3:
            print("Usage: bundle_cache.py deactivate <bundle_id>")
            sys.exit(1)
        if deactivate_bundle(sys.argv[2]):
            print(f"Deactivated {sys.argv[2]}")
        else:
            print(f"No bundle found")
            sys.exit(1)
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: bundle_cache.py [list | show <id> | deactivate <id>]")
        sys.exit(1)
