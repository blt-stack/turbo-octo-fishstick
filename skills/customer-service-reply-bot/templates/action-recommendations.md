# Action Recommendations — Decision Framework

Every ticket gets a recommended action alongside the reply. The action is the business decision; the reply is the communication. They go together, but they're separable — the buyer can adopt the reply text and a different action.

## The action menu

| Action | Code | When |
|---|---|---|
| No action needed | `no_action` | Pre-purchase Q&A, info request, customer satisfied |
| Resend tracking / status | `info_update` | Customer wants order status; no problem to fix |
| Issue refund (partial) | `refund_partial` | Minor defect customer keeps, late shipping (small comp) |
| Issue refund (full) | `refund_full` | Defective + customer doesn't want replacement; brand-fault major issue |
| Issue refund (full) + store credit | `refund_full_plus_credit` | Brand-fault + relationship-saving extra (5-20 credit) |
| Issue refund (full) + free reship | `refund_full_plus_reship` | Brand error twice; lost order + replacement |
| Reship the product | `reship` | Lost in transit, wrong item shipped, defect within window — no refund, just replace |
| Reship + small credit | `reship_plus_credit` | Defect or shipping issue with goodwill comp |
| Honor return / process exchange | `process_return` | Standard return within window |
| Decline gracefully (with reason) | `decline` | Outside return window, customer error not brand error, policy violation |
| Escalate to founder / owner | `escalate_founder` | High-LTV customer, public-complaint risk, unusual situation, customer named the founder |
| Add to BIS waitlist | `add_to_bis` | Stock question, product currently out |

The skill picks ONE action per ticket and provides a rationale.

---

## Decision framework

### Step 1: Is the brand at fault?

| Answer | Default action lean |
|---|---|
| Yes (defect, ship-from-wrong-warehouse, wrong item) | Refund + replacement, credit for inconvenience |
| Partially (shipping delay where carrier dropped the ball but brand chose the carrier) | Credit + escalation commitment |
| No (customer changed mind, didn't read sizing chart) | Honor policy fairly, no extra goodwill needed |

### Step 2: What's the customer relationship worth?

| Customer LTV | Treatment lean |
|---|---|
| New customer / first order | Slightly more generous (relationship-building) |
| Repeat customer (2-5 orders) | Standard policy + small goodwill |
| High-LTV customer (5+ orders or >$500 lifetime) | Generous + escalate to founder for personal touch |
| One-time low-value customer | Standard policy, no special treatment |
| Customer with prior CS issues | Investigate before being generous (may be high-need vs the brand-at-fault) |

### Step 3: What's the public-complaint risk?

If the ticket includes any of:
- Mentions of Trustpilot, BBB, Google, social media
- Threats to "tell people about this"
- cc'ing journalists / named brand people
- Threats of chargeback

→ Escalate to founder + over-deliver on the action (full refund + replacement + extra credit). The risk-adjusted cost of NOT over-delivering far exceeds the cost of doing it.

### Step 4: What does the resolution cost the brand?

For brand-at-fault situations, the math:

| Cost tier | Typical action |
|---|---|
| Under $20 | Just absorb (refund/credit/reship) — investigating is more expensive than the resolution |
| $20-100 | Standard action; document for pattern-tracking |
| $100-500 | Resolve + flag for internal review (was it a one-off or a pattern?) |
| Over $500 | Escalate to founder; resolution + supplier/carrier discussion |

---

## Common decision patterns by sub-type

### Shipping delays

| Days late | Action |
|---|---|
| 0-2 | Info update, no comp |
| 3-7 | Small store credit ($5-15) + escalation commitment |
| 7-14 | Full refund OR reship at brand's expense + $10-20 credit |
| 14+ | Full refund + escalate to founder + carrier complaint |

### Shipping lost in transit

- Default: reship immediately (don't wait for claim investigation)
- For high-value items (>$200): reship + file claim simultaneously to recover cost
- Repeat lost-in-transit from same customer (3rd in 12 months): investigate before reshipping

### Defects on arrival (BOA)

- Default: free replacement (no return required) + small credit
- For valuable items: replacement + photo request (for insurance, after committing)
- Same-product 3+ BOA reports in 30 days: flag systemic issue

### Defect after use within warranty

- Replacement at no charge
- Photo request for QC purposes (after committing to the fix)

### Defect after warranty

- Discount on replacement (not free) + acknowledge the disappointment
- For very-recent expirations (within 30 days): often free as goodwill

### Customer changed mind, within return window, unused

- Standard return per policy
- Refund within 5 business days of receipt

### Customer changed mind, within window, item used/opened

- Store credit instead of refund (or partial refund)
- Depends on category (cosmetics/intimate/perishable: stricter)

### Customer changed mind, OUTSIDE return window

- Default: decline gracefully + offer store credit at reduced value (e.g., 80%)
- For high-LTV customers: full store credit
- For 90+ days past: decline + offer discount on future order

### Pre-purchase question

- No action needed — reply only

---

## Rationale format

The skill outputs the action recommendation with a one-line rationale. Patterns:

**For straightforward actions:**
```
Recommended action: Issue full refund
Rationale: Customer's order arrived broken — brand fault. Refund + ship a
replacement at no charge protects the relationship and is the obvious
right call.
Estimated cost: $48 (refund) + $4 (replacement shipping) = $52
```

**For credit-additions:**
```
Recommended action: Reship + $10 store credit
Rationale: Product arrived defective. Reship fixes the immediate issue; the
$10 credit acknowledges the 7-day delay caused by needing to reship.
Estimated cost: $0 (replacement product COGS) + $4 (shipping) + $10 (credit
if used) = ~$14 expected
```

**For escalations:**
```
Recommended action: Escalate to founder for personal reply
Rationale: Customer has $1,840 LTV across 8 orders and is threatening a
Trustpilot review. Personal founder response + full refund + free
replacement + 25% off next order protects the LTV and the public
reputation.
Estimated cost: $80 (refund) + $4 (reship) + ~$15 (future discount usage)
= ~$99 — worth it vs the ~$2,400 risk of a negative public review +
attrition
```

**For declines:**
```
Recommended action: Decline gracefully + offer 15% discount on next order
Rationale: Customer is requesting refund 87 days after delivery. Return
window is 30 days. Customer's two prior orders both went smoothly so this
isn't a chronic-complainer situation; small discount on next purchase
preserves the relationship.
Estimated cost: ~$8 if used (15% of avg next order $55)
```

Rationale should help the buyer understand WHY, not just WHAT.

---

## Action recommendation in batch mode

When the skill processes a batch via .xlsx, the "Recommended Action" column shows the action code (e.g., `refund_full_plus_credit`) and a separate "Rationale" column shows the one-line reasoning.

The buyer reviews and updates a "Decision" column with what they actually did. Over time the buyer can review patterns: does the skill's recommendations align with what they ultimately decide? If consistently off (e.g., skill recommends refund_full but buyer typically chooses reship), the buyer can adjust the default policy in `config.store.policies`.

---

## When the skill is uncertain about the action

For ambiguous cases (e.g., a defect ticket where it's unclear whether the customer caused the damage or it was manufacturing), the skill:

1. Recommends an investigative action ("ask for photo / clarification") rather than committing to a refund/reship
2. Drafts a reply that asks the clarifying question warmly
3. Flags the ticket as "needs investigation before action" in the .xlsx Decision column
4. Doesn't force a recommendation when one isn't warranted

Don't fake confidence on actions the skill can't reasonably determine.

---

## Cost tracking across the batch

Sheet 2 of the batch .xlsx aggregates:

- Total recommended refund value across the batch
- Total recommended replacement/reship cost
- Total store credit issued
- Estimated total cost to brand

This helps the buyer see the financial impact of the day's tickets at a glance. If the total recommended cost is unusually high (>$300/day for a small brand), that's a signal something systemic is going on — defect rate, fulfillment partner issue, shipping carrier problem.
