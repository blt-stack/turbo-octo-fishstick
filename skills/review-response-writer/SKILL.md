---
name: review-response-writer
description: >
  Drafts public-facing replies to 1-5 star reviews across nine platforms (Shopify review apps
  including Judge.me, Loox, Yotpo, Stamped, Reviews.io, plus Amazon, Etsy, Google Business Profile,
  Trustpilot, Facebook). Three-tier framework — 1-2 star recovery with offline handoff, 3 star clarify
  with friction probe, 4-5 star amplify with referral seed. Sentiment override layer flags abusive or
  fake-competitor reviews and drafts removal-request disputes. Mines 4-5 star reviews into a
  testimonial cache and 1-2 star reviews into an objection cache for downstream skills. Single mode
  outputs .docx, bulk mode outputs .xlsx (4 sheets). Use this skill when the user mentions review
  response, reply to review, 'respond to this 1 star,' 'answer this review,' Amazon review, Etsy
  review, Google review, or 'I just got a bad review.'
---

# Review Response Writer

Drafts public-facing replies to 1★–5★ reviews across six platforms. Star-rating-aware tone (recovery / clarify / amplify). Single review or bulk mode. Mines downstream caches for the rest of the plugin.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Detect mode.** Single review (default) or bulk CSV.
3. **Ingest review(s).** Paste, CSV upload, or Shopify connector auto-fetch.
4. **Categorize each review.** Match to a star-rating tier + sentiment subtype. Flag potential fake/competitor reviews.
5. **Draft the public reply.** Apply brand voice + tier-specific reply pattern + per-platform constraints.
6. **Draft optional private follow-up.** When the public reply hands off to a private channel, draft the email/DM the buyer sends after the reviewer reaches out.
7. **Mine cross-skill caches.** Write 4-5★ quotes into testimonial cache, 1-2★ pain points into objection cache, recurring praise into keyword cache.
8. **Render output.** Single mode → `.docx`. Bulk mode → `.xlsx`.
9. **Report back.** File path, review count, tier breakdown, sentiment summary, cache write summary, suggested next step.

---

## Step 1: First-run check

Look for `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`. If missing, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

---

## Step 2: Detect mode

**Single review mode is the default.** Switch to bulk when any of these are true:

- The user attaches a CSV of reviews
- The user says "bulk," "batch," "go through all my reviews," "do my whole queue"
- The user provides 3+ reviews pasted in one message
- The user says a count: "process the next 20 reviews," "do this week's reviews"

Confirm out loud before proceeding.

---

## Step 3: Ingest reviews

Three ingestion paths:

### Path A: Buyer pastes the review (default for single mode)

Most universal. Buyer pastes the star rating, the review text, the reviewer's name, the date, and the platform. If any of those are missing, ask before drafting.

### Path B: CSV upload (default for bulk mode)

Buyer uploads a CSV exported from their review platform. Read `templates/platform-csv-shapes.md` for the column patterns each platform uses. Expected columns (case-insensitive, any subset):

- `platform`, `product_name` (or `product_id`/`product_handle`), `reviewer_name`, `reviewer_email`, `star_rating`, `review_title`, `review_body`, `received_at`, `verified_purchase` (Y/N), `order_id` (when available)

Parse, then categorize each row.

### Path C: Shopify connector auto-fetch (Judge.me / Loox / Yotpo metafields)

When Shopify is connected and the buyer's review app stores reviews in product metafields (default for Judge.me, Loox, and Yotpo's "free" tier), fetch the most recent N reviews via the metafield API. Read `templates/shopify-connector-fetch.md` for the field paths. Falls back to CSV path if the buyer is on a different review app tier or if the connector returns nothing.

---

## Step 4: Categorize the review

Three layers of categorization:

### Layer 1: Star-rating tier

| Tier | Star ratings | Reply mode | Template |
|---|---|---|---|
| Recovery | 1★, 2★ | Acknowledge failure, offer concrete fix, offline channel handoff | `templates/tier-recovery.md` |
| Clarify | 3★ | Probe for what would have made it 5★, surface the friction, light fix offer | `templates/tier-clarify.md` |
| Amplify | 4★, 5★ | Specific thanks, reinforce brand values, seed referral or repeat-purchase cue | `templates/tier-amplify.md` |

A 4★ that reads like a 3★ (lots of constructive criticism with one positive sentence) gets handled with the clarify template even though the star count is 4. Read `templates/tier-recovery.md`, `tier-clarify.md`, and `tier-amplify.md` for the patterns.

### Layer 2: Sentiment override

Read `templates/sentiment-override.md` for the framework. Four sentiment subtypes that can override the star-tier reply pattern:

- **Constructive** — Customer raises a legitimate, specific issue. (Most reviews — handle per the standard tier template.)
- **Abusive / unhinged** — All-caps tirade, personal attacks on staff, profanity. → Keep the public reply short, professional, and unprovokable. Skip apologies that don't fit the facts. Tag for founder review.
- **Fake / competitor / suspect** — Generic complaint with no specifics, reviewer history shows no purchase, oddly-timed cluster of similar reviews, language that reads like a competitor wrote it. → Draft a flag-for-removal request to the platform using `templates/dispute-drafts.md`, and only draft a placeholder public reply if removal fails.
- **Sycophantic / paid-looking** — 5★ with no substance, repetitive marketing language, suspicious reviewer history. → Draft a low-key thank-you that doesn't engage with the suspect content. Don't amplify or feature in testimonials.

The sentiment label changes what the buyer sees, not just the reply — abusive and fake reviews get the dispute draft + a "DO NOT amplify" flag on the testimonial cache write.

### Layer 3: Issue category (for recovery / clarify tiers)

What is the customer actually complaining about? Match to one of:

- Shipping (slow, lost, damaged in transit)
- Product quality (defect, doesn't match description, broke)
- Sizing / fit / spec mismatch
- Customer service experience (couldn't reach support, slow response)
- Expectation mismatch (looked different in photos, didn't perform as expected)
- Pricing / value (felt too expensive, miscounted promo)
- Other

The issue category determines specifics in the reply. A shipping complaint gets a different concrete-fix offer than a defect complaint.

---

## Step 5: Draft the public reply

Read `templates/reply-craft.md` for the universal reply structure plus per-platform constraints.

The 4-part skeleton:

1. **Open by name** — "Hi [Reviewer name]" or, on platforms where last names are exposed, just first name. Never "Dear Customer." Never "Dear Valued Customer."
2. **Reflect the specific thing** — name the issue back to them in their own words. For 4-5★, name the specific thing they praised.
3. **Resolve / amplify** — for recovery: state the concrete fix + offline channel. For clarify: probe for what would have made it 5★ + small light fix. For amplify: specific thanks + values + seed.
4. **Close in brand voice** — sign with a name (real person preferred over "the team").

Apply the brand voice from `config.brand_voice`. Apply the platform-specific constraints from `templates/platform-*.md`. Apply the tier and issue-category specifics.

### Per-platform constraints

Read the matching platform template for character limits, formatting rules, and visibility nuances:

| Platform | Template | Key constraints |
|---|---|---|
| Shopify apps (Judge.me, Loox, Yotpo, Stamped, Reviews.io) | `templates/platform-shopify-apps.md` | Most permissive; can use light markdown / line breaks; reply shows publicly under the review |
| Amazon Seller Reviews | `templates/platform-amazon.md` | Strict TOS — no contact info, no discount codes, no asking for review updates explicitly, no language that could be read as incentivization |
| Etsy | `templates/platform-etsy.md` | 500-char practical ceiling, community-style tone expected, no external links |
| Google Business Profile | `templates/platform-google.md` | Public-facing, indexed by Google search — write knowing this reply appears in search results |
| Trustpilot | `templates/platform-trustpilot.md` | High-stakes for DTC brands, replies are surfaced prominently, link to offline channel allowed |
| Facebook Page Reviews | `templates/platform-facebook.md` | Reply appears under the recommendation/review on the page; Messenger handoff common |

### Length targets

- 1-2★ recovery: 60-140 words (longer than CS reply — public proof of brand handling)
- 3★ clarify: 40-90 words
- 4-5★ amplify: 30-70 words (short, specific, warm)

### Never

- Use form-letter language ("Thank you for your review!")
- Promise things publicly that should be promised privately ("We'll refund you $X right now")
- Argue with the reviewer publicly, even when they're wrong
- Use the customer's full last name (only if the platform already exposes it)
- Sign as "Customer Service Team" — sign with a first name when at all possible
- Use the same opener twice in a single bulk batch — readers compare adjacent replies

---

## Step 6: Draft optional private follow-up

When the public reply hands the customer to a private channel ("we just emailed you," "DM us," "reply to this thread"), draft the private follow-up email/DM in `templates/private-followup.md`.

Structure:
- Subject line referencing the review
- Warmer, longer tone than the public reply
- Concrete resolution offer
- Easy next step for the customer

The private email goes in the .docx alongside the public reply. In bulk mode it gets its own column.

---

## Step 7: Mine cross-skill caches

Three caches get written from review batches:

### Testimonial cache (4-5★ amplification mining)

Read `templates/testimonial-mining.md`. From each 4-5★ review (excluding sycophantic/suspect ones), extract one to two pull-quotes that pass these filters:

- 8-30 words
- Concrete and specific (mentions a feature, outcome, or feeling — not generic praise)
- Reads aloud naturally
- Attributable (named reviewer, verified purchase preferred)

Write to `~/.the-ecommerce-seller/cache/testimonials/{product-identifier}.json` via `scripts/testimonial_cache.py`. Schema in the script docstring.

Downstream consumers: Landing Page Copywriter (testimonial sections), A+ Content Creator (social proof modules), Ad Creative Generator (testimonial-format ads).

### Objection cache (1-2★ pain point mining)

Read `templates/objection-mining.md`. From each 1-2★ review (excluding abusive/fake), extract the underlying objection — what belief or fear caused the customer to leave the rating. Examples:

- "Smaller than expected" → objection: "Sizing photos don't reflect real-life scale"
- "Took 3 weeks to arrive" → objection: "Shipping is unreliable"
- "Material felt cheap" → objection: "Doesn't match the premium price point"

Write to `~/.the-ecommerce-seller/cache/objections/{product-identifier}.json` via `scripts/objection_cache.py`. Schema in the script docstring.

Downstream consumers: Ad Creative Generator (objection-handling ads), Landing Page Copywriter (FAQ + above-the-fold reassurance), Product Description Writer (proactive spec callouts).

### Keyword cache enrichment (recurring praise phrases)

When a phrase recurs in 3+ 4-5★ reviews (e.g., "the grip is perfect," "smells exactly like the description"), promote it as a candidate keyword in the existing keywords cache at `~/.the-ecommerce-seller/cache/keywords/{product-identifier}.json`. Use `scripts/keyword_cache_enricher.py` — it loads the existing artifact (written by skill #2), appends review-mined keywords with a `source: "review-mining"` tag, and re-saves.

This is enrichment, not overwrite. Skill #2's original keywords stay intact.

---

## Step 8: Render output

### Single mode

Use `scripts/render_review_docx.py` and the `docx` skill. Structure:

```
Reply to: [Reviewer name] · [N★] · [Platform]
Posted: [date]
Product: [product name]
Tier: [Recovery / Clarify / Amplify]
Sentiment: [Constructive / Abusive / Fake / Sycophantic]

══════════════════════════════════════════════════
ORIGINAL REVIEW (for reference)
══════════════════════════════════════════════════
[Review title, if any]
[Review body]

══════════════════════════════════════════════════
DRAFTED PUBLIC REPLY
══════════════════════════════════════════════════
[Reply text, ready to copy-paste into the platform]
Character count: [N] (limit: [N])

══════════════════════════════════════════════════
DRAFTED PRIVATE FOLLOW-UP (when applicable)
══════════════════════════════════════════════════
Subject: [...]
Body: [...]

══════════════════════════════════════════════════
DISPUTE DRAFT (only for fake/competitor reviews)
══════════════════════════════════════════════════
[Removal request draft for the platform]

══════════════════════════════════════════════════
CACHE WRITES
══════════════════════════════════════════════════
- Testimonial cache: [pulled X quotes / skipped — not amplifiable]
- Objection cache: [pulled X objections / skipped — not minable]
- Keyword cache: [N candidate phrases added]
```

Save to `config.output_folder` with filename `review_reply_{reviewer-last-name}_{star}star_{date}.docx`.

### Bulk mode

Use `scripts/render_reviews_xlsx.py`. Four-sheet workbook:

**Sheet 1: Reply Queue** — one row per review with:
- Received date, Platform, Star rating, Reviewer name, Verified, Product, Tier, Sentiment, Issue category
- Original review (cell-text, wrapped)
- Drafted public reply (cell-text, wrapped) + character count
- Drafted private follow-up (cell-text, wrapped)
- Dispute draft (only populated for flagged reviews)
- Status column (Pending review / Approved / Sent / Held / Disputed — buyer fills in)

**Sheet 2: Tier & Sentiment Breakdown** — counts per tier, per platform, per sentiment, per issue category. NPS-style summary (% promoters vs detractors).

**Sheet 3: Cache Mining Summary** — list of testimonials extracted, objections extracted, keyword phrases enriched. The buyer sees exactly what flowed into the downstream skills.

**Sheet 4: Systemic Issues** — when the skill detects recurring issue categories (5+ shipping complaints in one batch, 3+ defects on one SKU), surfaces them as systemic patterns worth fixing once.

Save to `config.output_folder` with filename `review_reply_batch_{date}.xlsx`.

---

## Step 9: Report back

Tell the buyer:
1. Where the file is (`computer://` link)
2. Review count + tier breakdown (e.g., "23 reviews: 4 recovery, 5 clarify, 14 amplify")
3. Sentiment flags (e.g., "1 review flagged as likely competitor — dispute draft included")
4. Cache write summary ("8 testimonials added, 3 new objections added, 2 keyword candidates promoted")
5. Any systemic-issue flags from Sheet 4
6. One suggested next step:
   - If bulk mode: "Review the .xlsx, mark each reply's status, and post the approved ones. Sheet 3 shows what flowed into the testimonial / objection / keyword caches — the next time you run Landing Page Copywriter or Ad Creative Generator, those quotes and objections will be available."
   - If single mode: "Post the public reply, send the private follow-up if applicable, and the testimonial/objection caches are already updated."
   - If a 1★ review was abusive/fake: "Recommend filing the platform dispute first before posting any public reply — that's drafted in the .docx."

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Shopify | Skill works on CSV/paste only; flags auto-fetch from Judge.me/Loox/Yotpo metafields as upgrade |
| Trustpilot API | Skill works on CSV exports; flags direct API fetch as upgrade |
| Amazon Seller Central API | Skill works on CSV exports; flags direct API fetch as upgrade |
| Gmail | Not required; review replies aren't email-driven by default. Private follow-ups can be sent manually or via Gmail connector if available |

The skill always produces a complete reply package — connectors enrich.

---

## Edge cases

- **Review left in non-English language**: draft the reply in the same language when buyer's brand voice supports multilingual; otherwise flag for translation handoff. Don't reply in English to a Spanish reviewer if the brand voice config doesn't list Spanish.
- **Customer left two reviews on the same product**: treat the latest as the primary; reference the earlier one if context helps ("I see you returned and tried again — thank you for giving us another chance").
- **Reviewer threatens legal / regulatory action**: tag as high-risk, recommend founder review + legal review before any public reply. Don't draft anything that could be construed as admission of fault.
- **5★ review that's actually a complaint** ("Five stars only because I love the brand but the new formula is awful"): treat as clarify-tier, not amplify. The actual signal is the body, not the star count.
- **Bulk batch crosses platforms**: process each review per its platform's constraints. Don't apply Amazon's TOS rules to a Judge.me reply.
- **Reviewer is a known influencer / press / VIP**: tag in the customer context. Recommend founder reply on amplification side. The reply should still feel personal, not formal.
- **Review mentions a competitor by name** ("Way better than [Brand X]"): draft the reply without engaging with the competitor mention. Don't repeat the competitor's name in the reply.
- **Review references a CS interaction** ("Your support team was incredible"): the reply should name the team member if known. Pull from the Customer Service Reply Bot history if the email matches.
- **Pricing complaint where the buyer disagrees** ("Way too expensive for what it is"): never argue. Lead with the value framing the buyer believes in; don't litigate price publicly.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema (extended with review_response section)
- `templates/tier-recovery.md` — 1-2★ recovery reply patterns + offline handoff scripts
- `templates/tier-clarify.md` — 3★ clarification reply patterns + light-fix offers
- `templates/tier-amplify.md` — 4-5★ amplification reply patterns + referral seeds
- `templates/sentiment-override.md` — constructive vs. abusive vs. fake/competitor vs. sycophantic detection
- `templates/reply-craft.md` — universal 4-part skeleton + length targets
- `templates/private-followup.md` — private email/DM draft patterns
- `templates/dispute-drafts.md` — platform-removal request drafts per platform
- `templates/platform-shopify-apps.md` — Judge.me / Loox / Yotpo / Stamped / Reviews.io constraints
- `templates/platform-amazon.md` — Amazon Seller Reviews + TOS guardrails
- `templates/platform-etsy.md` — Etsy review reply conventions
- `templates/platform-google.md` — Google Business Profile (SEO-aware) reply patterns
- `templates/platform-trustpilot.md` — Trustpilot reply conventions
- `templates/platform-facebook.md` — Facebook Page Reviews conventions
- `templates/platform-csv-shapes.md` — Expected CSV column patterns per platform
- `templates/shopify-connector-fetch.md` — Judge.me / Loox / Yotpo metafield paths
- `templates/testimonial-mining.md` — extraction rules for 4-5★ pull-quotes
- `templates/objection-mining.md` — extraction rules for 1-2★ pain points
- `scripts/config_loader.py` — shared config loader
- `scripts/render_review_docx.py` — single-review .docx renderer
- `scripts/render_reviews_xlsx.py` — bulk .xlsx renderer with tier/sentiment breakdown + cache mining summary + systemic issues
- `scripts/testimonial_cache.py` — writer for `~/.the-ecommerce-seller/cache/testimonials/{id}.json`
- `scripts/objection_cache.py` — writer for `~/.the-ecommerce-seller/cache/objections/{id}.json`
- `scripts/keyword_cache_enricher.py` — appender for existing `~/.the-ecommerce-seller/cache/keywords/{id}.json`
- `examples/single-1star-recovery-example.md`
- `examples/single-5star-amplify-example.md`
- `examples/bulk-batch-example.md`
