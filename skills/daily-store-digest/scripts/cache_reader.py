"""
Cross-skill cache reader for the Daily Store Digest.

Reads from the 4 caches written by skills #11-14 plus the optional forecast-runs cache.
Aggregates them into a unified "Needs Attention Today" action queue with ranking.

Paths (relative to plugin root):
    .cache/reorder_triggers/{date}.json       # skill #12 - inventory stockout flags
    .cache/suppliers/{supplier_id}.json       # skill #11 - per-supplier state
    .cache/bundles/{bundle_id}.json           # skill #13 - bundle suggestions
    .cache/influencers/{handle_slug}.json     # skill #14 - per-influencer state
    .cache/forecast_runs/{date}.json          # skill #12 (optional)
    .cache/sku_to_supplier.json               # skill #12 (used for cross-ref)

Usage:
    from cache_reader import read_all_caches, rank_action_queue

    today = "2026-05-22"
    caches = read_all_caches(today)
    queue = rank_action_queue(caches)
"""

import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path


def find_plugin_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".claude-plugin" / "plugin.json").exists():
            return parent
    raise FileNotFoundError(f"Could not locate plugin root walking up from {here}.")


def _cache_dir(subpath: str) -> Path:
    return find_plugin_root() / ".cache" / subpath


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _parse_date(s: str) -> date | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.split("T")[0]).date()
    except (ValueError, AttributeError):
        return None


def read_inventory_triggers(target_date: str) -> list[dict]:
    """
    Read the most recent reorder triggers file at or before target_date.

    Returns list of triggers with normalized urgency tiers.
    """
    d = _cache_dir("reorder_triggers")
    if not d.exists():
        return []
    target = _parse_date(target_date)
    # Find the most recent file at or before target_date
    candidates = []
    for path in d.glob("*.json"):
        file_date = _parse_date(path.stem)
        if file_date and (target is None or file_date <= target):
            candidates.append((file_date, path))
    if not candidates:
        return []
    candidates.sort(key=lambda x: x[0], reverse=True)
    _, latest_path = candidates[0]
    data = _load_json(latest_path)
    if not data:
        return []
    triggers = data.get("triggers", []) or []
    # Normalize urgency
    normalized = []
    for t in triggers:
        days_to_stockout = t.get("days_until_stockout_p50") or t.get("days_until_stockout")
        if days_to_stockout is None:
            continue
        if days_to_stockout <= 7:
            tier = "critical_immediate"
        elif days_to_stockout <= 14:
            tier = "critical"
        elif days_to_stockout <= 30:
            tier = "plan"
        elif days_to_stockout <= 60:
            tier = "watch"
        else:
            continue
        normalized.append({
            "type": "inventory_reorder",
            "sku": t.get("sku"),
            "product_name": t.get("product_name") or t.get("sku"),
            "current_stock": t.get("current_stock"),
            "days_until_stockout": days_to_stockout,
            "reorder_qty": t.get("reorder_recommended_qty") or t.get("reorder_qty"),
            "supplier_lead_time_days": t.get("supplier_lead_time_days"),
            "urgency_tier": tier,
            "source_file": str(latest_path.name),
        })
    normalized.sort(key=lambda x: x["days_until_stockout"])
    return normalized


def read_supplier_pendings(target_date: str) -> list[dict]:
    """
    Iterate all supplier files; surface pending responses where follow_up_due <= target.
    """
    d = _cache_dir("suppliers")
    if not d.exists():
        return []
    target = _parse_date(target_date) or date.today()
    out = []
    for path in sorted(d.glob("*.json")):
        payload = _load_json(path)
        if not payload:
            continue
        company = payload.get("company_name") or payload.get("supplier_id")
        region = payload.get("region", "")
        for pending in payload.get("pending_responses", []) or []:
            follow_up_due = _parse_date(pending.get("follow_up_due"))
            if not follow_up_due:
                continue
            if follow_up_due > target:
                continue
            days_overdue = (target - follow_up_due).days
            if days_overdue <= 0:
                priority = "due_today"
            elif days_overdue <= 7:
                priority = "routine_overdue"
            elif days_overdue <= 14:
                priority = "notable_overdue"
            else:
                priority = "critical_overdue"
            out.append({
                "type": "supplier_pending",
                "supplier_id": payload.get("supplier_id"),
                "company_name": company,
                "region": region,
                "letter_date": pending.get("letter_date"),
                "letter_type": pending.get("letter_type"),
                "follow_up_due": pending.get("follow_up_due"),
                "days_overdue": days_overdue,
                "priority": priority,
            })
    out.sort(key=lambda x: x["days_overdue"], reverse=True)
    return out


def read_undeployed_bundles(top_n: int = 3) -> list[dict]:
    """
    Iterate all bundle files; surface top N undeployed ranked by composite score.
    """
    d = _cache_dir("bundles")
    if not d.exists():
        return []
    out = []
    for path in sorted(d.glob("*.json")):
        payload = _load_json(path)
        if not payload:
            continue
        if payload.get("deployed") is True:
            continue
        # Also consider deployed if downstream has consumed it (heuristic)
        score = (payload.get("discovery_evidence", {}) or {}).get("composite_score", 0)
        out.append({
            "type": "bundle_undeployed",
            "bundle_id": payload.get("bundle_id"),
            "bundle_name_evocative": payload.get("bundle_name_evocative"),
            "bundle_name_descriptive": payload.get("bundle_name_descriptive"),
            "bundle_type_primary": payload.get("bundle_type_primary"),
            "composite_score": score,
            "recommended_tier": payload.get("recommended_tier"),
            "recommended_price_usd": (
                payload.get("pricing_tiers", {})
                .get(payload.get("recommended_tier", "standard"), {})
                .get("bundle_price_usd")
            ),
            "sku_count": len(payload.get("skus_included", []) or []),
        })
    out.sort(key=lambda x: x.get("composite_score") or 0, reverse=True)
    return out[:top_n]


def read_influencer_pendings(target_date: str) -> list[dict]:
    """
    Iterate all influencer files; surface pending follow-ups due on or before target.
    """
    d = _cache_dir("influencers")
    if not d.exists():
        return []
    target = _parse_date(target_date) or date.today()
    out = []
    stage_to_next_variant = {
        "outreached": "A",
        "follow_up_sent_a": "B",
        "follow_up_sent_b": "C",
        "follow_up_sent_c": None,  # creator is at terminal — no more follow-ups
    }
    for path in sorted(d.glob("*.json")):
        payload = _load_json(path)
        if not payload:
            continue
        # Skip blacklisted / cooling stages
        if payload.get("blacklisted") is True:
            continue
        stage = payload.get("relationship_stage", "")
        if stage in ("agreed", "completed", "declined", "strained", "no_reply_terminal", "blacklisted"):
            continue
        next_variant = stage_to_next_variant.get(stage)
        if next_variant is None:
            continue
        # Find pending response with earliest follow_up_due
        pendings = payload.get("pending_responses", []) or []
        eligible_pendings = []
        for p in pendings:
            fu_due = _parse_date(p.get("follow_up_due"))
            if not fu_due or fu_due > target:
                continue
            eligible_pendings.append((fu_due, p))
        if not eligible_pendings:
            continue
        eligible_pendings.sort(key=lambda x: x[0])
        fu_due, pending = eligible_pendings[0]
        days_overdue = (target - fu_due).days
        primary_platform = next(
            (p for p, info in payload.get("platforms", {}).items() if info.get("primary")),
            list(payload.get("platforms", {}).keys())[0] if payload.get("platforms") else "instagram"
        )
        tier = payload.get("platforms", {}).get(primary_platform, {}).get("tier", "")
        out.append({
            "type": "influencer_follow_up",
            "handle": payload.get("handle"),
            "influencer_id": payload.get("influencer_id"),
            "platform": primary_platform,
            "tier": tier,
            "current_stage": stage,
            "next_variant": next_variant,
            "outreach_date": pending.get("outreach_date"),
            "follow_up_due": pending.get("follow_up_due"),
            "days_overdue": days_overdue,
        })
    out.sort(key=lambda x: (x["days_overdue"], x.get("tier", "")), reverse=True)
    return out


def read_forecast_method_changes(target_date: str) -> list[dict]:
    """
    Optional: surface recent forecast method changes from the last forecast run.
    Returns empty list if no recent run or no method changes.
    """
    d = _cache_dir("forecast_runs")
    if not d.exists():
        return []
    target = _parse_date(target_date) or date.today()
    candidates = []
    for path in d.glob("*.json"):
        file_date = _parse_date(path.stem)
        if file_date and (target - file_date).days <= 1:
            candidates.append((file_date, path))
    if not candidates:
        return []
    candidates.sort(key=lambda x: x[0], reverse=True)
    _, latest_path = candidates[0]
    data = _load_json(latest_path)
    if not data:
        return []
    return data.get("method_changes", []) or []


def read_all_caches(target_date: str) -> dict:
    """Read all 4 (+1 optional) caches; return structured rollup."""
    return {
        "inventory": read_inventory_triggers(target_date),
        "suppliers": read_supplier_pendings(target_date),
        "bundles": read_undeployed_bundles(),
        "influencers": read_influencer_pendings(target_date),
        "forecast_method_changes": read_forecast_method_changes(target_date),
    }


def rank_action_queue(caches: dict, max_actions: int = 5) -> list[dict]:
    """
    Rank items from all caches into a unified action queue.

    Ranking priority (highest first):
      1. critical_immediate inventory (stockout <=7d)
      2. critical_overdue supplier (overdue >14d)
      3. critical inventory (stockout 8-14d)
      4. influencer Variant C
      5. high-score undeployed bundles (score >=80)
      6. notable_overdue supplier (8-14d)
      7. influencer Variant A on macro (high-value follow-ups first)
      8. influencer Variant A on mid_tier
      9. influencer Variant A on micro/nano
      10. plan inventory (stockout 15-30d)
      11. routine_overdue supplier
      12. influencer Variant B
      13. mid-score bundles
    """
    actions = []

    inv = caches.get("inventory", [])
    sup = caches.get("suppliers", [])
    bun = caches.get("bundles", [])
    inf = caches.get("influencers", [])

    # 1. critical immediate inventory
    for t in inv:
        if t["urgency_tier"] == "critical_immediate":
            actions.append((1, _inventory_action(t)))

    # 2. critical overdue supplier
    for s in sup:
        if s["priority"] == "critical_overdue":
            actions.append((2, _supplier_action(s)))

    # 3. critical inventory (14d)
    for t in inv:
        if t["urgency_tier"] == "critical":
            actions.append((3, _inventory_action(t)))

    # 4. influencer Variant C
    for i in inf:
        if i["next_variant"] == "C":
            actions.append((4, _influencer_action(i)))

    # 5. high-score undeployed bundles
    for b in bun:
        if (b.get("composite_score") or 0) >= 80:
            actions.append((5, _bundle_action(b)))

    # 6. notable_overdue supplier
    for s in sup:
        if s["priority"] == "notable_overdue":
            actions.append((6, _supplier_action(s)))

    # 7/8/9. influencer Variant A by tier
    tier_rank = {"macro": 7, "mid_tier": 8, "micro": 9, "nano": 9}
    for i in inf:
        if i["next_variant"] == "A":
            actions.append((tier_rank.get(i.get("tier", "micro"), 9), _influencer_action(i)))

    # 10. plan inventory
    for t in inv:
        if t["urgency_tier"] == "plan":
            actions.append((10, _inventory_action(t)))

    # 11. routine_overdue supplier
    for s in sup:
        if s["priority"] in ("routine_overdue", "due_today"):
            actions.append((11, _supplier_action(s)))

    # 12. influencer Variant B
    for i in inf:
        if i["next_variant"] == "B":
            actions.append((12, _influencer_action(i)))

    # 13. mid-score bundles
    for b in bun:
        score = b.get("composite_score") or 0
        if 60 <= score < 80:
            actions.append((13, _bundle_action(b)))

    actions.sort(key=lambda x: x[0])
    return [a for _, a in actions[:max_actions]]


def _inventory_action(t: dict) -> dict:
    return {
        "kind": "inventory",
        "urgency": t["urgency_tier"],
        "description": (
            f"Reorder {t['product_name']} — stocks out in {t['days_until_stockout']} days "
            f"at current velocity; supplier lead time {t.get('supplier_lead_time_days', 'unknown')} days"
        ),
        "skill_to_use": "supplier-negotiation-assistant",
        "skill_prompt_hint": f"draft reorder letter for {t['product_name']} ({t.get('reorder_qty', 'recommended qty')} units)",
        "source": t,
    }


def _supplier_action(s: dict) -> dict:
    return {
        "kind": "supplier",
        "urgency": s["priority"],
        "description": (
            f"Follow up with {s['company_name']} on {s.get('letter_type', 'pending request')} — "
            f"overdue {s['days_overdue']} days"
        ),
        "skill_to_use": "supplier-negotiation-assistant",
        "skill_prompt_hint": f"send follow-up to {s['company_name']}",
        "source": s,
    }


def _bundle_action(b: dict) -> dict:
    return {
        "kind": "bundle",
        "urgency": "opportunity",
        "description": (
            f"Launch {b.get('bundle_name_evocative') or b.get('bundle_name_descriptive')} bundle — "
            f"composite score {b.get('composite_score', 0):.1f}/100; "
            f"price ${(b.get('recommended_price_usd') or 0):.2f}"
        ),
        "skill_to_use": "landing-page-copywriter",
        "skill_prompt_hint": f"generate landing page for bundle {b.get('bundle_id')}",
        "source": b,
    }


def _influencer_action(i: dict) -> dict:
    return {
        "kind": "influencer",
        "urgency": f"variant_{i['next_variant'].lower()}",
        "description": (
            f"Send Variant {i['next_variant']} follow-up to {i['handle']} "
            f"({i.get('platform', '')}, {i.get('tier', '')}-tier) — "
            f"original outreach {i.get('outreach_date')}, "
            f"follow-up due {i.get('follow_up_due')} ({'overdue ' + str(i['days_overdue']) + 'd' if i['days_overdue'] > 0 else 'today'})"
        ),
        "skill_to_use": "influencer-outreach-pro",
        "skill_prompt_hint": f"follow up with {i['handle']} (variant {i['next_variant']})",
        "source": i,
    }


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    print(f"Reading caches as of: {target}")
    caches = read_all_caches(target)
    for key, items in caches.items():
        print(f"  {key}: {len(items)} items")
    queue = rank_action_queue(caches)
    print(f"\nRanked action queue (top {len(queue)}):")
    for i, a in enumerate(queue, 1):
        print(f"  {i}. [{a['kind']}] {a['description']}")
