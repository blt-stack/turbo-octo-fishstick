# Campaign Mode — Reference Example

Fictional 5-creator campaign used to show structure. Never reproduce verbatim.

**Campaign:** River Stone Pour-Over — Spring Wave 1
**Brief type:** Paid UGC (Spark Ads)
**Platforms:** TikTok + Reels (cross-posted)
**Creators:** 5

---

## What gets generated in campaign mode

For a 5-creator campaign, the skill produces **7 files**:

1. `river-stone_campaign-master-brief_2026-05-22.docx` — Master brief
2. `river-stone_brief_@amyhouse_2026-05-22.docx` — Per-creator brief #1
3. `river-stone_brief_@lifestylebymeg_2026-05-22.docx` — Per-creator brief #2
4. `river-stone_brief_@coffeebysamantha_2026-05-22.docx` — Per-creator brief #3
5. `river-stone_brief_@nightowlbarista_2026-05-22.docx` — Per-creator brief #4
6. `river-stone_brief_@threecutekids_2026-05-22.docx` — Per-creator brief #5
7. `river-stone_campaign-workbook_2026-05-22.xlsx` — Campaign workbook (3 sheets)

All seven save to `config.output_folder`.

---

## Master brief structure (highlights)

The master brief contains everything — all 10 hooks, the full 10-shot b-roll list, the complete do's-and-don'ts, the full FTC + usage rights. It reads like the single-paid example but with these additions:

```
Campaign Master Brief: River Stone Pour-Over — Spring Wave 1
Generated 2026-05-22 · Brand: {{brand_name}} · Brief type: Paid UGC · Platforms: TikTok, Reels

CAMPAIGN OVERVIEW

We're producing 5 paid UGC videos across 5 creators, targeting TikTok and
Instagram Reels. Each creator gets 2-3 hooks from the master library below,
matched to their style and audience. The goal is to test 5 distinctly
different angle directions and identify which converts best for River Stone
on cold paid traffic.

All videos will run as Spark Ads on Meta and TikTok for 3 months. Usage
rights and FTC disclosure terms below apply to every creator's deliverable.

[...rest of brief — full 10 hooks, all 10 b-roll shots, full compliance section...]

CREATOR ASSIGNMENT SUMMARY
| Creator | Platform | Assigned Hooks | Archetype Focus | Shoot By |
|---|---|---|---|---|
| @amyhouse | TikTok | #1, #4 | Problem-aware + Social-proof | May 26 |
| @lifestylebymeg | Reels | #5, #6 | Transformation | May 27 |
| @coffeebysamantha | TikTok | #7, #8 | Curiosity gap | May 26 |
| @nightowlbarista | TikTok | #9, #10 | Contrarian | May 28 |
| @threecutekids | Reels | #2, #3 | Problem-aware + Social-proof | May 27 |
```

---

## Per-creator brief structure (example: @amyhouse)

Each per-creator brief is 60-70% the length of the master. Same product context, same compliance sections, but:

- Personalized intro
- Only their assigned 2 hooks shown (not all 10)
- Only their assigned 5-6 b-roll shots (not all 10)
- Their specific deadlines and payment terms

```
UGC Brief: River Stone Pour-Over — @amyhouse
Generated 2026-05-22 · Brand: {{brand_name}} · Brief type: Paid UGC · Platforms: TikTok
Campaign: River Stone Pour-Over — Spring Wave 1

══════════════════════════════════════════════════
PERSONALIZED INTRO
══════════════════════════════════════════════════

Hey Amy,

Excited to be working with you on the River Stone Spring Wave. We picked you
for the Problem-aware + Social-proof angle of the campaign because your TikTok
content does a great job of opening with a real, named frustration before
introducing the solution — and your audience trusts your taste.

Below are your assigned 2 hooks. Pick the one that lands best for you. The
rest of the brief (b-roll, talking points, do's-and-don'ts) is the same across
the campaign, so all 5 deliverables stay consistent.

══════════════════════════════════════════════════
HOOKS (your 2 assigned)
══════════════════════════════════════════════════

| # | Archetype | Spoken line | On-screen text | Notes |
|---|---|---|---|---|
| 1 | Problem-aware | "I bought a $400 espresso machine and now it lives in a cabinet because of this." | "$400 mistake → $68 fix" | Deliver flat, mildly self-deprecating |
| 4 | Social-proof | "Featured in Sprudge's 2026 coffee gear guide — and it's $68." | "Sprudge picked it · $68" | Punch the "$68" for impact |

[...rest of brief: overview, b-roll (5 shots assigned to Amy), talking points,
do's-and-don'ts, deliverables (1 TikTok, 30s), timeline (shoot May 26, deliver
May 28), FTC + usage rights, brand safety, compensation ($600 + 3mo Spark)...]
```

Each of the other 4 creators gets a similar brief, with their own 2 hooks,
their own 5-6 shots from the master list, and their own personalized intro.

---

## Campaign workbook (.xlsx) structure

### Sheet 1: Creator Roster (the main planning view)

| Creator handle | Real name | Platform | Assigned hooks | Assigned archetypes | Shoot deadline | Delivery deadline | Payment terms | Usage rights duration | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| @amyhouse | Amy Houseman | TikTok | #1: I bought a $400 espresso...<br>#4: Featured in Sprudge's 2026... | Problem-aware, Social-proof | 2026-05-26 | 2026-05-28 | $600 + 3mo Spark | 3 months Spark | Pending | Strong opener style |
| @lifestylebymeg | Megan Lefranc | Reels | #5: Slow Saturday mornings...<br>#6: Three minutes from kettle... | Transformation | 2026-05-27 | 2026-05-29 | $750 + 3mo Spark | 3 months Spark | Pending | Aesthetic-lead content |
| @coffeebysamantha | Sam Tomás | TikTok | #7: There's one thing missing...<br>#8: I've been making pour-over wrong... | Curiosity gap | 2026-05-26 | 2026-05-28 | $500 + 3mo Spark | 3 months Spark | Pending | Educational hook specialist |
| @nightowlbarista | Jordan Lee | TikTok | #9: Espresso machines are over...<br>#10: Paper coffee filters are quietly... | Contrarian | 2026-05-28 | 2026-05-30 | $700 + 3mo Spark | 3 months Spark | Pending | Confident on-camera, good for contrarian |
| @threecutekids | Riley Park | Reels | #2: Pour-over coffee is intimidating...<br>#3: 1,247 reviews said this is... | Problem-aware, Social-proof | 2026-05-27 | 2026-05-29 | $650 + 3mo Spark | 3 months Spark | Pending | Family-context fit |

The Status column starts at "Pending" and updates as the buyer moves each creator through: Pending → Briefed → Shooting → Delivered → Approved → Published → Paid. Each status has a different cell background color for at-a-glance triage.

### Sheet 2: Hook Library (assignment tracking)

| Hook # | Archetype | Spoken line | On-screen text | Assigned to | Status |
|---|---|---|---|---|---|
| 1 | Problem-aware | I bought a $400 espresso machine and now it lives in a cabinet because of this. | $400 mistake → $68 fix | @amyhouse | Assigned |
| 2 | Problem-aware | Pour-over coffee is intimidating until you try the one that's actually made for a real morning. | Pour-over, but easy | @threecutekids | Assigned |
| 3 | Social-proof | 1,247 reviews said this is the pour-over that converted them — here's why. | 1,247 reviews. One pour-over. | @threecutekids | Assigned |
| 4 | Social-proof | Featured in Sprudge's 2026 coffee gear guide — and it's $68. | Sprudge picked it · $68 | @amyhouse | Assigned |
| 5 | Transformation | Slow Saturday mornings start exactly like this. | Saturday. 7:34am. | @lifestylebymeg | Assigned |
| 6 | Transformation | Three minutes from kettle on to coffee in mug. Every morning, no thinking. | Three minutes. Every morning. | @lifestylebymeg | Assigned |
| 7 | Curiosity gap | There's one thing missing from your morning routine and it isn't a machine. | Hint: not a machine | @coffeebysamantha | Assigned |
| 8 | Curiosity gap | I've been making pour-over wrong for two years — turns out it was the dripper. | Was making pour-over wrong | @coffeebysamantha | Assigned |
| 9 | Contrarian | Espresso machines are over. Hand-brewed coffee is the actually-good way. | RIP espresso machine 2010-2024 | @nightowlbarista | Assigned |
| 10 | Contrarian | Paper coffee filters are quietly the most wasteful thing in your kitchen. | Look in your trash. | @nightowlbarista | Assigned |

(Unassigned hooks get a yellow background — useful when a creator drops out and the buyer needs to reassign their hook to a backup creator.)

### Sheet 3: Campaign Calendar (chronological view)

| Date | Creator | Milestone |
|---|---|---|
| 2026-05-22 | All | Briefs sent |
| 2026-05-23 | @amyhouse | Pre-shoot Q&A call |
| 2026-05-24 | All | Approval-flow reminder |
| 2026-05-26 | @amyhouse | Shoot deadline |
| 2026-05-26 | @coffeebysamantha | Shoot deadline |
| 2026-05-27 | @lifestylebymeg | Shoot deadline |
| 2026-05-27 | @threecutekids | Shoot deadline |
| 2026-05-28 | @amyhouse | Delivery deadline (raw + edit) |
| 2026-05-28 | @coffeebysamantha | Delivery deadline |
| 2026-05-28 | @nightowlbarista | Shoot deadline |
| 2026-05-29 | @lifestylebymeg | Delivery deadline |
| 2026-05-29 | @threecutekids | Delivery deadline |
| 2026-05-30 | @nightowlbarista | Delivery deadline |
| 2026-06-02 | All | Final edits approved + posts go live |
| 2026-06-03 | All | Spark Ads boosted |

The buyer uses this to know what's coming up day-by-day.

---

## Notes on this exemplar

- **5 creators, 10 hooks, 5 archetypes — each creator gets 2 hooks from 1-2 archetypes** so no two creators are shooting the same hook
- **Each creator's archetype assignment is matched to their content style** (Amy gets Problem-aware because her existing TikTok content opens with frustrations; Nightowl gets Contrarian because they have a confident, declarative delivery style)
- **The .xlsx is the buyer's project-management tool** — they update Status as creators move through the workflow
- **Per-creator briefs are 60-70% the length of the master** — the buyer doesn't make a creator wade through 10 hooks to find their 2
- **Calendar is auto-sorted chronologically** — eliminates the "wait when is X due?" problem
- **Pay amounts are creator-specific** — different creators have different rates; the workbook captures it once and tracks it

The campaign workbook is the highest-value artifact in campaign mode. Most buyers managing 5+ creators do this in a half-broken Google Sheet they made themselves. Shipping a structured one with hook-to-creator visibility built in is the operational win.
