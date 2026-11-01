# Single Dispute Letter — Reference Example

Shows what gets produced when the buyer needs to file a dispute over a quality issue with an established Chinese supplier.

**Brand:** {{brand_name}}
**Supplier:** Shenzhen Stoneworks Co., Ltd. (established — 4 completed orders)
**Region:** China
**Letter type:** Dispute (medium severity, glaze cracking on 14% of units)
**Relationship stage:** Established (to be transitioned to strained pending response)
**Output:** Single `.docx`

---

## Input (what the buyer described)

> "Order #5118 came in last week — about 14% of the units have glaze cracking near the spout. Same defect on every cracked unit, so it's clearly a production batch issue. Ms. Chen at Shenzhen Stoneworks has been a great supplier for 4 orders now. I want to file a dispute but I don't want to burn the relationship — they've been solid."

---

## Detection

- **Letter type:** Dispute (quality defect)
- **Region:** China
- **Relationship stage:** Established → Strained (pending response)
- **Severity:** Medium (14% rate is meaningful but not catastrophic; first quality issue in the relationship)
- **Resolution structure suggested:** Inspection + plan + credit OR replacement (give supplier two paths)
- **Holiday check:** Today is March 26, 2026 — no holiday conflicts
- **Evidence captured:** Order ID, shipment + arrival dates, defect description, % affected, photos attached

---

## .docx output structure

```
Dispute Letter  →  Shenzhen Stoneworks Co., Ltd.
Drafted 2026-03-26  ·  Region playbook: China
Relationship stage: established  (→ strained pending response)
Contact: Ms. Cindy Chen, Sales Manager
```

### SUPPLIER MEMORY SNAPSHOT

- Known since: 2025-10-15
- Orders completed: 4
- Total volume to date: $48,000
- Prior asks: sample_request 2025-10-15; moq_reduction 2025-11-08; pricing_tier 2026-01-22
- Current MOQ on file: 300
- Current unit price: $4.20 (1000-tier)
- Payment terms in force: 30/70 TT before shipping

### PRODUCT CONTEXT

- Product: River Stone Pour-Over (ceramic)
- Order #5118 — shipped 2026-02-12, arrived Brooklyn warehouse 2026-03-18
- Quantity: 1500 units
- Affected: 210 of 1500 (14%) — glaze cracking on inner wall near spout
- Photos: 12 detail shots attached + comparison photos from order #5005 (prior batch) showing standard glaze

### DRAFTED LETTER

Subject: Order #5118 — quality issue on River Stone Pour-Over batch

```
Dear Ms. Chen,

I want to bring an issue to your attention from order #5118, which shipped February 12 and arrived our Brooklyn warehouse on March 18.

Upon inspection of the 1500 units received, we identified glaze cracking in approximately 14% of units (210 of 1500). The cracking appears on the inner wall near the spout — the same location across the affected units, suggesting a production-batch issue rather than handling damage.

I've attached 12 detail photos of the affected units, plus comparison photos from order #5005 (October 2025) showing the standard glaze finish for reference.

I'd like to propose two paths and see which works best on your end:

1. Your QC team inspects the photos and confirms whether this is consistent with a production-batch issue. Once confirmed, we discuss either (a) a credit on the 210 affected units to be applied to our next order, or (b) replacement of 210 units in our next production run, included at no charge.

2. If your team identifies this as something we missed in the spec, we'd like to understand that as well and adjust on our end.

This is the first quality issue we've seen across four orders together, and we're confident we can resolve it. We've appreciated the consistent quality on the prior orders and we're committed to continuing this partnership — we want to handle this in a way that preserves the relationship we've built.

Could you respond by April 2? Our next reorder is planned for late April, so confirming the resolution before then would help both of us plan production timing.

Thank you for your attention to this.

Best regards,
Jamie Carter
{{brand_name}}
```

Word count: 322 words (China region dispute target: 280-400)

### WHY THIS LETTER WORKS

- Fact-based bridge with specific order ID, ship date, arrival date
- Quantitative description (14%, 210 of 1500) — no exaggeration
- Photo evidence referenced + comparison photos to a known-good prior order
- Two resolution paths offered (face-saving — supplier has options, not one demand)
- Acknowledges supplier's quality record on prior orders (preserves relationship)
- "We're committed to continuing this partnership" — Chinese-region appropriate framing
- Specific deadline tied to operational planning (next reorder), not arbitrary
- No emotional language; no blame; no threat of finding another supplier
- Founder-tier signing not used (kept at first-name only) — appropriate for established relationship with first quality issue

### ALTERNATE PHRASINGS

**For the dispute framing:**

Option 1: "We identified glaze cracking in approximately 14% of units..."
Option 2: "On inspection we found cracking on 210 of the 1500 units received..."
Option 3: "Quality inspection revealed a consistent defect pattern in 14% of the shipment..."

**For the relationship-preservation close:**

Option 1: "We're committed to continuing this partnership..."
Option 2: "We've valued the consistency of the prior orders and want to preserve what we've built..."
Option 3: "This is the first issue we've seen across our work together, and we're confident in resolving it cleanly..."

### SUGGESTED FOLLOW-UP TIMING

- Wait: 3 business days before nudging (China-region standard); add 1 day for dispute weight
- Follow-up date: 2026-04-01 (if no response by then)
- If no reply by April 2: send a soft follow-up referencing the original letter and the operational deadline. Maintain the same measured tone. Do NOT escalate language on the first follow-up.
- If still no reply 5 business days after the follow-up: consider whether to copy Cindy's manager (Frank Liu, per supplier notes)

### SUPPLIER MEMORY WRITTEN

Updated `<plugin-root>/.cache/suppliers/shenzhen-stoneworks-co-ltd-cindy-chen.json`:

- Added letter to `letters_sent`:
  - type: dispute
  - date: 2026-03-26
  - summary: "Quality issue: glaze cracking on 14% of order #5118 (210 of 1500). Requested QC inspection + resolution choice between credit or replacement."
  - outcome: pending
- Added to `pending_responses`: expected_response_by: 2026-04-02
- Added a stage transition: `established` → `strained` (pending dispute resolution); will transition back to `established` if resolved positively, or stay strained if not
- Added a note: "March 2026 dispute on order #5118. Resolution pending."

---

## What the buyer does next

1. Send the letter to Cindy via direct email (not TradeMessenger — disputes always move to email)
2. Set follow-up reminder for April 1
3. When Cindy responds:
   - If she confirms and proposes resolution: update letter outcome to "approved" with specifics; transition stage back to `established`
   - If she pushes back / blames the customer: stays `strained`; consider escalation
   - If silence past follow-up: escalation path opens
4. Once resolved, the supplier memory will reflect the resolution — useful context for future letters

---

## What the skill specifically avoided

- Emotional language ("This is unacceptable") — would damage the relationship
- Threats of finding another supplier — burns the relationship for short-term pressure
- Asking for a refund publicly / via TradeMessenger (which has a public audit trail) — keeping it in email
- Demanding a specific resolution (credit only, replacement only) — giving the supplier choice preserves face
- Bringing up payment terms or future orders in the same letter — combining is poor practice in disputes
- Hyperbole about the percentage ("a massive batch failure") — 14% is accurate; "massive" is theater
