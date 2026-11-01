# Reorder Triggers — Handoff Cache to Skill #11

When the forecast identifies SKUs needing reorder within the next 30 days, the skill writes those decisions to a shared cache that the Supplier Negotiation Assistant (skill #11) reads.

## Cache location

```
~/.the-ecommerce-seller/cache/reorder_triggers/{YYYY-MM-DD}.json
```

One file per forecast run date. The skill appends new triggers to today's file if multiple forecast runs happen on the same day; otherwise creates a new file.

## Schema

```json
{
  "forecast_run_at": "2026-04-15T10:30:00Z",
  "forecast_run_id": "fc-2026-04-15-1030",
  "scope": "full_catalog",
  "triggers": [
    {
      "sku": "RS-POUR-OVER-001",
      "product_name": "River Stone Pour-Over",
      "supplier_id": "shenzhen-stoneworks-co-ltd-cindy-chen",
      "urgency": "urgent",
      "trigger_reason": "Days until stockout (18) < lead time (45) + safety stock (14)",
      "current_on_hand": 220,
      "velocity_p50_units_per_day": 12.2,
      "velocity_p90_units_per_day": 16.8,
      "days_until_stockout_p50": 18,
      "days_until_stockout_p90": 13,
      "lead_time_days": 45,
      "transit_days": 30,
      "transit_mode": "sea_freight",
      "moq": 1500,
      "current_unit_price_usd": 4.20,
      "payment_terms_in_force": "30_70_tt_before_shipping",
      "recommended_reorder_quantity": 1500,
      "recommended_deposit_date": "2026-04-15",
      "expected_ship_date": "2026-05-30",
      "expected_arrive_date": "2026-06-29",
      "days_short_before_arrival": 57,
      "estimated_reorder_cost_usd": 6300,
      "notes": "Lead time exceeds days-until-stockout — expedite via air freight or accept partial stockout. Cost-of-stockout estimate: $X (vs. air-freight expedite cost $Y).",
      "expedite_suggested": true,
      "consumed_by_skill_11": false,
      "consumed_at": null
    },
    ...
  ],
  "_meta": {
    "schema_version": 1,
    "writer": "inventory-forecaster",
    "total_triggers": 12,
    "urgency_distribution": {
      "stockout_imminent": 1,
      "urgent": 5,
      "reorder_soon": 6
    }
  }
}
```

## Urgency levels

Four urgency levels (lowest to highest):

| Urgency | Definition | Action |
|---|---|---|
| `healthy` | days_until_stockout > (lead_time + safety_stock + reorder_window) | No trigger written |
| `reorder_soon` | days_until_stockout in (lead_time + safety_stock, lead_time + safety_stock + reorder_window) | Reorder within next 7-14 days |
| `urgent` | days_until_stockout in (lead_time, lead_time + safety_stock) | Reorder today |
| `stockout_imminent` | days_until_stockout < lead_time | Already late — expedite or accept stockout |

Only `reorder_soon`, `urgent`, and `stockout_imminent` get triggers written.

## Consumed flag

When skill #11 reads a trigger and drafts a reorder letter, it updates the trigger with:

```json
"consumed_by_skill_11": true,
"consumed_at": "2026-04-15T11:45:00Z",
"draft_letter_path": "C:\Users\...\Desktop\AI Black Magic\supplier_letter_shenzhen_stoneworks_20260415.docx"
```

The forecaster (this skill) reads `consumed_by_skill_11` on subsequent runs to avoid re-flagging the same trigger. Once consumed, the trigger persists in the cache as historical record.

## Forecast run lineage

Each trigger references its parent forecast run via `forecast_run_id`. If the buyer re-runs the forecast and a previously-triggered SKU drops below urgency (e.g., demand slowed, on-hand replenished), the new forecast writes an updated state without re-triggering.

## Reading the cache (from skill #11)

When skill #11 starts up, it can scan `~/.the-ecommerce-seller/cache/reorder_triggers/`:

```python
from pathlib import Path
import json

def get_pending_triggers(plugin_root: Path, days_back: int = 14) -> list[dict]:
    """Read all unconsumed triggers from the last N days."""
    triggers_dir = plugin_root / "~/.the-ecommerce-seller/cache" / "reorder_triggers"
    if not triggers_dir.exists():
        return []
    pending = []
    for path in sorted(triggers_dir.glob("*.json")):
        with path.open() as f:
            data = json.load(f)
        for trigger in data.get("triggers", []):
            if not trigger.get("consumed_by_skill_11"):
                pending.append(trigger)
    return pending
```

Skill #11 can then prompt the buyer:
> "The inventory forecaster identified 12 SKUs needing reorder. Want me to draft reorder letters to the suppliers now?"

## Trigger cleanup

The skill auto-prunes old triggers:
- Consumed triggers older than 90 days are archived to `~/.the-ecommerce-seller/cache/reorder_triggers/archive/`
- Unconsumed triggers older than 30 days are flagged for buyer review (likely abandoned or superseded)

## Multi-supplier triggers

When a SKU has split allocation across multiple suppliers, the skill writes one trigger per supplier:

```json
"triggers": [
  {
    "sku": "RS-POUR-OVER-001",
    "supplier_id": "shenzhen-stoneworks",
    "recommended_reorder_quantity": 1050,  // 70% of 1500
    "split_allocation_fraction": 0.7,
    ...
  },
  {
    "sku": "RS-POUR-OVER-001",
    "supplier_id": "jingdezhen-ceramics",
    "recommended_reorder_quantity": 450,  // 30% of 1500
    "split_allocation_fraction": 0.3,
    ...
  }
]
```

Skill #11 drafts separate letters per supplier (different region, different stage, different MOQ considerations).

## Suppressed triggers

The buyer can suppress triggers for specific SKUs:

```json
"inventory_forecasting": {
  "suppress_triggers_for_skus": ["DROP-SHIP-001", "DISCONTINUED-XYZ"],
  "suppress_triggers_for_suppliers": ["supplier-on-pause"]
}
```

Useful when:
- A supplier is on temporary pause (e.g., factory holiday closure)
- A SKU is being discontinued (don't reorder)
- A SKU is being sourced from a new supplier this run (skip during transition)

## What happens if no downstream consumer

If skill #11 isn't installed or isn't being used, the triggers file still gets written. The buyer can:
- Read the file directly (it's JSON; legible)
- Use the .xlsx Reorder Calendar sheet (which contains the same data, prettier)
- Ignore the cache; the .xlsx is the primary deliverable

The cache write is cheap and idempotent — no harm if unused.

## Trigger audit

Each forecast run writes a summary entry to `~/.the-ecommerce-seller/cache/reorder_triggers/audit.log`:

```
2026-04-15  full_catalog  12 triggers (1 imminent, 5 urgent, 6 soon)  ${total_value_at_risk}
2026-04-22  full_catalog  9 triggers (0 imminent, 3 urgent, 6 soon)   $4,580
2026-04-29  single_sku    1 trigger (urgent, RS-POUR-OVER-001)        $6,300
```

The audit lets the buyer see whether the catalog's reorder pipeline is healthy over time.
