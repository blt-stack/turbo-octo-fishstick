# Q4 BFCM-Focused Calendar — Reference Example

Fictional brand used to show structure. Never reproduce verbatim.

**Brand:** {{brand_name}} (handmade ceramic coffee gear)
**Buyer request:** "Plan my Q4 — focus on BFCM"
**Region:** US
**Window:** October 1, 2026 – December 31, 2026 (92 days)

---

## .xlsx output structure

### Sheet 1: Calendar (chronological)

Sample rows from the 90-day calendar (truncated for example):

| Date | Day | Time | Channel | Campaign | Topic | Owner | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-10-05 | Mon | 9:00 | Email | October Pivot — Fall Restock | Restock announcement: River Stone in Slate | — | Planned | New colorway |
| 2026-10-12 | Mon | 9:00 | Email | Canadian Thanksgiving (CA market only) | Gratitude content, no offer | — | Planned | Skip US sends |
| 2026-10-24 | Sat | 10:00 | Email | Halloween (low intensity) | Trick or treat themed content | — | Planned | Skip if brand doesn't fit |
| 2026-10-31 | Sat | 11:00 | Organic Social | Halloween (low intensity) | Single TikTok if brand fits | — | Planned | — |
| 2026-11-11 | Wed | 9:00 | Email | Veterans Day content | Brief content nod, no promo | — | Planned | — |
| 2026-11-22 | Sun | 10:00 | Email | BFCM 2026 | Pre-Black-Friday teaser email | — | Planned | "Coming Friday" |
| 2026-11-24 | Tue | 10:00 | Email | BFCM 2026 | Wishlist build email (subscriber-exclusive 24h early access) | — | Planned | Drive form signups |
| 2026-11-25 | Wed | 11:00 | Organic Social | BFCM 2026 | Behind-the-scenes IG Reel | — | Planned | UGC opportunity |
| 2026-11-27 | Fri | 6:00 | Email | BFCM 2026 | BLACK FRIDAY launch email | — | Planned | Peak day push |
| 2026-11-27 | Fri | 8:00 | SMS | BFCM 2026 | Black Friday SMS | — | Planned | — |
| 2026-11-27 | Fri | 7:00 | Paid Ad | BFCM 2026 | Meta + TikTok ads activate | — | Planned | Peak budget |
| 2026-11-27 | Fri | 8:00 | Site Update | BFCM 2026 | Homepage hero swap + popup + announcement bar | — | Planned | All live |
| 2026-11-27 | Fri | 12:00 | Organic Social | BFCM 2026 | Black Friday hype IG post + Reel + TikTok | — | Planned | Cross-post |
| 2026-11-28 | Sat | 11:00 | Email | BFCM 2026 | Saturday continuation | — | Planned | — |
| 2026-11-29 | Sun | 11:00 | Email | BFCM 2026 | Sunday mid-event reminder | — | Planned | Lower intensity |
| 2026-11-30 | Mon | 9:00 | Email | BFCM 2026 | CYBER MONDAY launch email | — | Planned | Second peak day |
| 2026-11-30 | Mon | 11:00 | SMS | BFCM 2026 | Cyber Monday SMS | — | Planned | — |
| 2026-12-01 | Tue | 10:00 | Email | BFCM 2026 | Cyber Tuesday extension | — | Planned | — |
| 2026-12-03 | Thu | 10:00 | Email | BFCM 2026 | Cyber Week last-call | — | Planned | — |
| 2026-12-05 | Sat | 6:00 | Email | BFCM 2026 | Last day of Cyber Week | — | Planned | — |
| 2026-12-05 | Sat | 6:00 | SMS | BFCM 2026 | Last-day SMS | — | Planned | — |
| 2026-12-06 | Sun | 9:00 | Email | BFCM 2026 | Wrap-up + thank-you | — | Planned | End of campaign |
| 2026-12-15 | Tue | 9:00 | Email | Last-Shipping Push | "Last day to ship for Christmas" | — | Planned | Real urgency |
| 2026-12-17 | Thu | 9:00 | Email | Last-Shipping Push | "Cutting it close" reminder | — | Planned | — |
| 2026-12-24 | Thu | 9:00 | Email | Christmas Eve | Warm holiday content | — | Planned | Quiet/no offer |
| 2026-12-26 | Sat | 9:00 | Email | Boxing Day (post-holiday) | Post-Christmas reset sale | — | Planned | Growing in US |
| 2026-12-30 | Wed | 10:00 | Email | NYE wrap-up | Year-end thank you | — | Planned | — |

Color-coding applies:
- BFCM rows highlighted green
- Holiday-named campaigns in pale yellow
- Status column color-coded as rows move through Planned → Drafted → Scheduled → Sent

### Sheet 2: Campaigns (aggregate view)

| Campaign Name | Type | Start | End | Days | Emails | SMS | Paid Ads | Organic | Site | Total | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| October Pivot — Fall Restock | Restock | 10-05 | 10-09 | 5 | 2 | 1 | 1 | 2 | 1 | 7 | Planned |
| Halloween (low intensity) | Holiday | 10-24 | 10-31 | 8 | 1 | 0 | 0 | 1 | 0 | 2 | Planned |
| Veterans Day content | Holiday | 11-11 | 11-11 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | Planned |
| BFCM 2026 | Holiday | 11-22 | 12-06 | 15 | 11 | 4 | 5 | 12 | 4 | 36 | Planned |
| Last-Shipping Push | Holiday | 12-15 | 12-22 | 8 | 4 | 2 | 1 | 2 | 1 | 10 | Planned |
| Christmas Eve content | Holiday | 12-24 | 12-24 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | Planned |
| Boxing Day (post-holiday) | Holiday | 12-26 | 12-30 | 5 | 4 | 1 | 1 | 2 | 1 | 9 | Planned |
| NYE wrap-up | Holiday | 12-30 | 12-31 | 2 | 1 | 0 | 0 | 1 | 0 | 2 | Planned |

8 campaigns, 68 sends total across all channels.

### Sheet 3: Monthly view (matrix)

Heat-map of activity density. One row per day, columns for each channel showing send count. Weekends shaded slightly. BFCM week shows up as the densest column on Nov 27 (6 sends across 5 channels).

---

## .docx output excerpt

```
{{brand_name}} — Campaign Calendar Brief
Generated 2026-05-22 · Region: United States · Window: 2026-10-01 – 2026-12-31
Total campaigns: 8
Total sends across channels: 68

═════════════════════════════════════════════════
EXECUTIVE SUMMARY
═════════════════════════════════════════════════

Q4 2026 leans heavily on BFCM (36 sends, 53% of the calendar). The largest
revenue opportunity is the 8-day Black Friday → Cyber Week window — buyer
should expect this to generate 20-30% of full-year revenue if executed
well. Secondary push at Last-Shipping (Dec 15-22) captures Christmas-gift
buyers. Boxing Day (Dec 26-30) is included as a growing US opportunity
worth ~3-5% of program revenue.

Non-BFCM intensity is intentionally lower — Q4 fatigue from over-sending
during BFCM lowers Boxing Day conversion when sellers don't rest. The 7-day
"quiet zone" Dec 8-14 (between BFCM and Last-Shipping) is deliberate.

═════════════════════════════════════════════════
CAMPAIGN 4: BFCM 2026  (2026-11-22 – 2026-12-06)
═════════════════════════════════════════════════
Type: Holiday
Playbook: BFCM (Pattern 3 — extended 14-day campaign)
Goal: Drive 25-35% of annual revenue. Maximize subscriber engagement to
build the post-BFCM customer base for 2027.
Audience: Full engaged segment + early-access for SMS-opted-in subscribers
+ extra creative for high-LTV customers.

Topic brief:
BFCM 2026 is the year's biggest commercial moment. The campaign opens with
brand-story warming (Nov 22) before the Wishlist-build email (Nov 24) that
captures the 24-hour-early-access list. Black Friday launches with the
hero offer (30% off sitewide). Cyber Week sustains daily sends through
Dec 5 with diminishing intensity. Boxing Day is treated as a separate
campaign Dec 26-30.

The brand-voice frame: this is the year we discount, AND we're still
{{brand_name}}. Hand-thrown ceramic at 30% off doesn't change what it is.
The campaign emphasizes scarcity (real inventory limits, not fake
urgency), studio context (BFCM week behind-the-scenes Reels), and a
"thank-you to our community" through-line that grounds the promotional
energy in warmth.

Send schedule:
[full table from .xlsx Sheet 1, filtered to this campaign]

Copy starters:
Email subject lines:
- Coming Friday: our biggest collection moment of the year
- 24 hours early — for our list only
- We rarely do this. Friday: 30% off everything.
- BLACK FRIDAY: 30% off the whole shop, including the bestsellers
- Cyber Monday — we're back at it for one more day

SMS drafts:
- Hey [first name], black friday at {{brand_name}} starts now: 30% off everything. [link]. Reply STOP to opt out.
- last day of cyber week, last chance at 30% off: [link]. Reply STOP to opt out.

Paid ad hooks (across 5 archetypes):
- Problem-aware: That $400 espresso machine in your cabinet doesn't need to be there
- Social-proof: 12,000+ five-star reviews. 30% off this weekend.
- Transformation: Slow Saturday mornings — at 30% off through Cyber Monday
- Curiosity-gap: We don't usually run sales. This week is the exception.
- Contrarian: Skip the espresso machine sale. The handmade alternative is 30% off.

Organic social post angles:
- IG Reel: behind-the-scenes — packing BFCM orders in the studio
- TikTok: founder explaining why they do BFCM their way (no false urgency)
- IG Story sequence: hour-by-hour Black Friday studio recap

Site banner copy options:
- 30% off everything · Black Friday – Cyber Monday · Free shipping over $50
- Our biggest week of the year · 30% off through Dec 5 · Code applied at checkout

[...repeats for each of the 8 campaigns]
```

---

## Notes on this exemplar

- **BFCM is the dominant campaign** — 36 sends out of 68 total. The skill correctly weighted it.
- **Halloween is low-intensity** for a coffee brand (it's not a costume / candy category). The skill defaulted appropriately.
- **Veterans Day** gets a content-only treatment, not a promo. Same with Christmas Eve.
- **Boxing Day** is included as a US opportunity (the holiday template flagged it as "growing in US")
- **The quiet zone Dec 8-14** is intentional — sender fatigue is real, and the skill recommends rest periods
- **Each campaign has playbook-driven send cadence** — BFCM uses Pattern 3, restocks use Pattern 2, holidays use Pattern 1
- **Copy starters at the campaign level** match the 5-archetype framework used across skills #5/#6 — coordination across the program
- **Channel mix per campaign** varies by campaign type — BFCM has all 5 channels active; Halloween has only 2

The `.xlsx` is the operational tracker the buyer updates as they execute. The `.docx` is the creative brief they share with VAs / collaborators or use as a reference when running skills #5/#7 to expand specific sends.
