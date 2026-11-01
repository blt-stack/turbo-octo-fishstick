---
name: influencer-outreach-pro
description: >
  Drafts personalized cold DMs and outreach emails to creators across 6 platforms (Instagram, TikTok,
  YouTube, X/Twitter, LinkedIn, Pinterest) with 4 follower-count tiers (nano, micro, mid-tier, macro)
  and 3 payment frameworks per tier (gifted, hybrid, paid). Personalizes from buyer-pasted recent post
  context (no scraping). Tracks per-influencer relationship state (outreach history, responses,
  deliverables, payment) so follow-up messages read like continuing conversations. Includes FTC
  disclosure compliance flagging per platform. Single mode outputs .docx; bulk campaign mode outputs
  .xlsx (5 sheets). Use this skill when the user mentions influencer outreach, creator outreach,
  influencer DM, brand partnership, cold pitch, 'reach out to creators,' 'pitch [handle],' or 'send
  influencer emails.'
---

# Influencer Outreach Pro

Drafts personalized cold DMs and emails to creators across 6 platforms. 4 tiers × 3 payment frameworks. Per-influencer relationship memory. Single or bulk campaign mode.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Detect mode.** Single creator (default) or bulk campaign.
3. **Identify the creator(s).** Pull from influencer memory if known; collect handle + platform + tier + recent-post context if new.
4. **Determine tier + payment framework.** Tier from follower count; payment framework from buyer's preference + tier defaults.
5. **Extract themes from recent-post context.** Identify content style, products mentioned, current campaigns, brand alignment signals.
6. **Pick product or bundle to pitch.** From product catalog or bundle cache (skill #13).
7. **Compose the outreach.** Personalized opener + brand intro + product fit + offer + clear ask + CTA.
8. **Generate follow-up variants.** 3 follow-up messages for if no reply (different angles).
9. **Apply disclosure-compliance layer.** Flag required FTC / platform disclosures per relationship type.
10. **Update influencer memory.** Log outreach attempt, expected reply window, status.
11. **Render output.** Single → `.docx`. Bulk → `.xlsx`.
12. **Report back.** File path, creator count, expected reach if all convert, payment exposure, suggested next step.

---

## Step 1: First-run check

Look for `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`. If missing, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

---

## Step 2: Detect mode

**Single creator mode is the default.** Switch to bulk campaign when any of these are true:

- The buyer provides 2+ creator handles in one message
- The buyer says "campaign," "outreach batch," "reach out to multiple creators," "build me a list"
- The buyer uploads a CSV of creators
- The buyer says a count: "DM 20 micros for our launch"

Confirm out loud before proceeding.

---

## Step 3: Identify the creator(s)

For each creator, two paths:

### Path A: Known creator (from memory cache)

Look up `~/.the-ecommerce-seller/cache/influencers/{handle}.json` via `scripts/influencer_memory.py`. The cache holds:

- Handle, platform, follower count, tier classification
- Display name, real name if known
- Content themes, niche, audience demographics if known
- Relationship stage (new / outreached / responded / negotiating / agreed / completed / strained / blacklisted)
- All prior outreach attempts (date, type, content summary, outcome)
- Prior deliverables (posts made, links, performance metrics)
- Payment history (gifted value, cash paid, affiliate earnings)
- Notes (preferred contact channel, time zone, response time patterns)

If known, pull all of this into the new draft so it reads like a continuing relationship.

### Path B: New creator

Collect minimum: handle, platform, follower count (for tier classification), recent-post context (1-3 captions or descriptions the buyer has pasted from the creator). Optional: real name, email if found, prior brand collabs the creator has done.

Create a new influencer memory file.

---

## Step 4: Determine tier + payment framework

### Tier from follower count

Read `templates/tier-classification.md`:

| Tier | Follower range | Outreach voice | Typical conversion rate |
|---|---|---|---|
| Nano | 1K-10K | Peer-to-peer; warm + casual | 10-25% (high if relevant) |
| Micro | 10K-100K | Friendly + professional | 5-15% |
| Mid-tier | 100K-500K | Professional + business-aware | 2-8% |
| Macro | 500K+ | Formal + manager-aware | 1-3% |

### Payment framework per tier

Read `templates/payment-frameworks.md`. Three frameworks:

| Framework | Description | When to use |
|---|---|---|
| Gifted product only | Send product, no cash; creator posts at their discretion | Standard for nano + micro; sometimes mid-tier with high brand alignment |
| Hybrid (product + payment) | Product + a flat fee or per-post payment | Standard for micro + mid-tier when seeking guaranteed deliverables |
| Paid partnership | Cash fee with deliverables contract; product may or may not be included | Standard for mid-tier + macro |

Rate guidance per tier (varies by platform + niche; these are starting baselines):

```
Nano:    Gifted: $0   |   Hybrid: $25-150 + product   |   Paid: $50-200 + product
Micro:   Gifted: $0   |   Hybrid: $150-800 + product  |   Paid: $300-1500 + product
Mid:     Gifted: rare |   Hybrid: $800-3500 + product |   Paid: $1500-8000 + product
Macro:   Gifted: rare |   Hybrid: rare                |   Paid: $5000-50000+ + product (negotiated)
```

The skill recommends a framework based on tier, the brand's existing campaign budget, and the relationship stage (first contact vs. returning collaborator).

---

## Step 5: Extract themes from recent-post context

When the buyer pastes recent post context, the skill extracts:

- **Content themes** — what does the creator make content about?
- **Product mentions** — what brands / products have they featured recently?
- **Campaign signals** — are they currently running paid partnerships? (Look for #ad, #sponsored, #partner)
- **Voice signals** — formal vs. casual, irony vs. earnestness, hashtag heavy vs. minimal
- **Audience signals** — who's commenting? What language?
- **Alignment scoring** — how well does the creator's content fit the brand?

Read `templates/post-context-extraction.md` for the extraction methodology.

The extracted themes flow into the personalized opener (most critical part of cold outreach).

---

## Step 6: Pick product or bundle to pitch

Read `templates/pitch-selection.md`. Sources:

- **Single SKU pitch**: when one product is the obvious match for the creator's content
- **Bundle pitch**: when a bundle from the cache (skill #13) is a better fit (e.g., creator does morning-routine content → "The Slow Morning Bundle")
- **Multi-pitch ladder**: when the creator's audience has multiple aligned interests, present 2-3 options and let them pick

The skill checks the bundle cache for matching bundles before defaulting to single SKU. Bundle pitches often convert better because they let the creator choose the angle.

---

## Step 7: Compose the outreach

Read `templates/outreach-craft.md`. The 6-part skeleton:

1. **Personalized opener** — references something specific from their content (not "love your stuff!"; specific reference to a recent post)
2. **Brand intro** — 1-2 sentences on who the brand is, why the creator would care
3. **Product or bundle fit** — why this specific product/bundle fits their content
4. **The offer** — what's being offered (gifted product, hybrid, paid) + value
5. **The ask** — what the brand wants from the creator (post types, deliverables, timeline, exclusivity if any)
6. **Soft CTA + clear next step** — easy yes/no path

Length targets per platform:

| Platform | DM length | Email length |
|---|---|---|
| Instagram DM | 80-180 words | n/a |
| TikTok DM | 60-120 words | n/a |
| YouTube comment / DM | 80-160 words | 200-350 (email) |
| X/Twitter DM | 50-100 words | n/a |
| LinkedIn message | 120-280 words | 250-400 (email) |
| Pinterest DM | 80-150 words | n/a |
| Email (any platform) | 200-400 words | — |

---

## Step 8: Generate follow-up variants

Read `templates/follow-up-cadence.md`. When the first outreach gets no reply, the skill drafts 3 follow-up variants for different timing + tone:

1. **Soft nudge (7-10 days after first)** — light bump, no pressure, references original message
2. **Reframed offer (14-21 days)** — different angle on the same opportunity, slightly different deliverables or terms
3. **Final ask (28-35 days)** — clear "if not interested no worries, just confirming" close

The follow-up cadence varies by tier:
- Nano: tighter cadence (5 / 12 / 21 days)
- Macro: looser cadence (10 / 21 / 45 days)

---

## Step 9: Apply disclosure-compliance layer

Read `templates/disclosure-compliance.md`. The skill flags required disclosures per platform + relationship type:

- **Gifted only**: #gift or #partner on Instagram; "thanks to [brand] for sending this" on TikTok/YouTube
- **Hybrid product + payment**: #ad or #sponsored, plus platform-specific paid partnership tag
- **Paid partnership**: full #ad / #sponsored / "paid partnership with [brand]" — required everywhere
- **Affiliate**: #affiliate or "[brand] gives me a commission" required by FTC

The skill includes the required language in the outreach draft so the creator sees the disclosure expectation upfront (avoiding the "we didn't realize" excuse later).

---

## Step 10: Update influencer memory

After each outreach, the skill writes:

- Adds entry to `outreach_history` (date, type, summary, channel)
- Updates `relationship_stage` to "outreached" or "follow_up_sent_N"
- Sets `expected_response_by` based on tier defaults (3-7 days for nano, 10-21 for macro)
- Captures any new info pasted (recent post themes get logged)

When the buyer comes back with "follow up with [creator]," the skill knows when the original was sent + drafts the next variant.

---

## Step 11: Render output

### Single creator mode

Use `scripts/render_outreach_docx.py`. Structure:

```
Outreach: [Creator handle] ([Platform])
Tier: [Nano/Micro/Mid/Macro] (Followers: [N])
Payment framework: [Gifted / Hybrid / Paid]
Generated: [date]

══════════════════════════════════════════════════
CREATOR CONTEXT
══════════════════════════════════════════════════
Handle: [@handle]
Platform: [Instagram / TikTok / etc.]
Follower count: [N]
Niche: [extracted from posts]
Recent themes: [extracted from posts]
Prior relationship: [from memory cache, if any]

══════════════════════════════════════════════════
PITCH RECOMMENDATION
══════════════════════════════════════════════════
Product/Bundle: [SKU or bundle name]
Why this fits: [reasoning from post context]
Payment framework: [recommended]
Rate guidance: $[range]
Expected reach: [N impressions estimate]

══════════════════════════════════════════════════
INITIAL OUTREACH (paste-ready for [DM channel])
══════════════════════════════════════════════════
[Word count: N / target: N-N]

[Full outreach message text]

══════════════════════════════════════════════════
FOLLOW-UP VARIANTS (use if no reply)
══════════════════════════════════════════════════
Follow-up A — Soft nudge (send 7-10 days after initial)
[message]

Follow-up B — Reframed offer (send 14-21 days after initial)
[message]

Follow-up C — Final ask (send 28-35 days after initial)
[message]

══════════════════════════════════════════════════
SUGGESTED DELIVERABLES STRUCTURE
══════════════════════════════════════════════════
[Number of posts, post types, usage rights, timing window]

══════════════════════════════════════════════════
DISCLOSURE REQUIREMENTS
══════════════════════════════════════════════════
[Per FTC + platform requirements for this relationship type]

══════════════════════════════════════════════════
NEXT STEPS
══════════════════════════════════════════════════
[Send via X channel; expected reply window N days; follow-up reminder for date Y]
```

Save as `outreach_{handle}_{platform}_{date}.docx`.

### Bulk campaign mode

Use `scripts/render_campaign_xlsx.py`. Five-sheet workbook:

**Sheet 1: Outreach Queue** — one row per creator:
- Handle, platform, tier, follower count
- Niche, recent themes (extracted)
- Pitch product/bundle, payment framework, rate offered
- Initial outreach draft (full text, cell-wrapped)
- Subject line (if email channel)
- Status (Drafted / Sent / Responded / Negotiating / Agreed / Declined / Posted — buyer fills in)
- Expected reply by date

**Sheet 2: Campaign Summary** — counts per tier, per platform, total budget exposure, projected reach, response rate (auto-calculates as buyer fills in status)

**Sheet 3: Disclosure Compliance** — per creator: required disclosure language, where the creator must include it, brand monitoring approach

**Sheet 4: Follow-up Calendar** — chronological, when each creator's next follow-up is due (based on no-reply window per tier)

**Sheet 5: Influencer Memory Updates** — what got written to the cache per creator

Save as `influencer_campaign_{campaign-name}_{date}.xlsx`.

---

## Step 12: Report back

Tell the buyer:
1. File path (`computer://` link)
2. Creator count + tier breakdown
3. Total budget exposure if all convert
4. Projected reach across creators (if data available)
5. Expected response rate range based on tiers
6. Memory cache write summary
7. Suggested next step:
   - "Send the outreach via [channel]; check Sheet 4 for follow-up timing reminders"
   - "Bulk-send messages over 2-3 days, not all at once (platform spam filters)"
   - "Update Status column as conversations progress — re-run skill to draft follow-ups for any 'no_reply' creators"

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Brand voice config | Skill outputs generic-brand-voice outreach; flags |
| Bundle cache (skill #13) | Skill pitches single SKUs only; flags as upgrade |
| Testimonial cache (skill #10) | Social-proof paragraph falls back to features-only |
| Platform direct send | Skill outputs paste-ready text; buyer manually pastes into platform DM |

The skill always produces outreach — connectors enrich.

---

## Edge cases

- **Creator already in cache with prior decline**: skill flags and recommends not re-outreaching for 6+ months (or skipping entirely if the decline was hostile)
- **Creator's recent content shows brand misalignment**: skill flags the mismatch in the audit and recommends finding a better-fit creator instead of forcing a pitch
- **Creator currently running competitor partnership**: skill detects competitor mentions in pasted post context and recommends waiting 30-60 days
- **Cold outreach to a creator with public manager email**: skill recommends emailing the manager rather than DM'ing the creator directly; provides a manager-pitch template
- **Multilingual creator (content in non-English language)**: skill flags and asks if the buyer wants outreach in the creator's language (requires buyer to confirm language fit)
- **Creator's audience demographic doesn't match brand audience**: skill flags and reasks before drafting
- **Bulk campaign exceeds buyer's stated budget**: skill flags the total exposure if all convert and asks buyer to confirm or trim list
- **Creator with very recent viral moment**: skill recommends adjusting framing — they may be overwhelmed with brand outreach; lead with non-pitch warmth
- **Creator request rate vs. budget mismatch**: when rates the skill suggests don't fit buyer's budget, the skill recommends going to a smaller tier rather than lowballing

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config (extended with influencer_outreach section)
- `templates/platform-instagram.md` — IG DM conventions + paid partnership tags
- `templates/platform-tiktok.md` — TikTok DM conventions + creator marketplace basics
- `templates/platform-youtube.md` — YouTube comment/DM vs. email; long-form considerations
- `templates/platform-x-twitter.md` — X/Twitter DM conventions
- `templates/platform-linkedin.md` — LinkedIn message conventions (B2B-adjacent creators)
- `templates/platform-pinterest.md` — Pinterest message conventions
- `templates/tier-classification.md` — follower-count tiers + voice register per tier
- `templates/payment-frameworks.md` — gifted / hybrid / paid frameworks + rate guidance
- `templates/post-context-extraction.md` — methodology for extracting themes from pasted post context
- `templates/pitch-selection.md` — single SKU vs. bundle pitch decision tree
- `templates/outreach-craft.md` — 6-part outreach skeleton + length targets
- `templates/follow-up-cadence.md` — 3-variant follow-up framework + tier-based timing
- `templates/disclosure-compliance.md` — FTC + platform disclosure requirements per relationship type
- `templates/influencer-memory.md` — schema for `~/.the-ecommerce-seller/cache/influencers/{handle}.json`
- `templates/deliverables-structure.md` — common deliverables packages + usage rights
- `scripts/config_loader.py` — shared config loader
- `scripts/influencer_memory.py` — per-influencer relationship cache writer/reader
- `scripts/render_outreach_docx.py` — single-creator .docx renderer
- `scripts/render_campaign_xlsx.py` — bulk campaign .xlsx renderer (5 sheets)
- `examples/single-nano-ig-outreach-example.md`
- `examples/single-macro-youtube-outreach-example.md`
- `examples/bulk-campaign-example.md`
