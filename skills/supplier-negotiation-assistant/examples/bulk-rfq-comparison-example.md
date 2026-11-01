# Bulk RFQ Comparison — Reference Example

Shows what gets produced when the buyer sources a new product across multiple suppliers and wants to compare quotes side-by-side.

**Brand:** {{brand_name}}
**RFQ:** River Stone Pour-Over 2026 Q2 reorder + capacity expansion
**Target quantity:** 1500 units initial; 6000 annually
**Suppliers contacted:** 5 (3 China, 1 Vietnam, 1 NA)
**Output:** `.xlsx` workbook with 4 sheets

---

## Input (what the buyer described)

> "I'm planning my Q2 reorder of the River Stone Pour-Over. Want to get quotes from 5 suppliers: Shenzhen Stoneworks (current supplier), Jingdezhen Ceramics, two new China suppliers I just found on Alibaba, and a Vietnamese supplier in Bat Trang. Same RFQ to all 5: 1500 unit initial order, 60-day lead time, FOB to my Brooklyn warehouse, samples beforehand. Help me draft the letters and compare the quotes when they come in."

---

## The five suppliers (per the buyer's brief)

| Supplier | Region | Stage | Why included |
|---|---|---|---|
| Shenzhen Stoneworks | China | Established | Current supplier; benchmark; want to see if they sharpen pricing |
| Jingdezhen Ceramics | China | Established (1 order, 2 letters) | Backup option I've already started talking to |
| Foshan Pottery Works | China | New | Highly rated on Alibaba; need to validate quality |
| Guangzhou Ceramics Studio | China | New | New, possibly cheaper |
| Bat Trang Heritage Co | Vietnam | New | Alternative geography to diversify supply |

---

## .xlsx output structure

### Sheet 1: Outreach Queue (5 rows + header)

Sample excerpt showing the variation in tailored letters across the 5 suppliers — same RFQ content, different region/stage shaping:

| Supplier | Region | Stage | Send Time (local) | Follow-up Date | Subject | Letter Body | Quote Response | Status |
|---|---|---|---|---|---|---|---|---|
| Shenzhen Stoneworks | China | established | 2026-04-08 10:00 (Asia/Shanghai) | 2026-04-11 | RFQ — RS Pour-Over Q2 2026 + 2026 Annual Capacity | Dear Ms. Chen, Hope you're well after the recent reorder. We're planning our Q2 production... [365 words] | (empty) | Drafted |
| Jingdezhen Ceramics | China | established | 2026-04-08 10:00 (Asia/Shanghai) | 2026-04-11 | RFQ — River Stone Pour-Over Q2 2026 production | Dear Ms. Wang, Thank you for the sample shipment last month. We're now planning our Q2 production... [340 words] | (empty) | Drafted |
| Foshan Pottery Works | China | new | 2026-04-08 10:00 (Asia/Shanghai) | 2026-04-13 | RFQ from {{brand_name}} — River Stone Pour-Over | Dear Mr. Lin, We're {{brand_name}}, a US-based ceramics brand sourcing for our 2026 lineup. Discovered your factory via Alibaba and would like to request a quote for... [285 words] | (empty) | Drafted |
| Guangzhou Ceramics Studio | China | new | 2026-04-08 10:00 (Asia/Shanghai) | 2026-04-13 | RFQ from {{brand_name}} — ceramic pour-over production | Dear Mr. Zhou, We're {{brand_name}}, a US-based ceramics brand looking for a manufacturing partner... [275 words] | (empty) | Drafted |
| Bat Trang Heritage Co | Vietnam | new | 2026-04-08 09:00 (Asia/Ho_Chi_Minh) | 2026-04-12 | RFQ — ceramic pour-over production from Vietnam | Dear Mr. Nguyen, Hope you are well. We're {{brand_name}}, a US-based ceramics brand looking to diversify our manufacturing partners in the region... [255 words] | (empty) | Drafted |

Notice the variation:
- **Established China suppliers**: shorter intro (relationship implied), references prior orders specifically
- **New China suppliers**: introductory "We're {{brand_name}}..." opening, more mutual-benefit framing
- **Vietnamese supplier**: slightly different opening register, mentions geography diversification (subtle context)
- All 5 share identical RFQ specs (1500 units, 60-day lead time, FOB to Brooklyn, samples upfront)

Subject lines all start with "RFQ" so the buyer can filter easily; consistent across the 5.

---

### Sheet 2: Quote Comparison (5 rows pre-populated; auto-fills as buyer enters quotes)

Pre-populated structure with the supplier names; the buyer fills in quote data as replies arrive:

| Supplier | Region | MOQ Offered | Unit Price (USD) | Quoted Qty | Total at Qty | Lead Time (days) | Payment Terms Offered | Shipping Terms | Sample Cost (USD) | Sample Availability | Quote Validity | Shipping Estimate | Duties Estimate | Total Landed Cost | Per-Unit Landed Cost | Rank by Landed Cost | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Shenzhen Stoneworks | China | 1500 | $4.05 | 1500 | $6,075 (formula) | 45 | 30/70 TT | FOB | $0 (stock sample) | Ready | 30 days | $1,400 | $610 | $8,085 (formula) | $5.39 (formula) | 2 | Best lead time; existing relationship |
| Jingdezhen Ceramics | China | 1000 | $3.85 | 1500 | $5,775 (formula) | 60 | 30/70 TT | FOB | $40/sample + ship | 7 days | 30 days | $1,400 | $580 | $7,755 (formula) | $5.17 (formula) | 1 | Lower price; needs new sample run |
| Foshan Pottery Works | China | 1500 | $4.20 | 1500 | $6,300 (formula) | 50 | 30/70 TT | FOB | $50/sample + ship | 10 days | 21 days | $1,400 | $630 | $8,330 (formula) | $5.55 (formula) | 4 | Mid pricing; longer sample time |
| Guangzhou Ceramics Studio | China | 1000 | $3.50 | 1500 | $5,250 (formula) | 75 | 50/50 TT | FOB | $0 (free samples!) | Ready | 14 days | $1,400 | $525 | $7,175 (formula) | $4.78 (formula) | (?) | Lowest price BUT red flags — free samples + long lead time + 50/50 deposit |
| Bat Trang Heritage Co | Vietnam | 800 | $4.50 | 1500 | $6,750 (formula) | 55 | 30/70 TT | FOB | $30/sample + ship | 14 days | 45 days | $1,500 | $135 (Vietnam-US trade preferences) | $8,385 (formula) | $5.59 (formula) | 5 | Higher base but lower duties; geography diversification |

Color-coding:
- **Lowest landed cost** highlighted green
- **Red flag rows** (Guangzhou — free samples + long lead + 50/50 deposit) highlighted yellow for review

The buyer enters MOQ Offered, Unit Price, Lead Time, Payment Terms, etc. as quotes arrive. Formulas compute Total at Qty, Total Landed Cost, and Per-Unit Landed Cost automatically. Rank by Landed Cost auto-sorts.

---

### Sheet 3: Supplier Memory Updates (5 rows)

| Supplier | Updates |
|---|---|
| Shenzhen Stoneworks | • Logged RFQ letter sent 2026-04-08; pending response by 2026-04-11<br>• Note added: April 2026 RFQ for Q2 reorder<br>• Stage: remains 'established' |
| Jingdezhen Ceramics | • Logged RFQ letter sent 2026-04-08; pending response by 2026-04-11<br>• Stage: remains 'established'<br>• Letter referenced March 2026 sample shipment |
| Foshan Pottery Works | • Supplier file created — new<br>• Logged RFQ as first letter sent<br>• Stage: 'new'<br>• Pending response by 2026-04-13 (5 day window for new China supplier) |
| Guangzhou Ceramics Studio | • Supplier file created — new<br>• Logged RFQ as first letter sent<br>• Stage: 'new'<br>• FLAG: skill noted this supplier in 'watch carefully' status pending evaluation |
| Bat Trang Heritage Co | • Supplier file created — new<br>• Logged RFQ as first letter sent<br>• Stage: 'new'<br>• Region: vietnam<br>• Pending response by 2026-04-12 |

---

### Sheet 4: Negotiation Tactics Reference

```
RED FLAGS in incoming quotes
• Unit price >25% below the cluster average → quality risk; ask hard spec questions
• "Free samples" offered on a custom product from a brand-new supplier → likely doesn't have capability
• 50/50 deposit structure on a new relationship → unusual; may indicate cash pressure on supplier side
• Refusal to quote validity period → not a serious supplier
• Replies that don't address spec details → factory may not actually make this product
• Lead time substantially longer than others (>40% longer) → likely subcontracting or unfamiliar with the product

COUNTER-NEGOTIATION guidance
• If best landed-cost supplier is also slowest replier → push for faster lead time as condition of award
• If multiple suppliers cluster around the same price → ask each for tier breakdowns; one will reveal more
• If one supplier is significantly faster than others → leverage for tighter lead time in counter
• If lowest price is from a new supplier with red flags → ask for verifiable references; insist on paid sample evaluation
• Don't reveal competing quotes by exact number; reveal range ("we have a quote at the $X.XX range") if at all

SOFT TELLS in supplier replies
• Supplier asks detailed spec questions → engaged; high quality signal
• Supplier doesn't address one of the RFQ specs → that spec is non-negotiable (e.g., they'll only do EXW not FOB)
• Quote arrives within 24 hours → highly motivated supplier
• Quote arrives 5+ days late → low motivation; relationship may not work
• Supplier mentions a different product as alternative → might not actually make this product
• Supplier requests a video call → high engagement; great signal

DECLINE letter pattern
• Keep declines short and respectful — they may be your next year's primary supplier
• Acknowledge a specific positive from their quote (lead time, communication, sample policy)
• Express interest in future RFQs
• Never reveal which supplier you awarded to
• Never compare them unfavorably to the winner
```

---

## What the buyer does next

Day 0 (today): Send all 5 letters via each supplier's preferred channel (TradeMessenger for new China; email for established + Vietnam).

Day 3-7: First quotes arrive (faster suppliers, more motivated ones).

Day 7-10: All quotes arrived (nudge any silent ones at 2x the expected window).

Day 10-14: Fill in Sheet 2 with quotes; review red flags + tactics; ask clarifying questions to top 2-3 suppliers.

Day 14-21: Award to one supplier; send decline letters to others using the patterns in Sheet 4; update supplier memory files.

---

## What this saves vs. manual approach

Manually:
- Draft 5 region-tailored letters: 2-3 hours
- Build a comparison spreadsheet from scratch: 1-2 hours
- Track responses + follow-ups across 5 suppliers in your head / notes: ongoing, error-prone
- Calculate total landed cost for each: 30 min × 5 = 2.5 hours
- Write 4 decline letters at the end: 1 hour
- Update supplier records (rarely done well): hours / never
- **Total: 8-12 hours over 3 weeks, with supplier records rarely captured well**

With this skill:
- Skill runs the RFQ batch: ~3-5 min
- Buyer reviews + sends letters: ~30 min
- Buyer fills in quotes as they arrive: ~15 min/supplier × 5 = ~75 min
- Skill drafts decline letters once awarded: ~10 min
- **Total: ~2 hours over 3 weeks, with full supplier memory captured**

Over 12 months, the buyer will have 30-50 supplier files captured automatically. That's the moat — by year 2, the skill is making decisions informed by the entire sourcing history, not just the immediate ask.
