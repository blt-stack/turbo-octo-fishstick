"""
Writes reorder triggers to .cache/reorder_triggers/{date}.json for skill #11 to consume.

Each trigger has urgency, SKU, supplier, reorder quantity, deposit date, etc.
The Supplier Negotiation Assistant (skill #11) reads pending (non-consumed) triggers
when the buyer asks "what supplier letters do I need to send?"

Schema documented in templates/reorder-triggers.md.
"""

import os
import shutil
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


CACHE_SUBDIR = "cache/reorder_triggers"


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


def cache_path_for_date(run_date: str) -> Path:
    """run_date in YYYY-MM-DD format."""
    return cache_dir() / f"{run_date}.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_triggers(triggers: list[dict], run_date: str | None = None, scope: str = "full_catalog") -> Path:
    """
    Write a list of triggers to today's reorder triggers file.
    Appends to existing file if same date.
    """
    run_date = run_date or _now_iso()[:10]
    run_at = _now_iso()
    run_id = f"fc-{run_date}-{datetime.now().strftime('%H%M')}"

    path = cache_path_for_date(run_date)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        data["triggers"].extend(triggers)
    else:
        data = {
            "forecast_run_at": run_at,
            "forecast_run_id": run_id,
            "scope": scope,
            "triggers": triggers,
            "_meta": {
                "schema_version": 1,
                "writer": "inventory-forecaster",
            },
        }

    # Update meta totals
    triggers_all = data["triggers"]
    data["_meta"]["total_triggers"] = len(triggers_all)
    urgency_dist: dict[str, int] = {}
    for t in triggers_all:
        u = t.get("urgency", "unknown")
        urgency_dist[u] = urgency_dist.get(u, 0) + 1
    data["_meta"]["urgency_distribution"] = urgency_dist

    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def list_pending_triggers(days_back: int = 14) -> list[dict]:
    """Return all unconsumed triggers from the last N days."""
    d = cache_dir()
    if not d.exists():
        return []
    pending = []
    for path in sorted(d.glob("*.json"), reverse=True):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        for trigger in data.get("triggers", []):
            if not trigger.get("consumed_by_skill_11"):
                pending.append(trigger)
    return pending


def trigger_from_forecast_result(forecast_result: dict) -> dict | None:
    """
    Convert a forecast_sku() result into a reorder trigger dict.
    Returns None if no trigger is warranted (urgency = healthy).
    """
    reorder = forecast_result.get("reorder_calc", {})
    urgency = reorder.get("urgency", "healthy")
    if urgency not in ("urgent", "reorder_soon", "stockout_imminent"):
        return None

    audit = forecast_result.get("audit", {})

    notes = ""
    days_short = reorder.get("days_short_before_arrival", 0)
    expedite_suggested = False
    if urgency == "stockout_imminent" or days_short > 0:
        notes = f"Lead time exceeds days-until-stockout by {days_short} days — consider air-freight expedite or accept partial stockout."
        expedite_suggested = True

    return {
        "sku": forecast_result.get("sku"),
        "product_name": forecast_result.get("product_name", ""),
        "supplier_id": forecast_result.get("supplier_id", ""),
        "urgency": urgency,
        "trigger_reason": f"Days until stockout ({reorder.get('days_until_stockout_p50', 0):.0f}) "
                          f"vs. lead time ({reorder.get('lead_time_days', 0)}) "
                          f"+ safety stock + reorder window",
        "current_on_hand": reorder.get("current_on_hand"),
        "velocity_p50_units_per_day": reorder.get("velocity_p50_units_per_day"),
        "velocity_p90_units_per_day": reorder.get("velocity_p90_units_per_day"),
        "days_until_stockout_p50": round(reorder.get("days_until_stockout_p50", 0), 1),
        "days_until_stockout_p90": round(reorder.get("days_until_stockout_p90", 0), 1),
        "lead_time_days": reorder.get("lead_time_days"),
        "transit_days": reorder.get("transit_days"),
        "moq": reorder.get("moq"),
        "current_unit_price_usd": reorder.get("estimated_reorder_cost_usd", 0) / max(reorder.get("recommended_reorder_quantity", 1), 1) if reorder.get("recommended_reorder_quantity") else None,
        "payment_terms_in_force": reorder.get("payment_terms_in_force"),
        "recommended_reorder_quantity": reorder.get("recommended_reorder_quantity"),
        "recommended_deposit_date": reorder.get("recommended_deposit_date"),
        "expected_arrive_date": reorder.get("expected_arrive_date"),
        "days_short_before_arrival": days_short,
        "estimated_reorder_cost_usd": reorder.get("estimated_reorder_cost_usd"),
        "expedite_suggested": expedite_suggested,
        "notes": notes,
        "consumed_by_skill_11": False,
        "consumed_at": None,
    }


def list_cached_dates() -> list[str]:
    d = cache_dir()
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.json"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        dates = list_cached_dates()
        if not dates:
            print("No reorder trigger files cached yet.")
            print(f"Cache dir: {cache_dir()}")
        else:
            print(f"{len(dates)} cached run(s):")
            for d in dates:
                path = cache_path_for_date(d)
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                meta = data.get("_meta", {})
                print(f"  {d}: {meta.get('total_triggers', 0)} trigger(s); dist: {meta.get('urgency_distribution', {})}")
    elif cmd == "pending":
        pending = list_pending_triggers()
        if not pending:
            print("No pending triggers.")
        else:
            print(f"{len(pending)} pending trigger(s):")
            for t in pending:
                print(f"  [{t.get('urgency', '?')}] {t.get('sku', '?')} → {t.get('supplier_id', '?')} "
                      f"({t.get('days_until_stockout_p50', '?')} days until stockout)")
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: reorder_trigger_writer.py show <YYYY-MM-DD>")
            sys.exit(1)
        path = cache_path_for_date(sys.argv[2])
        if not path.exists():
            print(f"No trigger file for {sys.argv[2]}")
            sys.exit(1)
        with path.open("r", encoding="utf-8") as f:
            print(f.read())
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: reorder_trigger_writer.py [list | pending | show <date>]")
        sys.exit(1)
