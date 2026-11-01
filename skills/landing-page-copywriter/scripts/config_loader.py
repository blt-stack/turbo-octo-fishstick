"""
Config loader / saver for The E-Commerce Seller plugin.

Shared by every skill in the plugin. Handles:
- Locating the config file (lives at ~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json)
- Loading and validating it
- Detecting incomplete configs (so the calling skill can trigger onboarding)
- Saving updates atomically
- Stamping last_updated timestamps

Usage from another script:
    from config_loader import load_config, save_config, is_complete

    config = load_config()
    if not is_complete(config):
        # trigger onboarding flow
        ...
    save_config(updated_config)
"""

import shutil
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

CONFIG_FILENAME = "the-ecommerce-seller.config.json"
CONFIG_SUBDIR = "config"


def find_plugin_root(start: Path | None = None) -> Path:
    """Walk up from this script until we find a directory containing .claude-plugin/plugin.json."""
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".claude-plugin" / "plugin.json").exists():
            return parent
    raise FileNotFoundError(
        "Could not locate plugin root (no .claude-plugin/plugin.json found walking up from "
        f"{here}). The config loader needs to live inside the plugin directory tree."
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


def config_path() -> Path:
    return data_root() / CONFIG_SUBDIR / CONFIG_FILENAME


def example_config_path() -> Path:
    """Find the config.example.json shipped with this skill."""
    return Path(__file__).resolve().parent.parent / "config.example.json"


def load_config() -> dict:
    """Load the buyer's config. Returns the example config if none exists yet."""
    path = config_path()
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    # Fall back to the example so the caller sees the expected shape
    with example_config_path().open("r", encoding="utf-8") as f:
        return json.load(f)


def is_complete(config: dict) -> bool:
    """
    Returns True if the config has enough filled-in fields to skip onboarding.
    Minimum required: brand_name, at least one platform enabled, and a brand_voice
    profile with non-empty tone.
    """
    store = config.get("store", {})
    if not store.get("brand_name"):
        return False

    platforms = config.get("platforms_enabled", {})
    if not any(platforms.values()):
        return False

    voice = config.get("brand_voice", {})
    if not voice.get("tone"):
        return False

    return True


def missing_fields(config: dict) -> list[str]:
    """Returns a human-readable list of what's missing. Useful for partial-onboarding flows."""
    missing = []
    store = config.get("store", {})
    if not store.get("brand_name"):
        missing.append("store.brand_name")
    if not any(config.get("platforms_enabled", {}).values()):
        missing.append("platforms_enabled (at least one)")
    voice = config.get("brand_voice", {})
    if not voice.get("tone"):
        missing.append("brand_voice.tone")
    if not voice.get("archetype"):
        missing.append("brand_voice.archetype")
    if not config.get("audience", {}).get("description"):
        missing.append("audience.description")
    return missing


def save_config(config: dict) -> Path:
    """Save config atomically. Creates .config/ if needed. Stamps brand_voice.last_updated."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    # Stamp last_updated
    config.setdefault("brand_voice", {})
    config["brand_voice"]["last_updated"] = datetime.now(timezone.utc).date().isoformat()

    # Atomic write: write to a tmp file, then rename
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def update_config(updates: dict) -> dict:
    """
    Merge updates into the existing config and save. Returns the merged config.
    Top-level keys are deep-merged one level down (e.g., partial brand_voice updates
    don't wipe other brand_voice fields).
    """
    config = load_config()
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(config.get(key), dict):
            config[key].update(value)
        else:
            config[key] = value
    save_config(config)
    return config


if __name__ == "__main__":
    # CLI for quick inspection: python config_loader.py [status|show|missing]
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    cfg = load_config()
    if cmd == "show":
        print(json.dumps(cfg, indent=2))
    elif cmd == "missing":
        missing = missing_fields(cfg)
        if missing:
            print("Missing fields:")
            for m in missing:
                print(f"  - {m}")
        else:
            print("Config is complete.")
    else:
        path = config_path()
        exists = path.exists()
        complete = is_complete(cfg) if exists else False
        print(f"Config path:  {path}")
        print(f"Exists:       {exists}")
        print(f"Complete:     {complete}")
        if exists and not complete:
            print("Missing:")
            for m in missing_fields(cfg):
                print(f"  - {m}")
