# Supplier Memory — Per-Supplier Relationship State

Every letter drafted by this skill pulls from and writes to a per-supplier JSON cache at:
```
<plugin-root>/.cache/suppliers/{supplier-id}.json
```

This cache turns the skill from a letter generator into a relationship-aware CRM. The third email to a supplier reads like a continuing relationship because the skill remembers the prior asks, the supplier's preferences, the relationship stage, and the open negotiations.

## Schema

```json
{
  "supplier_id": "shenzhen-stoneworks-ms-chen",
  "company_name": "Shenzhen Stoneworks Co., Ltd.",
  "primary_contact": {
    "name": "Cindy Chen",
    "honorific": "Ms.",
    "role": "Sales Manager",
    "preferred_address": "Ms. Chen",
    "email": "cindy.chen@shenzhenstoneworks.com",
    "alibaba_username": "shenzhenstoneworks_sales",
    "phone": "+86 ...",
    "whatsapp": ""
  },
  "region": "china",
  "country": "China",
  "city": "Shenzhen",
  "language_preference": "english_with_chinese_courtesy",
  "first_contact_date": "2025-10-15",
  "relationship_stage": "established",
  "relationship_stage_history": [
    {"stage": "new", "since": "2025-10-15", "until": "2025-12-02", "reason": "First contact"},
    {"stage": "established", "since": "2025-12-02", "until": null, "reason": "Third successful order delivered"}
  ],
  "product_lines_sourced": ["River Stone Pour-Over", "Studio Glaze Bowl"],
  "known_moqs": {
    "River Stone Pour-Over": {"moq": 300, "first_quoted_at_moq": 1000, "negotiated_down_via": "MOQ reduction letter Mar 2026"},
    "Studio Glaze Bowl": {"moq": 500}
  },
  "known_pricing_tiers": {
    "River Stone Pour-Over": [
      {"tier_qty": 100, "unit_price_usd": 4.80},
      {"tier_qty": 500, "unit_price_usd": 4.40},
      {"tier_qty": 1000, "unit_price_usd": 4.20},
      {"tier_qty": 2500, "unit_price_usd": 3.95},
      {"tier_qty": 5000, "unit_price_usd": 3.70}
    ]
  },
  "payment_terms_in_force": {
    "structure": "30/70 TT",
    "details": "30% deposit, 70% balance before shipping",
    "moved_to_current_on": "2026-01-10",
    "prior": "100% upfront"
  },
  "letters_sent": [
    {
      "date": "2025-10-15",
      "type": "sample_request",
      "summary": "First contact; requested 3 samples of RS Pour-Over",
      "outcome": "Samples arrived 2025-10-28; quality good",
      "response_time_days": 2
    },
    {
      "date": "2025-11-08",
      "type": "moq_reduction",
      "summary": "Requested 300 units instead of 1000 MOQ; offered to pay at 100-tier price",
      "outcome": "Accepted at 300 units @ $4.80",
      "response_time_days": 3
    },
    {
      "date": "2026-03-14",
      "type": "dispute",
      "summary": "Glaze cracking on 14% of order #5118",
      "outcome": "Pending response",
      "response_time_days": null
    }
  ],
  "pending_responses": [
    {
      "letter_date": "2026-03-14",
      "letter_type": "dispute",
      "expected_response_by": "2026-03-21",
      "follow_up_due": "2026-03-22"
    }
  ],
  "response_time_pattern": {
    "average_days": 2.3,
    "fastest_days": 1,
    "slowest_days": 5,
    "samples_n": 8
  },
  "communication_preferences": {
    "primary_channel": "email",
    "fallback_channel": "alibaba_trademessenger",
    "time_zone": "Asia/Shanghai",
    "business_hours_local": "9:00 - 18:00",
    "holidays_observed": ["lunar_new_year", "qingming", "labor_day", "dragon_boat", "mid_autumn", "national_day_golden_week"]
  },
  "notes": [
    {"date": "2025-12-10", "note": "Cindy mentioned her team works Saturday mornings"},
    {"date": "2026-01-15", "note": "Factory expanding new line in Q2; ask about capacity in March"},
    {"date": "2026-02-01", "note": "Lunar New Year shutdown Feb 8-17 2026"}
  ],
  "last_contact_at": "2026-03-14",
  "last_updated": "2026-03-14T16:30:00Z"
}
```

## How the skill uses the memory

### On every new letter

1. Look up supplier_id from buyer's input
2. If exists, load the cache
3. Use `relationship_stage` to pick tone (new / established / strained)
4. Use `region` + `country` + `language_preference` to pick regional playbook
5. Use `known_moqs` and `known_pricing_tiers` to inform the ask (e.g., when asking for a new pricing tier, reference the existing tiers)
6. Use `letters_sent` to avoid repeating asks or to chain follow-ups
7. Use `pending_responses` to warn the buyer if they're asking for something else while a prior letter is unanswered
8. Use `communication_preferences` to recommend channel (email vs. TradeMessenger)
9. Use `notes` for personal touches ("hope you had a good Lunar New Year")
10. Use `response_time_pattern` to set follow-up timing expectations

### On every letter send

1. Append to `letters_sent` with date, type, summary
2. Update `last_contact_at`
3. Add to `pending_responses` with expected response window
4. If the letter is a stage-shifting type (dispute → strained, first-order-success → established), update `relationship_stage_history`
5. Capture any new info (new MOQ negotiated, new pricing tier confirmed) into known_moqs / known_pricing_tiers
6. Atomic write

## Relationship stage transitions

The skill tracks stage based on letter outcomes:

| Trigger | Transition |
|---|---|
| First letter to a new supplier | Creates supplier_id; sets stage to `new` |
| First order delivered successfully | `new` → `established` |
| Third consecutive on-time + on-quality order | Reinforces `established` |
| Dispute letter sent | `established` → `strained` (pending response) |
| Dispute resolved positively | `strained` → `established` |
| Dispute unresolved + 30 days passed | `strained` confirmed; flag for buyer review |
| 6+ months without contact | `dormant` (sub-stage) — skill warns of relationship cooling |

The skill explains transitions in the .docx output so the buyer can override.

## Generating supplier_id

The skill creates a slug from company name + primary contact for collision resistance:

```python
def supplier_id(company_name: str, contact_name: str | None = None) -> str:
    base = slugify(company_name)
    if contact_name:
        base = f"{base}-{slugify(contact_name)}"
    return base[:80]
```

Example: `"Shenzhen Stoneworks Co., Ltd."` + `"Cindy Chen"` → `"shenzhen-stoneworks-co-ltd-cindy-chen"`

## Multi-contact suppliers

Some suppliers have multiple contacts (sales manager, QC, owner). The skill supports:

- Primary contact in `primary_contact` field
- Additional contacts in optional `other_contacts` array
- Each letter notes which contact it was sent to

If the buyer writes to a different contact at the same supplier, the skill notes the contact in the letter log without creating a separate supplier file.

## Privacy + portability

The supplier memory file is local to the plugin and never sent over the wire. The buyer can:

- Inspect any file directly at `<plugin-root>/.cache/suppliers/`
- Edit notes manually (the skill respects manual edits)
- Export the supplier list as a CSV for backup or migration
- Delete a supplier file (the skill recreates if a new letter is drafted to that supplier)

## Edge cases

- **Supplier changes contact person**: skill recommends keeping the supplier_id but updating `primary_contact` and adding a note about the transition
- **Supplier rebrands / changes company name**: skill recommends keeping the supplier_id (since it's slug-based on the original) and adding a note
- **Two contacts at the same supplier disagree on terms**: skill notes both in the file; buyer decides which is canonical
- **Buyer realizes a supplier is duplicate in the cache** (one ID for the company name, one for an alias): skill provides a `merge` CLI command on the `supplier_memory.py` script
- **Supplier ghosts after a dispute**: skill marks `relationship_stage: "strained"` with `outcome: "no_response"` after 30 days; recommends walk-away letter or escalation

## Use across other skills

While the primary writer is this skill, the supplier memory is theoretically readable by other skills:

- **Inventory Forecaster (skill #12)** can read `known_moqs` + `payment_terms` + `lead_time` from supplier memory to plan reorders
- **Bundle Builder (skill #13)** can check which suppliers are reliable (no recent disputes) before proposing bundles dependent on combined SKUs
- **Product Description Writer / SEO Optimizer** can reference origin country in product copy when it adds value

The supplier memory file is opt-in for downstream skills — they read it if useful, ignore it otherwise.
