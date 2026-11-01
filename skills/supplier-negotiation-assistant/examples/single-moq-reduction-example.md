# Single MOQ Reduction — Reference Example

Shows what gets produced when the buyer asks for help drafting an MOQ reduction letter to a new Chinese supplier.

**Brand:** {{brand_name}} (a US-based ceramics brand)
**Supplier:** Jingdezhen Ceramics Co., Ltd. (new supplier, first contact)
**Region:** China
**Letter type:** MOQ reduction
**Relationship stage:** New
**Output:** Single `.docx`

---

## Input (what the buyer described)

> "I found a ceramic supplier on Alibaba — Jingdezhen Ceramics. The contact is Cindy Chen, Sales Manager. They quoted $4.20/unit for the River Stone Pour-Over at 1000 MOQ. I want to do 300 for the initial launch — willing to pay a higher per-unit price. Help me draft the letter."

---

## Detection

- **Letter type:** MOQ reduction
- **Region:** China (Jingdezhen — Jiangxi Province)
- **Relationship stage:** New (first contact; supplier file doesn't yet exist)
- **Leverage point selected:** Per-unit-premium approach (buyer mentioned willingness to pay more)
- **Combined ask?:** No — keeping focused on MOQ alone
- **Holiday check:** Today is March 14, 2026 — no holiday conflicts

---

## .docx output structure

```
MOQ Reduction  →  Jingdezhen Ceramics Co., Ltd.
Drafted 2026-03-14  ·  Region playbook: China
Relationship stage: new
Contact: Ms. Cindy Chen, Sales Manager
```

### SUPPLIER MEMORY SNAPSHOT
- Known since: 2026-03-14 (file created with this letter)
- Orders completed: 0
- Prior asks: (none)
- Current MOQ on file: 1000 (their quoted MOQ)
- Current unit price: $4.20
- Payment terms in force: (not yet established)

### PRODUCT CONTEXT
- Product: River Stone Pour-Over (ceramic)
- Summary: Initial launch SKU for {{brand_name}}'s spring lineup; planned 300-unit first order with 500-unit reorder within 3 months if the launch performs

### DRAFTED LETTER

Subject: Following up on the River Stone Pour-Over quote

```
Dear Ms. Chen,

Thank you for the detailed quote you sent on March 12 for the River Stone Pour-Over. We appreciate the professionalism and clarity of your response.

The 1000-unit MOQ is higher than our launch plan can support, so I'd like to ask about a smaller initial run. We're a US-based ceramics brand launching River Stone as our spring product, and we'd like to validate the design with our customers before committing to a larger production order.

Would it be possible to do a first order of 300 units? We understand the smaller production may not match the 1000-unit pricing — we'd be comfortable at your 100-tier unit price ($4.80/unit, if that's the right level) for this initial run. We're committed to scaling: our reorder plan is 500+ units within three months, and we expect to be at the 1000-unit threshold by the end of 2026 if the product performs the way we believe it will.

We're looking for a long-term ceramics partner, and starting at 300 lets us validate the design with our customers before scaling. We believe this is the foundation of a strong working relationship that benefits both sides.

Could you let us know by March 21 whether 300 units at the 100-tier price is workable? Happy to discuss any alternative structure — including a setup fee on our side, or rolling our order into one of your scheduled production windows.

Best regards,
Jamie Carter
{{brand_name}}
```

Word count: 264 words (China region target for new supplier: 220-300)

### WHY THIS LETTER WORKS

- Applied Chinese opening convention with formal honorific ("Dear Ms. Chen")
- Bridge references the specific quote and quote date (specific = serious)
- Indirect ask framing ("Would it be possible to..." rather than "We need...")
- Per-unit-premium leverage point used (the buyer's stated willingness to pay more)
- Mutual benefit framing emphasizes long-term partnership — high resonance in China
- Acknowledges face by validating their pricing structure (asking for the 100-tier price, not asking them to invent a new tier)
- Specific deadline (7 business days, China-region appropriate)
- Offers alternative structures so the supplier has flexibility

### ALTERNATE PHRASINGS

**For the key ask sentence:**

Option 1: "Would it be possible to do a first order of 300 units?"
Option 2: "We'd like to propose a first run of 300 units. Is this workable on your end?"
Option 3: "Could you tell us whether 300 units would be a feasible starting point for our relationship?"

**For the mutual-benefit framing:**

Option 1: "We're looking for a long-term ceramics partner..."
Option 2: "We see this as the start of a multi-year relationship..."
Option 3: "Building stable orders together over time is what we're hoping for..."

### SUGGESTED FOLLOW-UP TIMING

- Wait: 3 business days before nudging (China-region standard)
- Follow-up date: 2026-03-19
- If no reply: Send a soft follow-up referencing the original letter date. China-region softness: "Just wanted to check in on the question we sent on the 14th — appreciate any update when convenient." Avoid pushiness; in China, persistence past the third nudge starts to hurt.

### SUPPLIER MEMORY WRITTEN

The skill created a new supplier file at:
`<plugin-root>/.cache/suppliers/jingdezhen-ceramics-co-ltd-cindy-chen.json`

With:
- Supplier_id: jingdezhen-ceramics-co-ltd-cindy-chen
- Region: china
- Relationship_stage: new
- Letters_sent: [{type: moq_reduction, date: 2026-03-14, summary: "Requested 300 units instead of 1000 MOQ, offered 100-tier unit price"}]
- Pending_responses: [{expected_response_by: 2026-03-19, follow_up_due: 2026-03-20}]
- Communication_preferences.primary_channel: alibaba_trademessenger (initial; will switch to email after first reply)
- Communication_preferences.holidays_observed: [lunar_new_year, qingming, labor_day, dragon_boat, mid_autumn, national_day_golden_week]

---

## What the buyer does next

1. Copy the letter into Alibaba TradeMessenger (initial channel for new China contact)
2. Send by end of buyer's day — letter will land in Cindy's morning per time zone
3. Set a follow-up reminder for March 19
4. When Cindy replies (expected by March 19), update the supplier file's `letters_sent[0].outcome` with what she said

---

## Why this skill saves time

Manually:
- Research how to phrase MOQ reduction politely in Chinese business culture: 30 min
- Draft the letter, second-guess tone, revise: 25 min
- Forget to track follow-up timing
- Forget the specifics for next time you write to this supplier
- **Total: ~1 hour, with no relationship memory captured**

With this skill:
- Skill runs: ~30 seconds
- Buyer reviews + sends: ~5 min
- **Total: ~5 min, with the supplier file capturing everything for next letter**

The compounding value: the next letter to Cindy (whether MOQ follow-up, pricing tier, or sample request) will reference this letter automatically. By the fifth letter, the skill is acting like a CRM-aware negotiation partner.
