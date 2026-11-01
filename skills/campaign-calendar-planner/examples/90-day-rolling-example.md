# 90-Day Rolling Calendar — Reference Example

The default skill output: a 90-day rolling calendar starting from "today" (the day the skill is run).

**Brand:** {{brand_name}}
**Buyer request:** "Plan my next 90 days"
**Region:** US
**Window:** May 22, 2026 – August 20, 2026 (90 days)

This window crosses Memorial Day, Father's Day, July 4th, and back-to-school timing. No BFCM in scope — that's a separate run when the buyer is ready for Q4.

---

## Campaigns generated (8 total over 90 days)

| # | Campaign | Type | Dates | Days | Total Sends |
|---|---|---|---|---|---|
| 1 | Memorial Day Long Weekend | Holiday | May 22 – May 26 | 5 | 8 |
| 2 | June Brand Story Push | Brand Content | June 1 – June 14 | 14 | 9 |
| 3 | Father's Day | Holiday | June 5 – June 21 | 17 | 14 |
| 4 | Summer Solstice Bestsellers | Tentpole | June 21 – June 28 | 8 | 8 |
| 5 | July 4th Weekend | Holiday | July 1 – July 5 | 5 | 9 |
| 6 | Mid-July Subscriber-Growth Push | Subscriber Growth | July 10 – July 24 | 15 | 12 |
| 7 | Summer Bestsellers Refresh | Tentpole | August 1 – August 14 | 14 | 11 |
| 8 | Pre-Back-to-School (optional, brand-fit-driven) | Cultural | August 15 – August 20 | 6 | 5 |

**Total sends across all channels: 76**

Note: cultural moment (BTS) was included even though the buyer didn't explicitly select "cultural moments" — the skill flagged it as low-priority and brand-fit-driven, and is marked "optional" so the buyer can drop it.

---

## .xlsx Sheet 1: Calendar (first 14 days as a sample)

| Date | Day | Time | Channel | Campaign | Topic | Status |
|---|---|---|---|---|---|---|
| 2026-05-22 | Thu | 10:00 | Email | Memorial Day Long Weekend | Pre-launch teaser ("long weekend offers coming Friday") | Planned |
| 2026-05-23 | Fri | 9:00 | Email | Memorial Day Long Weekend | Memorial Day weekend launch ("20% off site-wide") | Planned |
| 2026-05-23 | Fri | 11:00 | SMS | Memorial Day Long Weekend | Memorial Day SMS | Planned |
| 2026-05-23 | Fri | 9:00 | Paid Ad | Memorial Day Long Weekend | Meta + TikTok long-weekend ads | Planned |
| 2026-05-23 | Fri | 9:00 | Site Update | Memorial Day Long Weekend | Homepage hero swap + popup | Planned |
| 2026-05-24 | Sat | 11:00 | Organic Social | Memorial Day Long Weekend | IG Reel ("how we spend our long weekends") | Planned |
| 2026-05-25 | Mon | 10:00 | Email | Memorial Day Long Weekend | Day-of Memorial Day reminder | Planned |
| 2026-05-26 | Tue | 9:00 | Email | Memorial Day Long Weekend | Wrap-up + transition | Planned |
| 2026-06-01 | Mon | 10:00 | Email | June Brand Story Push | Founder voice email — "what June means to us" | Planned |
| 2026-06-03 | Wed | 12:00 | Organic Social | June Brand Story Push | BTS in the studio Reel | Planned |
| 2026-06-05 | Fri | 10:00 | Email | Father's Day | Pre-launch ("Father's Day collection drops next week") | Planned |
| 2026-06-08 | Mon | 9:00 | Email | Father's Day | Father's Day gift guide launch | Planned |
| 2026-06-08 | Mon | 11:00 | Paid Ad | Father's Day | Meta + TikTok ads activate | Planned |
| 2026-06-08 | Mon | 9:00 | Site Update | Father's Day | Father's Day gift guide collection live + banner | Planned |
| 2026-06-09 | Tue | 12:00 | Organic Social | Father's Day | Gift guide IG carousel post | Planned |
| 2026-06-10 | Wed | 10:00 | Email | June Brand Story Push | Customer story feature | Planned |
| 2026-06-12 | Fri | 10:00 | Email | Father's Day | Mid-campaign with bestsellers | Planned |
| 2026-06-15 | Mon | 10:00 | Email | June Brand Story Push | Behind-the-scenes prose + photos | Planned |
| 2026-06-17 | Wed | 9:00 | Email | Father's Day | Last-shipping-day notice | Planned |
| 2026-06-19 | Fri | 10:00 | Email | Father's Day | 48-hour-left urgency | Planned |
| 2026-06-19 | Fri | 12:00 | Organic Social | Father's Day | Last-day reminder Reel | Planned |
| 2026-06-20 | Sat | 8:00 | Email | Father's Day | Saturday morning scramble | Planned |
| 2026-06-20 | Sat | 8:00 | SMS | Father's Day | Last-call SMS | Planned |

[continues for the full 90 days]

---

## Coordination notes the .docx surfaces

The brief highlights moments where the buyer should run other plugin skills:

- **Memorial Day campaign:** No prior coordination needed; standalone holiday push
- **June Brand Story Push:** Optionally run skill #3 (Landing Page Copywriter) to refresh the About page for the brand story emphasis
- **Father's Day:** Run skill #5 (Ad Creative Generator) for the Father's Day ad concepts. Coordination opportunity with skill #6 if buyer is doing UGC for Father's Day.
- **July 4th:** Standalone — no specific skill coordination required
- **Subscriber-Growth Push:** Triggers skill #7's Welcome flow at higher volume (more new subscribers entering); buyer should verify the Welcome flow is healthy before launching the growth campaign
- **Summer Bestsellers Refresh:** Optionally run skill #1 (Product Description Writer) to refresh PDPs for the featured products

---

## Region behavior

This calendar is US-only (the buyer's default region). If the buyer ships globally, the skill would have:

- Added UK/EU equivalent for the Memorial Day window (Spring Bank Holiday, last Monday of May — falls May 25 in 2026)
- Adjusted Father's Day for AU/NZ markets (their Father's Day is in September, not June — would not appear in this 90-day window)
- Flagged Boxing Day Sales continuation in the calendar window (would have shown if window started earlier in the year)

The skill's region handling means a buyer running this same 90-day request from a UK perspective gets a meaningfully different calendar.

---

## Time-of-day defaults

All times use Pacific time (the brand's default — pulled from `config.store.timezone` if set, otherwise asks the buyer). For Klaviyo Smart Send, the buyer overrides to "send by recipient local time."

---

## Notes on this exemplar

- **A 90-day window naturally captures 6-10 campaigns** for a normal e-commerce brand cadence (not over-saturated, not too sparse)
- **The skill mixes holiday and non-holiday campaigns** — June Brand Story Push is a brand-tentpole that fills the brand-content gap between Memorial Day and Father's Day
- **Subscriber-Growth campaigns get scheduled in lower-intensity windows** (mid-July here) so they don't compete with promo campaigns
- **The Summer Bestsellers Refresh is brand-led, not promo-led** — many sellers default to discount campaigns; the skill suggests content campaigns when promo fatigue is a risk
- **The optional BTS campaign at the end** lets the buyer cleanly decide to include or exclude — the skill doesn't force-fit campaigns the buyer's brand doesn't align with
- **Per-campaign topic briefs in the .docx** include the copy-starter framework so the buyer can run skills #5 or write final copy quickly

This output represents a steady, sustainable e-commerce program — not a "blast every day" approach. The skill biases toward sustainable cadence; the buyer can override with "add more campaigns" if their growth stage warrants it.
