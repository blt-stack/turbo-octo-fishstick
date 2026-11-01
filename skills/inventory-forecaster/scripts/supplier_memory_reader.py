"""
Reader for the supplier memory cache written by skill #11 (Supplier Negotiation Assistant).

This skill (#12, Inventory Forecaster) reads lead times, MOQs, payment terms,
and unit prices from the supplier files to inform reorder-date computation.

Path conventions (must match skill #11's supplier_memory.py):
    ~/.the-ecommerce-seller/cache/suppliers/{supplier_id}.json
    ~/.the-ecommerce-seller/cache/sku_to_supplier.json

Usage:
    from supplier_memory_reader import (
        get_sku_supplier_details,
        load_sku_supplier_mapping,
        save_sku_supplier_mapping,
    )

    details = get_sku_supplier_details("RS-POUR-OVER-001")
    # details = {"supplier_id": "...", "lead_time_days": 45, "moq": 1500, ...}

CLI:
    python supplier_memory_reader.py list_mappings
    python supplier_memory_reader.py details <sku>
"""

import os
import shutil
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


SKU_TO_SUPPLIER_FILENAME = "cache/sku_to_supplier.json"
SUPPLIER_CACHE_SUBDIR = "cache/suppliers"

REGIONAL_DEFAULT_LEAD_TIME = {
    "china": 45,
    "vietnam": 40,
    "india": 35,
    "north_america": 14,
    "eu": 21,
}

REGIONAL_DEFAULT_TRANSIT = {
    "china_sea": 30,
    "china_air": 7,
    "vietnam_sea": 25,
    "vietnam_air": 5,
    "india_sea": 28,
    "india_air": 4,
    "north_america": 4,
    "eu_to_us": 12,
}


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


def sku_to_supplier_path() -> Path:
    return data_root() / SKU_TO_SUPPLIER_FILENAME


def supplier_cache_dir() -> Path:
    return data_root() / SUPPLIER_CACHE_SUBDIR


def supplier_file_path(supplier_id: str) -> Path:
    return supplier_cache_dir() / f"{supplier_id}.json"


def load_sku_supplier_mapping() -> dict:
    path = sku_to_supplier_path()
    if not path.exists():
        return {"_meta": {"version": 1}, "_mappings": {}}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Normalize: ensure _mappings key exists
        if "_mappings" not in data:
            # Old format: top-level keys are SKUs
            mappings = {k: v for k, v in data.items() if not k.startswith("_")}
            data = {"_meta": data.get("_meta", {"version": 1}), "_mappings": mappings}
        return data
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[supplier_memory_reader] Failed to load mapping: {exc}", file=sys.stderr)
        return {"_meta": {"version": 1}, "_mappings": {}}


def save_sku_supplier_mapping(data: dict) -> Path:
    path = sku_to_supplier_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data.setdefault("_meta", {})["last_updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def upsert_sku_supplier_mapping(sku: str, primary_supplier_id: str, overrides: dict | None = None) -> None:
    data = load_sku_supplier_mapping()
    data.setdefault("_mappings", {})
    entry = data["_mappings"].setdefault(sku, {})
    entry["primary_supplier_id"] = primary_supplier_id
    if overrides:
        entry.setdefault("supplier_specific_overrides", {}).update(overrides)
    save_sku_supplier_mapping(data)


def load_supplier_file(supplier_id: str) -> dict | None:
    path = supplier_file_path(supplier_id)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def get_sku_supplier_details(sku: str) -> dict | None:
    """
    Returns full reorder-relevant details for a SKU by walking the cascade:
    1. sku_to_supplier.json mapping → supplier_specific_overrides
    2. supplier file's product_lines_sourced[matching]
    3. supplier-wide defaults
    4. regional defaults
    """
    mapping = load_sku_supplier_mapping()
    sku_entry = mapping.get("_mappings", {}).get(sku)
    if not sku_entry:
        return None

    supplier_id = sku_entry.get("primary_supplier_id")
    if not supplier_id:
        return None

    overrides = sku_entry.get("supplier_specific_overrides", {}) or {}
    supplier = load_supplier_file(supplier_id)

    # Start with overrides as the most specific layer
    details = dict(overrides)
    details["supplier_id"] = supplier_id
    details["sku"] = sku

    if supplier:
        details["supplier_company_name"] = supplier.get("company_name", "")
        details["supplier_region"] = supplier.get("region", "")
        details["supplier_country"] = supplier.get("country", "")
        details["supplier_relationship_stage"] = supplier.get("relationship_stage", "new")
        # Payment terms from supplier
        if "payment_terms_in_force" not in details:
            pt = supplier.get("payment_terms_in_force", {}) or {}
            details["payment_terms_in_force"] = _normalize_payment_terms(pt.get("structure", "30/70 TT"))
        # Look for product-line specific entry in supplier file
        for prod in (supplier.get("product_lines_sourced") or []):
            if prod.get("sku") == sku or prod.get("product_name", "").lower().replace(" ", "-") == sku.lower():
                if "lead_time_days" not in details and "lead_time_days" in prod:
                    details["lead_time_days"] = prod["lead_time_days"]
                if "moq" not in details and "moq" in prod:
                    details["moq"] = prod["moq"]
                if "current_unit_price_usd" not in details and "current_unit_price_usd" in prod:
                    details["current_unit_price_usd"] = prod["current_unit_price_usd"]
                break

    # Apply regional defaults for anything still missing
    region = details.get("supplier_region", "")
    if "lead_time_days" not in details:
        details["lead_time_days"] = REGIONAL_DEFAULT_LEAD_TIME.get(region, 30)
    if "transit_days" not in details:
        transit_mode = details.get("transit_mode", "sea") if region in ("china", "vietnam", "india") else "default"
        if region == "china":
            details["transit_days"] = REGIONAL_DEFAULT_TRANSIT["china_air"] if transit_mode == "air" else REGIONAL_DEFAULT_TRANSIT["china_sea"]
        elif region == "vietnam":
            details["transit_days"] = REGIONAL_DEFAULT_TRANSIT["vietnam_air"] if transit_mode == "air" else REGIONAL_DEFAULT_TRANSIT["vietnam_sea"]
        elif region == "india":
            details["transit_days"] = REGIONAL_DEFAULT_TRANSIT["india_air"] if transit_mode == "air" else REGIONAL_DEFAULT_TRANSIT["india_sea"]
        elif region == "north_america":
            details["transit_days"] = REGIONAL_DEFAULT_TRANSIT["north_america"]
        elif region == "eu":
            details["transit_days"] = REGIONAL_DEFAULT_TRANSIT["eu_to_us"]
        else:
            details["transit_days"] = 14

    if "payment_terms_in_force" not in details:
        details["payment_terms_in_force"] = "30/70 TT"

    if "moq" not in details:
        details["moq"] = 100  # generic fallback; will trigger buyer prompt in skill

    if "current_unit_price_usd" not in details:
        details["current_unit_price_usd"] = None  # forces buyer to provide

    return details


def _normalize_payment_terms(s: str) -> str:
    """Normalize free-form payment-terms strings to a canonical token."""
    if not s:
        return "30/70 TT"
    s_low = s.lower()
    if "100%" in s_low or "upfront" in s_low or "full" in s_low:
        return "100_upfront"
    if "30/70" in s_low or "30/70" in s or "30%" in s_low:
        if "bl" in s_low or "b/l" in s_low or "against" in s_low:
            return "30_70_tt_against_bl"
        return "30_70_tt_before_shipping"
    if "lc" in s_low or "letter of credit" in s_low:
        return "lc_at_sight"
    if "net 30" in s_low or "net30" in s_low:
        return "net_30"
    if "net 45" in s_low:
        return "net_45"
    if "net 60" in s_low:
        return "net_60"
    return s  # unknown — leave as-is for buyer review


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list_mappings"
    if cmd == "list_mappings":
        data = load_sku_supplier_mapping()
        mappings = data.get("_mappings", {})
        if not mappings:
            print("No SKU-to-supplier mappings yet.")
        else:
            print(f"{len(mappings)} mapping(s):")
            for sku, entry in sorted(mappings.items()):
                print(f"  {sku}  →  {entry.get('primary_supplier_id', '?')}")
    elif cmd == "details":
        if len(sys.argv) < 3:
            print("Usage: supplier_memory_reader.py details <sku>")
            sys.exit(1)
        details = get_sku_supplier_details(sys.argv[2])
        if not details:
            print(f"No supplier mapping for SKU '{sys.argv[2]}'")
            sys.exit(1)
        print(json.dumps(details, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: supplier_memory_reader.py [list_mappings | details <sku>]")
        sys.exit(1)
