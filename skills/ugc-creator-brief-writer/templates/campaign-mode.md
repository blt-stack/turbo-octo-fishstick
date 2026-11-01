# Campaign Mode — Multi-Creator Brief Structure

When the buyer is working with multiple creators simultaneously (a "wave" or "roster" or "matched campaign" of creators), the skill switches to campaign mode and produces a different deliverable bundle.

The goal: each creator gets a brief that's clearly customized for them, no two creators are shooting the same hook or the same shot list, and the buyer gets a single workbook to manage the whole campaign.

---

## When campaign mode triggers

The skill detects campaign mode from any of these signals:

- The user names multiple creators (e.g., "I'm working with @amyhouse, @lifestylebymeg, and @threecutekids")
- The user says "campaign," "wave," "roster," "batch," "multi-creator"
- The user provides a list of 3+ creators
- The user references a creator marketplace they've matched on (Whalar, Aspire, LTK, Insense, Cartwheel, Trend, GRIN, CreatorIQ)

In ambiguous cases, ask: "Just one creator, or a campaign? If multiple, how many and which platforms?"

---

## Deliverable bundle in campaign mode

Three files instead of one:

1. **Master brief** (`.docx`) — the canonical brief. Contains all 10 hooks, the full b-roll shot list, and all do's-and-don'ts. Used by the buyer for reference and as the source-of-truth for what's in the campaign.

2. **Per-creator briefs** (`.docx` each, one per creator) — lightly personalized version of the master. Same product context, same compliance section, but:
   - Each creator gets 2-3 *assigned* hooks (not all 10)
   - Each creator gets their angle archetype focus (their assigned subset of the 5 archetypes)
   - A personalized "Your role in this campaign" intro paragraph
   - 5-6 shots from the master shot list (not all 8-10)

3. **Hook assignment workbook** (`.xlsx`) — the project-management view of the campaign. One row per creator, columns for handle, assigned hooks, assigned archetype, platform, due date, payment terms, status. Buyer uses this to track the campaign and to make sure no two creators are shooting the same hook.

---

## Hook assignment logic

When 10 hooks (2 per archetype × 5 archetypes) are assigned across N creators, the algorithm:

1. **For 2-3 creators:** each creator gets 2-3 hooks from 2 different archetypes. Total coverage: 4-9 of the 10 hooks; 4-5 of the 5 archetypes used.
2. **For 4-5 creators:** each creator gets 2 hooks from 1 archetype. Total: every archetype covered by at least one creator.
3. **For 6-10 creators:** archetypes assigned in round-robin. Each creator gets 1-2 hooks. Same archetype may be assigned to 2 creators, but with different specific hooks.
4. **For 10+ creators:** generate additional hooks (up to 20 total) so no two creators get the same exact hook. Or split into "waves" with the same hook list.

The algorithm should also factor in (when known):
- **Creator content style:** a creator whose existing content skews aspirational gets the Transformation archetype; one who skews contrarian/educational gets the Contrarian archetype
- **Creator platform:** if the creator's primary platform is TikTok, give them hooks that work in TikTok's first-1-second timing; if YouTube Shorts, hooks that can build over 3-5 seconds
- **Creator demographic match:** if the creator's audience skews younger / older / niche, match the archetype to their audience

---

## Per-creator personalization

Each per-creator brief includes a personalized intro paragraph at the top:

```
Hey [creator name],

Excited to be working with you on this. We picked you for the [archetype name]
angle of our [product name] campaign because [reason — usually a sentence
about their style/audience].

Below is your assigned brief. The hooks at the top are yours — please pick
the one that lands best for you and your audience. The rest of the brief
(b-roll, talking points, do's-and-don'ts) is the same across the campaign,
so the deliverables stay consistent.
```

The personalization paragraph should NOT be obviously templated. If the buyer hasn't provided detail on each creator's style, ask before generating per-creator intros — generic personalization reads worse than no personalization.

---

## Campaign workbook (`.xlsx`) structure

Three sheets:

### Sheet 1: Creator Roster

| Column | Notes |
|---|---|
| Creator handle | @username |
| Real name | Optional |
| Platform | TikTok / Reels / Stories / Shorts |
| Assigned hooks | Pipe-separated list of the 2-3 hooks assigned |
| Assigned archetype(s) | e.g., "Problem-aware, Transformation" |
| Shoot deadline | Date |
| Delivery deadline | Date |
| Payment terms | Flat fee, commission %, or "gifted" |
| Usage rights duration | "3 months Spark," "perpetual organic," etc. |
| Status | Pending / Briefed / Shooting / Delivered / Approved / Published / Paid |
| Notes | Anything campaign-specific |

The Status column is the buyer's workflow tracker — they update as the campaign progresses.

### Sheet 2: Hook Library

The 10 (or 20) hooks generated, with columns:

| Column | Notes |
|---|---|
| Hook # | 1-10 |
| Archetype | Problem-aware / Social-proof / Transformation / Curiosity gap / Contrarian |
| Hook (spoken line) | The line itself |
| Recommended on-screen text | Text overlay version |
| Assigned to | Creator handles (one or more) |
| Status | Assigned / Unassigned |

The "Assigned to" column lets the buyer see at-a-glance which hooks haven't been deployed yet — useful when a creator drops out and the buyer reassigns their hook.

### Sheet 3: Campaign Calendar

A simple month-view-style table showing what's due when:

| Date | Creator | Milestone |
|---|---|---|
| 2026-05-22 | All | Briefs sent |
| 2026-05-26 | @amyhouse | Pre-shoot sync |
| 2026-05-28 | @amyhouse | Delivery deadline |
| 2026-05-29 | @lifestylebymeg | Delivery deadline |
| ... | ... | ... |

Sorted chronologically. Used by the buyer to know what's coming up.

---

## Master brief vs per-creator brief — what's different

| Section | Master brief | Per-creator brief |
|---|---|---|
| Title | "Campaign Master Brief: [Campaign Name]" | "UGC Brief: [Product] for [Creator]" |
| Intro | Campaign overview ("we're producing 5 videos across 5 creators...") | Personalized intro to that creator |
| Hooks | All 10 | Their assigned 2-3 only |
| Archetype focus | All 5 | Their assigned 1-2 |
| B-roll shot list | All 8-10 shots | Their assigned 5-6 shots |
| Talking points | Same | Same |
| Tone / voice | Same | Same |
| Do's and don'ts | Same | Same |
| Deliverables | Per-creator counts noted | Their specific deliverables |
| Timeline | Master timeline (all dates) | Their specific dates |
| Usage rights / FTC | Same | Same |

Per-creator briefs are 60-70% the length of the master brief. The differentiation isn't in adding content; it's in subtracting content the creator doesn't need.

---

## Why subset hooks vs giving everyone all 10

If every creator in a campaign gets all 10 hooks, two things happen:
1. They each pick the same most-obvious hook (usually Problem-aware or Transformation)
2. The campaign produces 5 near-identical videos

By assigning specific hooks per creator, the buyer guarantees variety across the campaign. The .xlsx workbook makes this enforceable.

If a creator says "I don't like any of my assigned hooks," the workbook lets the buyer see what's still unassigned and reassign accordingly.

---

## Diversifying b-roll across creators

The master shot list has 8-10 shots. Per-creator briefs get 5-6 each. The selection logic:

- **Every creator** gets the 5-shot foundation (establishing, hero close-up, in-use, before/after-or-reaction, talking-head)
- **Each creator** gets 1-2 product-specific shots different from the others

This ensures variety in the campaign's b-roll without making any individual creator's shot list feel arbitrary.

---

## Common pitfalls in campaign mode

- **Everyone gets the same brief** — campaign produces 5 identical videos, defeats the purpose of multi-creator
- **Hooks too templated** — generic personalization is worse than no personalization
- **No workbook to track who's doing what** — buyer loses track at 4+ creators
- **Buyer changes the campaign mid-flight without updating creators** — version control matters; the workbook should be the single source of truth
- **Over-personalizing** — if the buyer doesn't know each creator's style, don't fake it. Generic-but-respectful per-creator briefs are fine
