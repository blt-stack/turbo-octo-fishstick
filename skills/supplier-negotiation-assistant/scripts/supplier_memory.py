"""
Per-supplier relationship state cache reader/writer.

Skill #11 (Supplier Negotiation Assistant) is the primary writer; the cache
turns each letter into part of an ongoing relationship rather than a cold
email.

Path convention:
    ~/.the-ecommerce-seller/cache/suppliers/{supplier_id}.json

Where supplier_id is derived from the company name (slug-safe).

Schema (full schema documented in templates/supplier-memory.md).

Usage:
    from supplier_memory import (
        load_supplier,
        save_supplier,
        upsert_supplier,
        log_letter_sent,
        transition_stage,
        list_pending_responses,
        supplier_id_from_company,
    )

CLI:
    python supplier_memory.py list
    python supplier_memory.py show <supplier_id>
    python supplier_memory.py pending           # all suppliers with open responses
"""

import os
import shutil
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


CACHE_SUBDIR = "cache/suppliers"

VALID_STAGES = {"new", "developing", "established", "strained", "dormant", "ended"}

# How many days to wait for a response per region before recommending follow-up
REGION_RESPONSE_WINDOWS = {
    "china": 3,
    "vietnam": 3,
    "india": 2,
    "north_america": 2,
    "eu": 4,
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


def cache_dir() -> Path:
    return data_root() / CACHE_SUBDIR


def slugify(text: str, max_len: int = 80) -> str:
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "unnamed-supplier"


def supplier_id_from_company(company_name: str, contact_name: str | None = None) -> str:
    """Generate a filesystem-safe supplier_id from company + optional contact."""
    base = slugify(company_name)
    if contact_name:
        contact_slug = slugify(contact_name)
        return f"{base}-{contact_slug}"[:80]
    return base


def cache_path_for(supplier_id: str) -> Path:
    return cache_dir() / f"{supplier_id}.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _empty_payload(supplier_id: str, company_name: str, region: str) -> dict:
    today = _now_iso()[:10]
    return {
        "supplier_id": supplier_id,
        "company_name": company_name,
        "primary_contact": {
            "name": "",
            "honorific": "",
            "role": "",
            "preferred_address": "",
            "email": "",
            "alibaba_username": "",
            "phone": "",
            "whatsapp": "",
        },
        "region": region,
        "country": "",
        "city": "",
        "language_preference": "english",
        "first_contact_date": today,
        "relationship_stage": "new",
        "relationship_stage_history": [
            {"stage": "new", "since": today, "until": None, "reason": "First contact"}
        ],
        "product_lines_sourced": [],
        "known_moqs": {},
        "known_pricing_tiers": {},
        "payment_terms_in_force": {},
        "letters_sent": [],
        "pending_responses": [],
        "response_time_pattern": {
            "average_days": None,
            "fastest_days": None,
            "slowest_days": None,
            "samples_n": 0,
        },
        "communication_preferences": {
            "primary_channel": "email",
            "fallback_channel": "alibaba_trademessenger",
            "time_zone": "",
            "business_hours_local": "",
            "holidays_observed": [],
        },
        "notes": [],
        "last_contact_at": today,
        "last_updated": _now_iso(),
    }


def load_supplier(supplier_id: str) -> dict | None:
    path = cache_path_for(supplier_id)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[supplier_memory] Failed to load {path}: {exc}", file=sys.stderr)
        return None


def find_supplier_by_company(company_name: str, contact_name: str | None = None) -> dict | None:
    """Try to load a supplier file by company + optional contact name."""
    sid = supplier_id_from_company(company_name, contact_name)
    payload = load_supplier(sid)
    if payload:
        return payload
    # Fallback: try without contact name
    if contact_name:
        sid_base = supplier_id_from_company(company_name)
        return load_supplier(sid_base)
    return None


def save_supplier(payload: dict) -> Path:
    """Save the supplier payload atomically."""
    supplier_id = payload.get("supplier_id")
    if not supplier_id:
        raise ValueError("payload missing supplier_id")
    path = cache_path_for(supplier_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload["last_updated"] = _now_iso()

    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def upsert_supplier(
    company_name: str,
    region: str,
    contact_name: str | None = None,
    extra_fields: dict | None = None,
) -> dict:
    """
    Load existing supplier or create a new one. Returns the payload.
    Use this as the entry point at the start of any letter draft.
    """
    sid = supplier_id_from_company(company_name, contact_name)
    payload = load_supplier(sid)
    if not payload:
        payload = _empty_payload(sid, company_name, region)
        if contact_name:
            payload["primary_contact"]["name"] = contact_name
    # Merge in any extra fields the caller wants set
    if extra_fields:
        for key, value in extra_fields.items():
            if isinstance(value, dict) and isinstance(payload.get(key), dict):
                payload[key].update(value)
            else:
                payload[key] = value
    save_supplier(payload)
    return payload


def log_letter_sent(
    supplier_id: str,
    letter_type: str,
    summary: str,
    expected_response_days: int | None = None,
) -> dict | None:
    """
    Append to letters_sent and pending_responses. Returns the updated payload.
    """
    payload = load_supplier(supplier_id)
    if not payload:
        return None
    today = _now_iso()[:10]
    payload["letters_sent"].append({
        "date": today,
        "type": letter_type,
        "summary": summary,
        "outcome": "pending",
        "response_time_days": None,
    })
    if expected_response_days is None:
        expected_response_days = REGION_RESPONSE_WINDOWS.get(payload.get("region", ""), 3)
    expected_by = (datetime.now(timezone.utc) + timedelta(days=expected_response_days)).date().isoformat()
    follow_up_due = (datetime.now(timezone.utc) + timedelta(days=expected_response_days + 1)).date().isoformat()
    payload["pending_responses"].append({
        "letter_date": today,
        "letter_type": letter_type,
        "expected_response_by": expected_by,
        "follow_up_due": follow_up_due,
    })
    payload["last_contact_at"] = today
    save_supplier(payload)
    return payload


def transition_stage(supplier_id: str, new_stage: str, reason: str = "") -> dict | None:
    """Move relationship stage; appends to history."""
    if new_stage not in VALID_STAGES:
        raise ValueError(f"Invalid stage: {new_stage}. Must be one of {VALID_STAGES}")
    payload = load_supplier(supplier_id)
    if not payload:
        return None
    today = _now_iso()[:10]
    # Close the current stage in history
    history = payload.get("relationship_stage_history", [])
    if history and history[-1].get("until") is None:
        history[-1]["until"] = today
    history.append({"stage": new_stage, "since": today, "until": None, "reason": reason})
    payload["relationship_stage_history"] = history
    payload["relationship_stage"] = new_stage
    save_supplier(payload)
    return payload


def list_pending_responses(within_days: int | None = None) -> list[dict]:
    """
    List all pending responses across all suppliers.
    If within_days set, only return ones where follow_up_due is within that window.
    """
    results = []
    d = cache_dir()
    if not d.exists():
        return results
    today = datetime.now(timezone.utc).date()
    for path in sorted(d.glob("*.json")):
        try:
            with path.open("r", encoding="utf-8") as f:
                payload = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        for pending in payload.get("pending_responses", []):
            try:
                follow_up_due = datetime.fromisoformat(pending["follow_up_due"]).date()
            except (KeyError, ValueError):
                continue
            days_until = (follow_up_due - today).days
            if within_days is not None and days_until > within_days:
                continue
            results.append({
                "supplier_id": payload.get("supplier_id"),
                "company_name": payload.get("company_name"),
                "letter_date": pending.get("letter_date"),
                "letter_type": pending.get("letter_type"),
                "expected_response_by": pending.get("expected_response_by"),
                "follow_up_due": pending.get("follow_up_due"),
                "days_until_follow_up_due": days_until,
            })
    return sorted(results, key=lambda r: r.get("days_until_follow_up_due", 999))


def list_suppliers() -> list[str]:
    d = cache_dir()
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.json"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        suppliers = list_suppliers()
        if not suppliers:
            print("No suppliers cached yet.")
            print(f"Cache dir: {cache_dir()}")
        else:
            print(f"{len(suppliers)} cached supplier(s):")
            for s in suppliers:
                payload = load_supplier(s)
                stage = payload.get("relationship_stage", "?") if payload else "?"
                company = payload.get("company_name", s) if payload else s
                print(f"  - {s}  [{stage}]  {company}")
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: supplier_memory.py show <supplier_id>")
            sys.exit(1)
        payload = load_supplier(sys.argv[2])
        if not payload:
            print(f"No supplier for '{sys.argv[2]}'")
            sys.exit(1)
        print(json.dumps(payload, indent=2))
    elif cmd == "pending":
        within = int(sys.argv[2]) if len(sys.argv) >= 3 else None
        results = list_pending_responses(within_days=within)
        if not results:
            print("No pending responses.")
        else:
            print(f"{len(results)} pending response(s):")
            for r in results:
                marker = "OVERDUE" if r["days_until_follow_up_due"] < 0 else f"in {r['days_until_follow_up_due']} days"
                print(f"  [{marker}]  {r['company_name']}  {r['letter_type']}  (sent {r['letter_date']})")
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: supplier_memory.py [list | show <supplier_id> | pending [within_days]]")
        sys.exit(1)
