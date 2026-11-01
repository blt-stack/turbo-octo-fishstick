---
name: campaign-calendar-planner
description: >
  Builds a 90-day rolling marketing campaign calendar for e-commerce sellers across four channels:
  email + SMS, paid social, organic social, and site updates. Holiday-aware for US, UK/EU,
  Canada/AU/NZ. Includes 7 reusable campaign playbooks (BFCM, product launch, restock, flash sale,
  anniversary, subscriber-growth, seasonal tentpole) and copy starters per campaign. Outputs an .xlsx
  calendar grid (operational tracker, 3 sheets) plus a .docx topic brief (creative reference). Use
  this skill when the user mentions campaign calendar, marketing calendar, content calendar, 'plan my
  Q4,' 'BFCM plan,' '90-day plan,' 'promo schedule,' 'what should I send this month,' or 'I need a
  marketing plan.'
---

# Campaign Calendar Planner

Builds a 90-day rolling marketing calendar for one-off promotional campaigns. Schedules sends across 4 channels per campaign. Outputs `.xlsx` grid + `.docx` topic briefs with copy starters.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Detect time horizon.** Default 90 days rolling from today. Custom ranges allowed.
3. **Detect region.** Default US. Buyer can override.
4. **Gather context.** Brand category + product catalog + buyer's specific campaign asks.
5. **Read shared caches.** Keywords (subject-line SEO) + UGC hooks (archetype-coordinated copy starters).
6. **Build the calendar.** Holiday-driven campaigns + buyer-specific campaigns (launches, restocks) + tentpole brand campaigns (anniversaries).
7. **Generate per-campaign sends.** For each campaign, produce a multi-step send schedule across enabled channels.
8. **Render outputs.** `.xlsx` calendar grid + `.docx` topic briefs with copy starters.
9. **Report back.** File paths, calendar summary, top revenue opportunities, next step.

---

## Step 1: First-run check

Look for `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`. If missing, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

---

## Step 2: Detect time horizon

**Default: 90 days rolling from today.** Buyer overrides:

| Buyer says | Range |
|---|---|
| "next 90 days," "this quarter" | 90 days from today |
| "plan my Q4," "October to December" | Q4 of current year (Oct 1 – Dec 31) |
| "Black Friday plan" | Oct 15 – Dec 5 (BFCM-focused window) |
| "Mother's Day plan" | 6 weeks before through 1 week after the appropriate Mother's Day date |
| "from [date] to [date]" | Custom range as specified |
| "the rest of the year" | Today through Dec 31 |

Confirm the range out loud before generating.

---

## Step 3: Detect region

**Default: US.** Buyer overrides:

| Region | Detection signal |
|---|---|
| US | Default; or buyer mentions "USA," "US holidays," "Black Friday" |
| UK / EU | Buyer mentions "Boxing Day," "Bank Holidays," "UK Mother's Day," "Europe" |
| Canada | Buyer mentions Canada, Canada Day, Victoria Day |
| Australia / NZ | Buyer mentions "Aussie," Australia Day, ANZAC Day |
| Multi-region (ships globally) | Buyer mentions "ship internationally," "global" — skill loads all 3 regional calendars and notes per-campaign which regions each applies to |

Read the matching holiday template(s) from `templates/`:
- `templates/us-holidays.md`
- `templates/uk-eu-holidays.md`
- `templates/canada-au-nz-holidays.md`

Each holiday template lists retail-relevant dates with send-timing recommendations (e.g., "BFCM: pre-tease Nov 22, soft launch Black Friday, full push Black Friday + Cyber Monday + Giving Tuesday, last call Dec 1").

---

## Step 4: Gather context

The skill needs:

- **From Shopify (when connected):** product catalog (so campaigns can reference real SKUs), recent sales data (for restock-focused campaigns), seasonal product flags (which products spike when)
- **From Klaviyo (when connected):** broadcast send history (so the skill doesn't recommend campaigns that overlap with already-scheduled sends), subscriber list sizes per segment
- **From config:** brand voice, audience, primary category, output folder
- **From buyer paste/conversation:** specific campaigns the buyer knows about (e.g., "we're launching a new mug set in early November"), promotional preferences (does the brand discount? what % is brand-typical?), brand events (founders' anniversary, milestone celebrations)

If anything's missing, ask one round of targeted questions before generating.

---

## Step 5: Read shared caches

### Cache A: Keywords (read-only, from skill #2)

**Path:** `~/.the-ecommerce-seller/cache/keywords/{product-identifier}.json`

Use `scripts/keyword_cache_reader.py`. For campaigns that reference specific products (product launch, restock, post-launch nurture), keywords influence subject-line and ad-headline copy starters.

### Cache B: UGC hooks (read-only)

**Path:** `~/.the-ecommerce-seller/cache/ugc_hooks/{product-identifier}.json`

Use `scripts/ugc_hook_cache.py`. The 5 archetype hooks (problem-aware, social-proof, transformation, curiosity-gap, contrarian) become copy starters for campaign emails and ads. Coordination across campaigns + automated flows + paid ads + UGC keeps the brand voice unified.

When both caches are empty for relevant products, the skill generates fresh copy starters using the same 5-archetype framework.

---

## Step 6: Build the calendar

Three campaign sources combine into the calendar:

### Source 1: Holiday-driven campaigns

From the regional holiday template, pick which holidays are retail-relevant for the buyer's category. Not every holiday warrants a campaign — a coffee brand doesn't need a Father's Day campaign unless coffee fits the category narrative; a skincare brand needs a heavy Mother's Day campaign.

Read `templates/campaign-playbooks.md` for the standard "campaign shape" per holiday type — typical pre-launch, launch, mid-campaign, last-day-urgency, post-event recap structure.

### Source 2: Buyer-specific campaigns

- Product launches (buyer specifies dates)
- Restock pushes (when a sold-out product comes back)
- Brand anniversaries (founding date, founders' birthdays)
- Collection drops
- Subscription pushes (if buyer offers Subscribe & Save)
- Email-list-growth campaigns (e.g., "free shipping for new subscribers" push)

### Source 3: Tentpole brand campaigns

- BFCM (universally important)
- A spring or summer "evergreen" campaign for non-holiday months
- An end-of-year "thank you" campaign (Dec 28-31)
- A January "new year, new collection" campaign

Combine all three sources. Conflict-check: don't schedule a flash sale during BFCM week (the audience is already in promo mode); don't schedule a product launch during a major holiday (the launch gets buried).

The result: a calendar with 8-20 campaigns over 90 days (varies by buyer's promotional rhythm). Per category benchmarks:

| Category | Typical 90-day campaign count |
|---|---|
| DTC apparel | 12-20 |
| Beauty / skincare | 10-15 |
| Food / beverage | 8-12 |
| Home / decor | 6-10 |
| Hobbyist / specialty | 4-8 |

---

## Step 7: Generate per-campaign sends

For each campaign in the calendar, generate a multi-step send schedule across enabled channels. Read `templates/send-cadence.md` for the standard cadence patterns:

### Typical campaign send structure

| Phase | Days from launch | Channels |
|---|---|---|
| Pre-launch tease | -7 to -3 | Email, organic social |
| Pre-launch reminder | -1 | Email, SMS, organic social |
| Launch day | 0 | Email, SMS, paid ads, organic social, site banner |
| Mid-campaign | +2 to +5 | Email, paid ads, organic social |
| Last-day urgency | -1 to 0 from end | Email, SMS, paid ads, site popup |
| Post-campaign | +1 to +3 | Email (thank you / wrap-up) |

For shorter campaigns (flash sale, 24-hour push), compress this. For longer campaigns (BFCM week, holiday season), extend.

### Per-send specification

For each scheduled send, the skill produces:

- **Date** and time (with timezone)
- **Channel** (email broadcast, SMS, paid ad, organic post, site update)
- **Campaign name** (e.g., "BFCM 2026 — Pre-launch tease")
- **Topic** (one paragraph: what this send is about)
- **Copy starters:**
  - For email: 2-3 subject line options + preview text suggestions
  - For SMS: 1-2 short message drafts (with TCPA opt-out)
  - For paid ads: 3-5 ad hooks across archetypes (matches skill #5's framework)
  - For organic social: 2-3 post angles
  - For site updates: banner/popup copy options

Read `templates/copy-starters.md` for the archetype framework and `templates/channel-conventions.md` for per-channel writing rules.

---

## Step 8: Render outputs

### Output 1: `.xlsx` calendar grid

Use `scripts/render_calendar_xlsx.py`. Three sheets:

**Sheet 1: Calendar (chronological view)** — one row per scheduled send across all channels, sorted by date.

Columns:
- Date
- Day of week
- Time (with timezone)
- Channel (Email | SMS | Paid Ads | Organic Social | Site Update)
- Campaign name
- Topic (one-line summary)
- Owner (blank by default, buyer fills in)
- Status (Planned | Drafted | Scheduled | Sent — buyer updates)
- Notes

Conditional formatting:
- Holidays highlighted in pale yellow
- BFCM week highlighted in green
- Status column color-coded (Planned = white, Drafted = blue, Scheduled = light green, Sent = dark green)

**Sheet 2: Campaigns (campaign view)** — one row per campaign, with aggregate send counts per channel.

Columns:
- Campaign name
- Campaign type (Holiday | Product Launch | Restock | Flash Sale | Brand Event | Other)
- Start date
- End date
- Email + SMS send count
- Paid ad concept count
- Organic post count
- Site updates
- Status

**Sheet 3: Monthly view (matrix)** — one row per day, columns per channel. Quick at-a-glance heatmap of activity density.

### Output 2: `.docx` topic briefs

Use `scripts/render_calendar_docx.py`. Structure:

```
[Brand name] — 90-Day Campaign Calendar
Generated [date] · Region: [US | UK/EU | Canada/AU/NZ | Global]
Calendar window: [start date] – [end date]
Total campaigns: [N]
Total sends across channels: [M]

═════════════════════════════════════════════════
EXECUTIVE SUMMARY
═════════════════════════════════════════════════
- [N] campaigns scheduled
- Largest revenue moments: [BFCM, Mother's Day, Product Launch X]
- Channel mix: [email/SMS X%, paid ads Y%, organic Z%, site W%]
- Recommended priority: [based on category benchmarks]

═════════════════════════════════════════════════
CAMPAIGN 1: [Campaign name] · [Start - End]
═════════════════════════════════════════════════
Type: [Holiday / Launch / Restock / etc.]
Goal: [One sentence on the conversion goal]
Audience: [Primary segment from config]

Topic brief:
[2-3 paragraphs describing what the campaign is about, the narrative
arc, the brand-voice hook the campaign hangs on]

Send schedule:
| Date | Channel | Topic |
| ... | ... | ... |

Copy starters:
- Email subject lines:
  - [...]
  - [...]
  - [...]
- SMS:
  - [...]
- Paid ad hooks (across 5 archetypes):
  - Problem-aware: [...]
  - Social-proof: [...]
  - Transformation: [...]
  - Curiosity-gap: [...]
  - Contrarian: [...]
- Organic social angles:
  - [...]
- Site banner copy options:
  - [...]

[Repeat for every campaign]
```

Save to `config.output_folder` with filenames:
- `{brand-slug}_campaign-calendar_{start-date}-to-{end-date}.xlsx`
- `{brand-slug}_campaign-briefs_{start-date}-to-{end-date}.docx`

---

## Step 9: Report back

Tell the buyer:
1. Where both files are (`computer://` links)
2. Calendar summary: campaign count, total sends, biggest revenue moments
3. Whether keywords + UGC hooks were pulled from shared caches (coordination signals)
4. One suggested next step:
   - For each near-term campaign (in the next 14 days), suggest running skills #5 (Ad Creative) and #7 (Email Flow Architect's broadcast mode — when that ships) to expand the copy starters into full sends
   - If the buyer hasn't run skill #2 / #5 / #6 yet: "Run [skill] first if you want [coordination benefit]"

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Shopify | Skill uses generic product references; flags that real catalog would improve campaign relevance |
| Klaviyo | Skill still produces calendar; no overlap-check with already-scheduled broadcasts |
| Keywords cache | Subject lines generated without keyword integration |
| UGC hooks cache | Copy starters generated without archetype coordination |

The skill always produces complete output — connectors enrich; they're not required.

---

## Edge cases

- **Buyer has very low budget, can't run paid ads:** filter out paid ads from the calendar. Note in the brief that organic + email + SMS only changes the campaign structure (paid amplifies; organic relies on existing audience).
- **Buyer's category doesn't fit traditional holidays:** for niche categories (B2B-leaning, hobbyist specialty), the skill biases toward brand-driven campaigns (anniversaries, collection drops, founder content) and downweights generic holiday campaigns.
- **Buyer is in regulated category (supplements, alcohol, CBD, financial):** flag platform-specific restrictions on paid ads during certain holidays (Meta has stricter alcohol restrictions during NYE; gambling restrictions vary). Note the restrictions in the campaign brief.
- **Buyer wants to skip BFCM:** rare but it happens for brands that intentionally don't discount. The skill respects it and biases toward content/brand-story-led campaigns instead.
- **Buyer wants more campaigns than the category average:** politely note that send fatigue is real — campaigns that all blend together convert worse than fewer, sharper ones. Recommend the category average.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema
- `templates/us-holidays.md` — US retail-relevant holidays with timing recommendations
- `templates/uk-eu-holidays.md` — UK/EU equivalent
- `templates/canada-au-nz-holidays.md` — Canada/AU/NZ equivalent
- `templates/campaign-playbooks.md` — campaign types (BFCM, launch, restock, flash sale, brand event)
- `templates/channel-conventions.md` — per-channel writing conventions (broadcast email, paid ads, organic social, site updates)
- `templates/send-cadence.md` — standard pre-launch / launch / mid / last-day patterns
- `templates/copy-starters.md` — archetype-driven copy starter framework
- `scripts/config_loader.py` — shared
- `scripts/keyword_cache_reader.py` — shared
- `scripts/ugc_hook_cache.py` — shared
- `scripts/holiday_dates.py` — multi-region holiday date module
- `scripts/render_calendar_xlsx.py` — calendar grid renderer
- `scripts/render_calendar_docx.py` — per-campaign briefs renderer
- `examples/q4-bfcm-calendar-example.md` — Q4 calendar with BFCM
- `examples/product-launch-calendar-example.md` — launch-focused mini-calendar
- `examples/90-day-rolling-example.md` — full 90-day rolling reference output
