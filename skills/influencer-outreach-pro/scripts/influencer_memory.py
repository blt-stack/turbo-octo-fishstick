"""
Per-influencer relationship state cache reader/writer.

Skill #14 (Influencer Outreach Pro) is the primary writer. The cache turns
each new outreach into part of an ongoing relationship rather than cold contact.

Path convention:
    ~/.the-ecommerce-seller/cache/influencers/{handle-slug}.json

Schema documented in templates/influencer-memory.md.

Usage:
    from influencer_memory import (
        load_influencer,
        save_influencer,
        upsert_influencer,
        log_outreach,
        transition_stage,
        list_pending_responses,
        check_cooling_period,
    )
"""

import os
import shutil
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


CACHE_SUBDIR = "cache/influencers"

VALID_STAGES = {
    "new", "outreached",
    "follow_up_sent_a", "follow_up_sent_b", "follow_up_sent_c",
    "no_reply_terminal",
    "responded", "negotiating", "agreed", "completed",
    "declined", "strained", "blacklisted",
}

# How many days to wait for response per tier
RESPONSE_WINDOWS_DAYS = {
    "nano": 7,
    "micro": 14,
    "mid_tier": 21,
    "macro": 45,
}

# Cooling periods before re-outreach after specific stages
COOLING_PERIODS_DAYS = {
    "declined": 180,
    "no_reply_terminal": 90,
    "strained": 365,
}


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
    text = (text or "").lower().strip().lstrip("@")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "unnamed-influencer"


def handle_to_slug(handle: str) -> str:
    return slugify(handle)


def cache_path_for(handle: str) -> Path:
    return cache_dir() / f"{handle_to_slug(handle)}.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _empty_payload(handle: str, primary_platform: str, follower_count: int, tier: str) -> dict:
    today = _now_iso()[:10]
    return {
        "influencer_id": handle_to_slug(handle),
        "handle": handle,
        "display_name": "",
        "real_name": "",
        "platforms": {
            primary_platform: {
                "handle": handle,
                "follower_count": follower_count,
                "engagement_rate": None,
                "tier": tier,
                "primary": True,
            }
        },
        "content_themes": [],
        "voice_register": "",
        "niche": "",
        "audience_demographic_guess": "",
        "language_preference": "english",
        "geography": "",
        "time_zone": "",
        "best_contact_method": primary_platform + "_dm",
        "email_known": "",
        "manager_email_known": "",
        "first_contact_date": today,
        "last_contact_at": today,
        "relationship_stage": "new",
        "relationship_stage_history": [
            {"stage": "new", "since": today, "until": None, "reason": "First record"}
        ],
        "outreach_history": [],
        "pending_responses": [],
        "post_context_history": [],
        "deliverables_history": [],
        "payment_history": {
            "total_gifted_value_usd": 0,
            "total_cash_paid_usd": 0,
            "total_affiliate_paid_usd": 0,
        },
        "exclusivity_windows": [],
        "blacklisted": False,
        "notes": [],
        "alignment_score": None,
        "alignment_notes": "",
        "last_updated": _now_iso(),
    }


def load_influencer(handle: str) -> dict | None:
    path = cache_path_for(handle)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[influencer_memory] Failed to load {path}: {exc}", file=sys.stderr)
        return None


def save_influencer(payload: dict) -> Path:
    handle = payload.get("handle") or payload.get("influencer_id")
    if not handle:
        raise ValueError("payload missing handle / influencer_id")
    path = cache_path_for(handle)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload["last_updated"] = _now_iso()

    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return path


def upsert_influencer(
    handle: str,
    primary_platform: str = "instagram",
    follower_count: int = 0,
    tier: str = "nano",
    extra_fields: dict | None = None,
) -> dict:
    payload = load_influencer(handle)
    if not payload:
        payload = _empty_payload(handle, primary_platform, follower_count, tier)
    if extra_fields:
        for key, value in extra_fields.items():
            if isinstance(value, dict) and isinstance(payload.get(key), dict):
                payload[key].update(value)
            else:
                payload[key] = value
    save_influencer(payload)
    return payload


def log_outreach(
    handle: str,
    channel: str,
    outreach_type: str,
    framework_offered: str,
    product_offered: str,
    summary: str,
    rate_offered_usd: float = 0,
    skill_run_id: str | None = None,
) -> dict | None:
    payload = load_influencer(handle)
    if not payload:
        return None

    today = _now_iso()[:10]
    primary_platform = next(
        (p for p, info in payload.get("platforms", {}).items() if info.get("primary")),
        "instagram"
    )
    tier_at_time = (payload.get("platforms", {}).get(primary_platform, {}).get("tier", "nano"))

    payload["outreach_history"].append({
        "date": today,
        "channel": channel,
        "outreach_type": outreach_type,
        "platform": primary_platform,
        "tier_at_time": tier_at_time,
        "framework_offered": framework_offered,
        "rate_offered_usd": rate_offered_usd,
        "product_offered": product_offered,
        "summary": summary,
        "response_status": "no_reply",
        "skill_run_id": skill_run_id or _now_iso(),
    })

    # Set pending response with expected window per tier
    response_days = RESPONSE_WINDOWS_DAYS.get(tier_at_time, 14)
    expected_by = (datetime.now(timezone.utc) + timedelta(days=response_days)).date().isoformat()
    follow_up_due = (datetime.now(timezone.utc) + timedelta(days=response_days + 1)).date().isoformat()
    payload["pending_responses"].append({
        "outreach_date": today,
        "outreach_type": outreach_type,
        "expected_response_by": expected_by,
        "follow_up_due": follow_up_due,
    })

    payload["last_contact_at"] = today
    save_influencer(payload)
    return payload


def transition_stage(handle: str, new_stage: str, reason: str = "") -> dict | None:
    if new_stage not in VALID_STAGES:
        raise ValueError(f"Invalid stage: {new_stage}. Must be one of {VALID_STAGES}")
    payload = load_influencer(handle)
    if not payload:
        return None
    today = _now_iso()[:10]
    history = payload.get("relationship_stage_history", [])
    if history and history[-1].get("until") is None:
        history[-1]["until"] = today
    history.append({"stage": new_stage, "since": today, "until": None, "reason": reason})
    payload["relationship_stage_history"] = history
    payload["relationship_stage"] = new_stage
    save_influencer(payload)
    return payload


def check_cooling_period(handle: str) -> dict:
    """
    Returns {"ok_to_outreach": bool, "reason": str, "cooled_off_on": date_str|None}
    """
    payload = load_influencer(handle)
    if not payload:
        return {"ok_to_outreach": True, "reason": "No prior contact", "cooled_off_on": None}

    if payload.get("blacklisted"):
        return {"ok_to_outreach": False, "reason": "Blacklisted by buyer", "cooled_off_on": None}

    current_stage = payload.get("relationship_stage", "new")
    if current_stage not in COOLING_PERIODS_DAYS:
        return {"ok_to_outreach": True, "reason": "No cooling period for current stage", "cooled_off_on": None}

    cooling_days = COOLING_PERIODS_DAYS[current_stage]
    history = payload.get("relationship_stage_history", [])
    stage_entered = None
    for h in reversed(history):
        if h.get("stage") == current_stage:
            stage_entered = h.get("since")
            break
    if not stage_entered:
        return {"ok_to_outreach": True, "reason": "No record of stage entry", "cooled_off_on": None}

    try:
        entered = datetime.fromisoformat(stage_entered).date()
    except ValueError:
        return {"ok_to_outreach": True, "reason": "Could not parse stage date", "cooled_off_on": None}

    cooled_off_date = entered + timedelta(days=cooling_days)
    today = datetime.now(timezone.utc).date()
    if today < cooled_off_date:
        days_remaining = (cooled_off_date - today).days
        return {
            "ok_to_outreach": False,
            "reason": f"Cooling period until {cooled_off_date.isoformat()} ({days_remaining} days remaining); current stage: {current_stage}",
            "cooled_off_on": cooled_off_date.isoformat(),
        }
    return {"ok_to_outreach": True, "reason": "Cooling period expired", "cooled_off_on": cooled_off_date.isoformat()}


def list_pending_responses() -> list[dict]:
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
            results.append({
                "influencer_id": payload.get("influencer_id"),
                "handle": payload.get("handle"),
                "outreach_date": pending.get("outreach_date"),
                "outreach_type": pending.get("outreach_type"),
                "follow_up_due": pending.get("follow_up_due"),
                "days_until_follow_up_due": days_until,
            })
    return sorted(results, key=lambda r: r.get("days_until_follow_up_due", 999))


def list_influencers() -> list[str]:
    d = cache_dir()
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.json"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        influencers = list_influencers()
        if not influencers:
            print("No influencers cached yet.")
            print(f"Cache dir: {cache_dir()}")
        else:
            print(f"{len(influencers)} cached influencer(s):")
            for i in influencers:
                payload = load_influencer(i)
                stage = payload.get("relationship_stage", "?") if payload else "?"
                handle = payload.get("handle", i) if payload else i
                print(f"  - {i:30s} [{stage:25s}]  {handle}")
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: influencer_memory.py show <handle>")
            sys.exit(1)
        payload = load_influencer(sys.argv[2])
        if not payload:
            print(f"No influencer for '{sys.argv[2]}'")
            sys.exit(1)
        print(json.dumps(payload, indent=2))
    elif cmd == "pending":
        results = list_pending_responses()
        if not results:
            print("No pending responses.")
        else:
            print(f"{len(results)} pending response(s):")
            for r in results:
                marker = "OVERDUE" if r["days_until_follow_up_due"] < 0 else f"in {r['days_until_follow_up_due']} days"
                print(f"  [{marker}]  {r['handle']}  {r['outreach_type']}  (sent {r['outreach_date']})")
    elif cmd == "blacklist":
        if len(sys.argv) < 3:
            print("Usage: influencer_memory.py blacklist <handle>")
            sys.exit(1)
        upsert_influencer(sys.argv[2], extra_fields={"blacklisted": True})
        print(f"Blacklisted {sys.argv[2]}")
    elif cmd == "cool":
        if len(sys.argv) < 3:
            print("Usage: influencer_memory.py cool <handle>")
            sys.exit(1)
        result = check_cooling_period(sys.argv[2])
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: influencer_memory.py [list | show <handle> | pending | blacklist <handle> | cool <handle>]")
        sys.exit(1)
