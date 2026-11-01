# Per-Channel Conventions for Campaign Sends

The calendar schedules sends across four channels per campaign. Each channel has its own writing conventions, send-frequency norms, and integration with the rest of the plugin's skills.

This file covers what to write per channel. For the deeper craft (subject lines, FTC, character limits), the calendar references the relevant per-skill templates:

- **Email + SMS broadcast craft** → see skill #7's `email-craft.md` and `sms-craft.md`
- **Paid ad creative craft** → see skill #5's platform conventions + ad archetypes
- **Organic social** → covered in this file (no dedicated skill in the plugin yet)
- **Site updates** → covered in this file

---

## Channel 1: Email + SMS broadcasts (via Klaviyo)

These are one-off campaign sends, separate from the triggered flows skill #7 builds. Sent to the buyer's full subscriber list or a segment.

### Email broadcast specs

- Format: HTML email with subject line + preview text + body
- Character limits: same as skill #7 (subject 30-50 char target, preview 35-90 char)
- Send frequency: 2-4 emails per week during active campaigns is the upper bound for most lists; more causes unsubscribes
- Audience: typically "engaged subscribers" segment (opened or clicked in past 60 days) — NOT the full list. Sending to dormant subscribers hurts deliverability.

### SMS broadcast specs

- Format: 140-160 char message with shortened link
- Compliance: same TCPA rules as skill #7 (Reply STOP, brand ID in first 30, quiet hours)
- Send frequency: 1-2 SMS per campaign per audience. SMS is more intrusive than email — over-sending kills the list.
- Audience: SMS-opted-in subscribers only

### What the skill produces per email/SMS send

For each scheduled email or SMS send in the calendar, the skill produces:

- **Topic** (one paragraph: what this email is about, the angle, the offer if any)
- **Suggested subject lines** (2-3 options for A/B testing)
- **Suggested preview text** (1-2 options)
- **Suggested CTA** (button copy + destination URL)

The calendar does NOT produce full email body copy — that's where the buyer either writes it themselves or runs a complementary skill (skill #7's flow builder pattern can be adapted for broadcasts).

### Integration

The calendar feeds skill #7's broadcast functionality (when that ships as a separate flow type) and reads from skill #7's existing flow setup to avoid scheduling broadcasts that conflict with active automated flows.

---

## Channel 2: Paid Ads (Meta + TikTok)

Paid amplification of campaign messaging. Scheduled to run during the campaign window.

### Specs per platform

| Platform | Format | Spec reference |
|---|---|---|
| Meta Feed | Static image or video | skill #5's meta-ads-conventions.md |
| Meta Reels | Vertical video | same |
| Meta Stories | Vertical full-screen | same |
| TikTok In-Feed | Vertical video | skill #5's tiktok-ads-conventions.md |
| TikTok Spark | Boosted creator post | same |

### What the skill produces per paid ad send

For each scheduled paid ad in the calendar, the skill produces:

- **Campaign window** (start date, end date — typically a few days, not "always on")
- **Topic** (the campaign moment this ad supports)
- **Suggested ad hooks** (3-5 hooks across the 5 archetypes from skill #5/#6's framework)
- **Suggested visual brief** (image direction or video brief — short, not the full ad-creative output skill #5 produces)
- **Recommended budget tier** (small / medium / large relative to the buyer's existing program)

The calendar does NOT produce full ad copy (subject text, headline, description) — that's skill #5's job. The calendar tells the buyer "in this window, run this kind of ad" so they know when to invoke skill #5.

### Integration

The calendar reads from the UGC hook cache (skills #5/#6 shared) so suggested ad hooks align with the rest of the program's voice. When the buyer runs skill #5 for a specific campaign, the resulting ads have a context-aware angle already established.

### Pacing

- Don't schedule paid ads more than 1-2 days before the email campaign launches (paid spend on a campaign that hasn't started feels uncoordinated)
- Don't schedule paid ads to extend more than 2-3 days past the email campaign's end (the audience moves on; ad spend wastes)
- Always-on retargeting ads are NOT in this calendar's scope — those are program-level, not campaign-level. The calendar covers campaign-specific paid pushes.

---

## Channel 3: Organic Social (Instagram, TikTok, Facebook)

Posts on the brand's own channels (organic, not paid). Coordinated with the campaign narrative.

### Specs per platform

| Platform | Post types | Cadence during a campaign |
|---|---|---|
| Instagram Feed | Static post, carousel, Reel | 1-2 posts per campaign |
| Instagram Stories | Story sequence | Daily during campaign window |
| TikTok | Original video | 1-3 videos per campaign |
| Facebook | Static post, photo, link share | 1-2 posts per campaign |
| LinkedIn (B2B brands only) | Article or post | 1 per campaign |

### What the skill produces per organic post

For each scheduled organic post in the calendar, the skill produces:

- **Platform** (where the post goes)
- **Format** (Reel vs Story vs static)
- **Topic** (the angle)
- **Suggested caption** (2-3 options for the buyer to choose / adapt)
- **Visual brief** (what the image/video should show)
- **Suggested hashtags** (3-5 per post, platform-appropriate)

### Coordination with skills #5 and #6

The organic-post brief can reference the same creator content (skill #6) and ad hooks (skill #5) the buyer has built. Often the same UGC video that runs as a Spark Ad also gets posted organically on the brand's own account — the calendar notes when this kind of cross-pollination makes sense.

### Common pitfalls

- Over-posting during a campaign (more than 2-3 Instagram posts in a week) drives down organic reach (Instagram's algorithm penalizes high-frequency accounts)
- Posting the exact same content across all platforms — each platform's audience expects native content
- Hashtag stuffing — 5-7 hashtags is the practical max on Instagram and TikTok in 2026

---

## Channel 4: Site Updates (Homepage, Collection Pages, Popup)

The brand's own website. Update the on-site copy and visuals to align with the campaign.

### What gets updated

| Element | Frequency | Purpose |
|---|---|---|
| Homepage hero banner | Per campaign | Top-of-funnel campaign messaging |
| Sticky announcement bar | Per campaign | Constant reminder of the offer |
| Collection page hero (if campaign is collection-focused) | Per campaign | Deep-link campaign to the relevant collection |
| Site-wide popup (with offer) | Per campaign | Capture visitors who arrive via paid traffic |
| Cart-page upsell module | Optional, per campaign | Push relevant cross-sells |
| Footer banner | Optional, longer-running campaigns | Subtle reinforcement |

### What the skill produces per site-update send

For each scheduled site update in the calendar, the skill produces:

- **Element** (homepage hero, announcement bar, popup, etc.)
- **Live date** + **End date**
- **Copy options** (2-3 versions for the headline + sub + CTA button)
- **Visual brief** (what image/video should be in the hero)
- **Destination URL** (where the CTA links)

### Coordination with skill #3

When the campaign is heavy enough to warrant a dedicated landing page, the calendar flags it and recommends running skill #3 (Landing Page Copywriter) for the full landing-page brief. The calendar's site-update entry then references the landing-page URL as the destination.

### Common pitfalls

- Leaving an announcement bar live past the campaign end (kills trust — "Mother's Day sale!" still on the site in June)
- Popup over-triggering — popup that fires on every page visit annoys returning visitors
- Hero banner that doesn't match the campaign URL — confusing journey

---

## Cross-channel coordination per campaign

For each campaign, the four channels should reinforce each other in coordinated waves. Example for a 7-day product launch:

| Day | Email + SMS | Paid ads | Organic social | Site update |
|---|---|---|---|---|
| Day -3 | Pre-launch tease email | (Not yet active) | "Coming Tuesday" teaser post | Footer mention |
| Day -1 | "Tomorrow" reminder email | (Not yet active) | Day-before reminder | Pre-launch landing live |
| Day 0 (launch) | Launch email + SMS | Paid ads activate | 2 launch posts (Reels + feed) | Homepage hero + popup + announcement bar |
| Day +2 | Mid-campaign email | Paid ads continue | UGC repost from creator | Hero remains |
| Day +5 | Last-chance email + SMS | Paid ads continue | Customer-story Reel | Hero remains |
| Day +7 | Thank-you email | Paid ads end | Wrap-up post | Hero + popup come down |

Coordinated waves work better than scattered single-channel sends. The calendar's .xlsx grid view makes this visible — buyers can see at a glance whether their channels are reinforcing or fighting each other on a given day.

---

## When the buyer is multi-channel-light

Not every buyer has all four channels active. The calendar adapts:

- **No SMS opt-in collected:** SMS broadcasts dropped from calendar
- **No paid ads budget:** paid ad rows dropped; the calendar leans heavier on email + organic + site
- **No active organic social:** organic post rows dropped; calendar relies on email + paid + site
- **Headless storefront (no easy site updates):** site update rows dropped; buyer handles those manually

The skill asks during context-gathering which channels the buyer has active. The output respects that.
