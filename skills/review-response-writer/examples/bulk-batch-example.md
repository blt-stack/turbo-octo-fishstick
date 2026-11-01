# Bulk Batch — Reference Example

Shows what gets produced when the buyer uploads a CSV of 25 reviews exported from Judge.me + Trustpilot + Google.

**Brand:** {{brand_name}}
**Batch:** 25 reviews across 3 platforms (Judge.me 14, Trustpilot 6, Google 5), processed in one run
**Output:** Single `.xlsx` workbook with 4 sheets

---

## Detection summary

- **Tier distribution:** 4 recovery (1-2★), 5 clarify (3★), 16 amplify (4-5★)
- **Sentiment flags:** 23 constructive, 1 abusive (Trustpilot), 1 suspected competitor (Trustpilot)
- **Platforms:** Judge.me (14), Trustpilot (6), Google (5)
- **NPS-style score:** +48 (16 promoters, 5 passives, 4 detractors out of 25)

---

## Sheet 1: Reply Queue (25 rows + header)

Sample 5-row excerpt:

| Received | Platform | Star | Reviewer | Verified | Product | Tier | Sentiment | Issue Category | Original Review | Drafted Public Reply | Char Count | Private Follow-up | Dispute Draft | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-05-15 | Trustpilot | 1 | Marcus T. | Y | River Stone Pour-Over | Recovery (1-2★) | constructive | shipping_cs_failure | [Worst customer service...] | Hi Marcus, Three emails over eleven days... | 624 | Subject: Personal note from Jamie... | — | Pending review |
| 2026-05-18 | Trustpilot | 1 | Anonymous | N | Studio Glaze Bowl | Recovery (1-2★) | fake | n/a | This product is terrible... | (placeholder) | — | [Trustpilot dispute draft populated] | Pending review |
| 2026-05-19 | Judge.me | 5 | Sam K. | Y | River Stone Pour-Over Mug | Amplify (4-5★) | constructive | n/a | I've had a lot of mugs... | Hi Sam, "Made by a person"... | 218 | — | — | Pending review |
| 2026-05-20 | Judge.me | 3 | Priya R. | Y | Studio Glaze Bowl | Clarify (3★) | constructive | expectation_mismatch | Good quality but the color... | Hi Priya, Thank you for this... | 252 | — | — | Pending review |
| 2026-05-21 | Google | 5 | Jamie W. | (unknown) | (brand-level review) | Amplify (4-5★) | constructive | n/a | Best ceramic brand I've found... | Hi Jamie, Thank you for the kind review... | 245 | — | — | Pending review |

Color coding:
- **Tier cell** colored per tier (recovery red, clarify yellow, amplify green)
- **Sentiment cell** colored per subtype (abusive red, fake orange, sycophantic yellow, constructive white)
- **Status cell** colored per state (Pending review yellow, Approved blue, Sent green, Held orange, Disputed red)

---

## Sheet 2: Tier & Sentiment Breakdown

```
Total reviews in batch                    25

Tier distribution
  Recovery (1-2★)                          4
  Clarify (3★)                             5
  Amplify (4-5★)                          16

Star distribution
  1★                                       2
  2★                                       2
  3★                                       5
  4★                                       6
  5★                                      10

Sentiment distribution
  constructive                            23
  abusive                                  1
  fake                                     1
  sycophantic                              0

Platform breakdown
  Judge.me                                14
  Trustpilot                               6
  Google                                   5

Issue categories (recovery/clarify tier)
  shipping                                 3
  expectation_mismatch                     3
  sizing                                   1
  cs_failure                               1
  quality                                  1

NPS-style summary
  Promoters (4-5★)                        16
  Passives (3★)                            5
  Detractors (1-2★)                        4
  NPS-style score                        +48.0
```

The buyer sees at a glance: this week's batch is healthy (NPS +48), with one Trustpilot fake flagged for dispute and one shipping pattern emerging.

---

## Sheet 3: Cache Mining Summary

```
TESTIMONIAL MINING
  Quotes extracted                         11
  Quote #1: "Made by a person. The weight, the way the handle sits..." — Sam K. (River Stone Pour-Over Mug, score 92)
  Quote #2: "I've had a lot of mugs in my life. This one feels like it was made by a person." — Sam K. (River Stone Pour-Over Mug, score 78)
  Quote #3: "Best ceramic brand I've found — worth every dollar." — Jamie W. (brand-level, score 75)
  Quote #4: "The glaze on the Studio Bowl is a quiet kind of beautiful." — Aisha N. (Studio Glaze Bowl, score 88)
  [...more quotes...]

OBJECTION MINING
  Objections extracted                      4
  Objection #1: Shipping is unreliable [category: shipping · systemic]
  Objection #2: CS unreachable when problems happen [category: customer_service · emerging]
  Objection #3: Listing photos don't reflect real-life color [category: expectation_mismatch · emerging]
  Objection #4: Studio Glaze Bowl glaze inconsistency [category: quality · novel]

KEYWORD ENRICHMENT
  Phrases enriched                         3
  Phrase #1: "made by a person" (4 occurrences across: River Stone Pour-Over Mug, River Stone Pour-Over)
  Phrase #2: "feels balanced" (3 occurrences across: River Stone Pour-Over)
  Phrase #3: "quiet kind of beautiful" (3 occurrences across: Studio Glaze Bowl)
```

After this batch, the brand's downstream skills now have:
- 11 new testimonial candidates for landing pages, A+ Content, and ads
- 4 new objections to address in copy (including one systemic one to also address operationally)
- 3 keyword phrases promoted into the SEO cache for product description and ad copy use

---

## Sheet 4: Systemic Issues (auto-detected)

| Pattern | Review Count | First Seen | Recommendation |
|---|---|---|---|
| Shipping unreliability via UPS Memphis | 5 | 2026-05-04 | 5 shipping complaints in 11 days all mention UPS or carrier hub delays. Not a one-off. Recommend testing a non-UPS carrier for orders shipping from this region. Also: the objection has been promoted to systemic — Ad Creative Generator and Landing Page Copywriter will now address shipping proactively. |
| Studio Glaze Bowl glaze inconsistency | 3 | 2026-05-19 | 3 reviews on Studio Glaze Bowl reference inconsistent glaze (one called it "uneven," one called it "varies a lot between bowls"). Recommend inspecting the May 12 production batch before more ship. Also: Ad Creative Generator should NOT lead with glaze beauty for this SKU until resolved. |

---

## How the buyer uses the bulk output

Typical workflow (~45 min for a 25-review batch):

1. **Open Sheet 1 (Reply Queue)** — scan the Tier column for recovery rows first (handle red/yellow tier cells before green ones)
2. **For each recovery row:**
   - Review the drafted public reply, edit if needed
   - Review the drafted private follow-up — must be sent within 24h of posting the public reply
   - Update the Status column ("Approved" → post → "Sent")
3. **For the abusive row:**
   - Read the short, professional public reply
   - Decide whether to post (buyer's call)
   - Update Status to "Held" if undecided
4. **For the fake row:**
   - Read the Trustpilot dispute draft
   - Submit it via Trustpilot's "Report this review" workflow
   - Update Status to "Disputed"
5. **For the clarify rows (3★):**
   - Review the probe question — is it the right probe?
   - Adjust if needed
   - Post and update Status
6. **For the amplify rows (4-5★):**
   - Scan-read, batch-approve, batch-post
   - These are the bulk of the workload but the lowest cognitive load
7. **Check Sheet 4 (Systemic Issues)** — flag the UPS Memphis pattern + the Studio Glaze Bowl batch for internal action
8. **Check Sheet 3 (Cache Mining)** — verify the quotes the skill extracted are ones you'd want featured. Reject any that don't feel right (the buyer can do this in Sheet 1 by changing the "Use as Testimonial?" field; only approved quotes flow to the cache)

---

## Time savings

Without this skill, processing 25 reviews manually:
- Reading + categorizing per platform's rules: ~30 min
- Drafting each public reply: ~3-7 min × 25 = 75-175 min
- Drafting private follow-ups for 4 recovery cases: ~30 min
- Researching dispute path for the fake review: ~20 min
- Maintaining a testimonial / objection library manually: ~rarely done
- **Total: 2.5 - 5 hours, with no cache mining**

With this skill:
- Skill runs the batch: ~3-5 min
- Buyer reviews + edits + approves: 30-60 min
- **Total: ~45 min - 1 hour**, with full cache mining auto-completed in the background

A 70-80% time savings, plus:
- The systemic-issue detection across platforms (almost impossible manually)
- The cross-skill cache writes that compound over months (becomes a curated asset library for the rest of the plugin)
- The dispute draft (saves 20 min researching the right wording)

---

## Notes on this exemplar

- **Mixed-platform batches are common** — most brands have reviews on at least 2 platforms; the skill processes them in one workbook with per-platform constraints applied
- **The cache mining is the hidden ROI** — the visible value is the replies, but the testimonial + objection + keyword caches compound across the plugin
- **Founder-signed recovery on Trustpilot** — the skill recommended founder signing for Marcus's 1★ + CS failure case; the buyer can override but the default is to recommend escalation for high-stakes platforms
- **Fake reviews get dispute drafts** but the public reply column is left mostly empty for them — the placeholder reply is short and noncommittal, and the buyer decides whether to post it after the dispute outcome
- **No discount codes** were included in any reply across 25 reviews — the skill enforces this universally
- **No two openers** are identical across the 25 replies — the skill varies "Hi [Name]," "[Name] —," "Thank you for this, [Name]," etc. to avoid form-letter feel
- **Verified purchase status** is shown for every reviewer — affects the testimonial cache (only verified gets `ad_creative_testimonial` tag) and the dispute draft strength
