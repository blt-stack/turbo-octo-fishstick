# Bulk Batch — Reference Example

Shows what gets produced when the buyer runs "process the next 12 unread customer service tickets from my Gmail inbox."

**Brand:** {{brand_name}}
**Batch:** 12 unread tickets fetched from Gmail "Support" label, processed in one run
**Output:** Single `.xlsx` workbook with 3 sheets

---

## Sheet 1: Reply Queue (12 rows + header)

Sample 4-row excerpt:

| Received | Customer | Email | Category | Sub-type | Sentiment | Original Ticket | Drafted Reply Subject | Drafted Reply Body | Recommended Action | Rationale | Est. Cost | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-05-22 09:14 | Sarah Mitchell | sarah.m@email.com | Shipping | Delayed | neutral | Hi - I ordered the River Stone Pour-Over on May 10... | Re: where is my order | Hi Sarah, Sorry your order has been sitting... | Issue $10 store credit + escalate w/ UPS + 48h followup | Order 6 days past estimate. Repeat customer ($340 LTV). Worth proactive handling. | $10 + ~10 min | Pending review |
| 2026-05-22 11:08 | Marcus T. | marcus.t@email.com | Defects/Damages | BOA | angry | I just opened my order and the ENTIRE THING IS CRACKED... | Re: BROKEN ON ARRIVAL | Hi Marcus, I'm so sorry. Opening a brand-new... | Full refund + replacement + $20 credit + founder reply | BOA on first-time customer + Trustpilot threat. Over-delivery protects $500-2K LTV risk. | ~$71 | Pending review |
| 2026-05-22 13:45 | Aisha Khan | aisha.k@email.com | Pre-purchase | Sizing | friendly | Hi! Huge fan of the brand. I'm a UK 10 / US 8 — would I be a Medium or Large in the long-sleeve? | Re: Sizing question | Hi Aisha, Thanks for the kind words! For UK 10 / US 8, the Medium will... | No action needed | Pre-purchase question. Friendly tone. Answer the question; the sale follows. | $0 | Pending review |
| 2026-05-22 14:22 | David L. | david.l@email.com | Returns/Refunds | Doesn't fit | neutral | The hoodie is too big. Can I exchange for a smaller size? | Re: Exchange request | Hi David, No problem — happy to swap that for you... | Free exchange (keep original, send Medium) | Apparel doesn't-fit case under $80 — keeping original saves return-ship cost; preserves goodwill. | ~$8 (replacement shipping) | Pending review |

Color-coding:
- **Sentiment cell** colored per sentiment (angry = red, neutral = white, friendly = green)
- **Status cell** colored per state (Pending review = yellow, Approved = blue, Sent = green, Held = orange, Escalated = red)
- The buyer updates the Status column as they work through the batch

---

## Sheet 2: Category Breakdown

```
Total tickets in batch                    12

Tickets per category
  Shipping                                 5
  Returns/Refunds                          3
  Defects/Damages                          2
  Pre-purchase                             2

Sentiment distribution
  angry                                    2
  neutral                                  8
  friendly                                 2

Recommended actions
  refund_partial_plus_credit               3
  reship                                   2
  refund_full_plus_credit                  2
  process_return                           2
  no_action                                2
  escalate_founder                         1

Total estimated cost across batch     $187.00
```

The buyer sees at a glance: today's batch has 2 angry tickets, $187 in expected costs, shipping issues dominating. Healthy ratio of neutral/friendly tickets means the brand's CS environment is OK.

---

## Sheet 3: Systemic Issues (auto-detected)

| Pattern | Ticket Count | First Seen | Recommendation |
|---|---|---|---|
| Shipping delays via UPS Memphis facility | 5 | 2026-05-15 | 5 of the last 12 shipping complaints reference UPS Memphis. This isn't a one-off — consider switching fulfillment to a non-UPS carrier for orders shipping from this region. Even a 30-day test would isolate whether the issue is UPS Memphis specifically or carrier-wide. |
| First-batch ceramic chips in River Stone Pour-Over | 3 | 2026-05-19 | 3 BOA reports on the River Stone Pour-Over in the past 7 days, all from the May 18 production batch. Recommend inspecting current inventory of that batch before more ship. |

If no systemic issues detected, the sheet says "(No systemic issues detected in this batch.)" instead.

---

## How the buyer uses the batch output

Typical workflow:

1. **Open Sheet 1 (Reply Queue)** — scan the sentiment column for angry/red tickets; handle those first
2. **Review the Drafted Reply Body** for each — edit if needed, approve if good
3. **Look at the Recommended Action** + Rationale — adopt as recommended or pick differently
4. **Update the Status column** as work progresses:
   - Mark "Approved" → buyer copies the reply into Gmail
   - Mark "Sent" → reply went out (and the buyer takes the corresponding business action: refund, reship, etc.)
   - Mark "Held" → needs more thought / customer follow-up needed
   - Mark "Escalated" → handed to founder or senior person
5. **Check Sheet 3 (Systemic Issues)** — flag the UPS-Memphis pattern + the River Stone batch issue for internal action

---

## Time savings

Without this skill, processing 12 tickets manually:
- Reading + categorizing: ~15 min
- Looking up order context for each: ~20 min
- Drafting each reply: ~5-15 min × 12 = 60-180 min
- Deciding actions: ~5 min × 12 = 60 min
- **Total: 2.5 - 4.5 hours**

With this skill:
- Skill runs the batch: ~3-5 minutes
- Buyer reviews + edits + approves: 30-60 minutes (1-5 min per ticket)
- **Total: ~45 min - 1 hour**

A 70-80% time savings, plus the systemic-issue detection that's almost impossible to do reactively across 12 individual tickets.

---

## Notes on this exemplar

- **Each ticket gets the full treatment** — categorization, sentiment, order context, reply, action, rationale, cost estimate
- **Sentiment + status both color-coded** for visual triage
- **Sheet 2 surfaces the financial impact** so the buyer sees today's cost upfront, not buried in individual tickets
- **Sheet 3 is the high-leverage output** — catching the UPS Memphis pattern or the River Stone batch issue is worth far more than the time saved on the replies themselves
- **The Status column gives the buyer a workflow tracker** — the .xlsx becomes a one-day CS dashboard, not just a static output
- **Reply bodies are full-text** in cell — the buyer copies the cell content directly into Gmail
- **Recommended actions reference the action library** from `action-recommendations.md` so the codes are consistent across batches and over time
