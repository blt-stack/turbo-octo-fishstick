---
name: listing-seo-optimizer
description: >
  Audits and optimizes e-commerce product listings for organic search across six platforms — Shopify,
  Amazon, Etsy, eBay, Walmart, and TikTok Shop. Three-source keyword research combining LLM inference,
  Amazon autocomplete scraping, and Google Suggest. Deterministic scoring rubric covers keyword
  coverage, title strength, bullet quality, backend fields, and completeness. Outputs a .docx audit
  report for single listings or .xlsx bulk audit workbook for multi-listing scans. Writes a shared
  keywords.json cache that downstream skills (PDP writer, ad copy, A+ Content) read. Use this skill
  when the user mentions listing SEO, keyword research, Amazon SEO, Etsy SEO, Shopify SEO, listing
  audit, 'audit my listing,' 'fix my product page,' 'find me keywords,' 'my listing isn't ranking,' or
  'rewrite my title and bullets.'
---

# Listing SEO Optimizer

Scores existing listings, researches keywords, and rewrites listing fields for organic search ranking across six platforms. Also feeds keyword data into the Product Description Writer for chained workflows.

## How this skill works at a glance

1. **First-run check.** Load the buyer's shared plugin config; trigger onboarding if missing.
2. **Detect mode.** Single product (default) or bulk (CSV upload / Shopify collection).
3. **Gather listing input.** Shopify pull, URL fetch, paste, or photo — same flexible input pattern as the Product Description Writer.
4. **Research keywords.** Combine LLM inference from product info with live scraping of Amazon autocomplete (via Claude in Chrome) and Google suggest (free endpoint). Cluster and rank.
5. **Score the existing listing.** Apply the audit rubric across keyword coverage, title strength, bullet quality, backend terms, and completeness. Per-platform.
6. **Rewrite listing fields.** Produce optimized title, bullets, description, backend search terms, meta tags, URL handle, alt text, attributes — per platform the buyer sells on.
7. **Render output.** Single mode → polished `.docx` per product. Bulk → `.xlsx` workbook with audit scores and rewrites per row.
8. **Write keyword artifact.** Save `keywords.json` to `~/.the-ecommerce-seller/cache/keywords/{product-id}.json` so the Product Description Writer picks it up automatically.
9. **Report back.** File paths, top-line score, and a one-line next-step suggestion.

---

## Step 1: First-run check

Look for the shared plugin config at `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`. This folder sits outside the plugin so setup and saved data survive plugin updates. If the buyer set `THE_ECOMMERCE_SELLER_DATA`, the scripts use that folder instead — run `python scripts/config_loader.py` (or call `config_path()`) to see the exact path rather than guessing.

If the config exists and is complete, load it. If missing or incomplete, run the onboarding flow defined in `../product-description-writer/templates/onboarding.md`. The config is shared across all skills in this plugin — same brand voice, same platforms, same audience. The buyer onboards once.

Use the same `scripts/config_loader.py` logic shipped with this skill (the version in this skill is identical to the one in the Product Description Writer skill; they read and write the same file).

---

## Step 2: Detect mode

Single product mode is the default. Switch to bulk when:

- The user attaches a CSV/.xlsx of listings to audit
- The user says "audit all my listings," "score everything in [collection]," "my whole catalog," "all [X] products," or similar
- The user references a Shopify collection by name
- The user provides 5+ listing URLs or handles in one message

Confirm the mode out loud, and for bulk mode confirm the source (which CSV, which collection).

---

## Step 3: Gather listing input

Same four input sources as the Product Description Writer. The buyer can mix and match.

### Source A: Shopify connector pull

If Shopify is connected, pull the product by handle or ID. Capture: title, current description, product type, vendor, tags, variants, price, images (with current alt text), URL handle, meta title, meta description, and any SEO-related metafields if accessible.

### Source B: Paste existing listing

The buyer pastes whatever they have — could be a full Amazon listing copy-pasted from Seller Central, an Etsy listing, a Shopify export, or just title + bullets.

### Source C: Listing URL

The buyer drops a URL (their own listing on any platform, or a competitor's). Use `mcp__workspace__web_fetch` first. If the page is client-rendered and returns a shell, escalate to `mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text` (load via ToolSearch first).

Note: when auditing the buyer's own listings, ranking is what matters. When analyzing a competitor URL, extract keywords and structural choices to inform the buyer's rewrite — never copy phrasing.

### Source D: Greenfield (no existing listing)

If the buyer is preparing to write a new listing and there's nothing to audit yet, skip the audit step and proceed directly to keyword research + draft rewrites. Note this clearly in the output.

---

## Step 4: Research keywords

Read `templates/keyword-research.md` for the full workflow. The short version:

### 4A — LLM inference (always run)

Generate 30-50 candidate keywords from product info, category knowledge, and the buyer's brand context. Cover:
- Head terms (broad, high-volume): `coffee dripper`, `pour over`
- Long-tail (3-5 words, lower volume, higher intent): `single cup ceramic pour over`, `handmade reusable filter pour over`
- Audience/occasion modifiers: `coffee gift for him`, `slow morning ritual`
- Use-case framings: `paperless coffee brewing`, `dishwasher safe pour over`

### 4B — Amazon autocomplete scrape (when Chrome available)

Use Claude in Chrome to:
1. Navigate to amazon.com
2. Click into the search box
3. Type the head term — capture the autocomplete suggestions (these are real searches Amazon users make)
4. Repeat for 3-5 head terms
5. Extract suggestions as a deduplicated list

If Claude in Chrome isn't available, skip this step and lean on LLM inference + Google suggest. Tell the buyer once that Chrome would improve the keyword quality.

### 4C — Google suggest (always run)

Use `scripts/google_suggest_scraper.py` to hit Google's free autocomplete endpoint (`https://suggestqueries.google.com/complete/search`). No API key needed. Returns 8-10 suggestions per seed query. Fast and reliable.

### 4D — Cluster and rank

Combine all sources. Cluster by intent (informational, transactional, comparison) and rank by:
- Relevance to the product (LLM judgment)
- Match-type intent (long-tail/buying intent wins over broad/informational)
- Repetition across sources (a keyword that appears in both Amazon autocomplete and Google suggest is a strong signal)

Produce a final ranked list of 15-25 keywords with notes on where to use each one (title, bullets, backend, meta description, alt text).

---

## Step 5: Score the existing listing

Read `templates/audit-rubric.md` for the full scoring system. Quick summary:

A listing gets a total score 0-100 (per platform), made of five weighted sub-scores:

- **Keyword coverage** (30 pts) — Does the title and body contain the high-priority keywords from the research step?
- **Title strength** (20 pts) — Length, front-loading, platform-specific best practices
- **Bullet quality** (20 pts) — Number of bullets used, benefit-led structure, character utilization
- **Backend / structured fields** (15 pts) — Backend search terms, attributes, tags filled and unique
- **Completeness** (15 pts) — Meta description present, alt text on images, URL handle clean, schema fields populated where applicable

Each sub-score has objective checks (e.g., "title uses 87% of available characters" → 17/20) and notes explaining what was lost. Use `scripts/score_listing.py` to apply the rubric programmatically — it's faster and more consistent than eyeballing.

The audit section of the output lists the score, the sub-scores, the specific issues found, and the suggested fixes. Treat it as actionable — every issue gets a fix recommendation.

---

## Step 6: Rewrite listing fields

For each platform the buyer sells on (from `config.platforms_enabled`), generate optimized rewrites. Read the platform-specific guide before writing:

- `templates/shopify-seo.md` — meta tags, URL handle, alt text, schema, internal linking
- `templates/amazon-seo.md` — A9 indexing, title structure, bullet best practice, backend search terms (byte-counted)
- `templates/etsy-seo.md` — title front-loading, 13 multi-word tags, attribute completion
- `templates/ebay-seo.md` — title (80 char), item specifics weighting
- `templates/walmart-seo.md` — listing quality score, attribute completion
- `templates/tiktok-shop-seo.md` — hashtag selection, attribute matching

Each rewrite must:
1. Integrate the top keywords naturally (never stuff)
2. Respect platform character limits (see character limit reference in each platform guide)
3. Preserve the buyer's brand voice (loaded from `config.brand_voice`)
4. Improve on the score the existing listing got

When a platform's rewrite is unchanged from the existing version, say so — sometimes the existing listing is already good and the win is in another field.

---

## Step 7: Render output

### Single mode

Use the `docx` skill (read its SKILL.md first if you haven't this session) and `scripts/render_audit_docx.py` for layout. Document structure:

```
[Product name] — SEO Audit & Optimization
Generated [date] · Brand: [brand_name] · Source: [Shopify | URL | pasted | greenfield]

══════════════════════════════════════════════════
AUDIT SUMMARY
══════════════════════════════════════════════════
Total score (per platform):
  Shopify: 72/100
  Amazon:  61/100
  Etsy:    —  (not enabled)

Strongest dimensions: title strength, bullet quality
Weakest dimensions:   keyword coverage, backend terms

══════════════════════════════════════════════════
KEYWORD RESEARCH
══════════════════════════════════════════════════
Top 20 keywords with source, intent, and recommended placement.

══════════════════════════════════════════════════
SHOPIFY — Audit + Rewrites
══════════════════════════════════════════════════
Sub-score breakdown.
Specific issues found.
Optimized title, meta title, meta description, URL handle.
Recommended alt text per image (if images available).
Schema field recommendations.

══════════════════════════════════════════════════
AMAZON — Audit + Rewrites
══════════════════════════════════════════════════
[same shape]

[...repeat per enabled platform...]

══════════════════════════════════════════════════
ACTION CHECKLIST
══════════════════════════════════════════════════
Ordered list of what to change, in order of impact. Checkboxes.
```

Save to the buyer's `output_folder` from config.

### Bulk mode

Use the `xlsx` skill and `scripts/render_bulk_audit_xlsx.py`. Three-sheet workbook:

- **Sheet 1: Scores** — one row per product, columns for total score + sub-scores per platform. Conditional formatting (red < 60, yellow 60-79, green ≥ 80) for at-a-glance triage.
- **Sheet 2: Rewrites** — one row per product, columns for optimized title/bullets/description/backend per enabled platform.
- **Sheet 3: Action Items** — one row per (product × issue), so the buyer can sort and tackle highest-impact issues first.

Bulk runs should batch products (default 10 per batch) using `scripts/bulk_processor.py` patterns from the Product Description Writer skill.

---

## Step 8: Write the keyword artifact

After every successful run, write a `keywords.json` to the shared cache:

**Path:** `~/.the-ecommerce-seller/cache/keywords/{product-identifier}.json`

Where `{product-identifier}` is, in priority order:
1. The Shopify product handle (preferred — stable and human-readable)
2. The Amazon ASIN
3. A slugified version of the product name (fallback)

Use `scripts/keyword_artifact_writer.py` to handle the write. The artifact schema:

```json
{
  "product_identifier": "river-stone-pour-over",
  "product_name": "River Stone Pour-Over",
  "generated_at": "2026-05-21T14:32:00Z",
  "voice_profile_version": "v2026-05-21",
  "keywords_ranked": [
    {"keyword": "ceramic pour over", "intent": "transactional", "sources": ["amazon_autocomplete", "google_suggest"], "recommended_placement": ["amazon_title", "shopify_title", "etsy_title"], "rank": 1},
    {"keyword": "handmade coffee dripper", "intent": "transactional", "sources": ["llm", "google_suggest"], "recommended_placement": ["amazon_bullet_1", "etsy_tag", "shopify_meta_title"], "rank": 2}
  ],
  "platforms_optimized": ["shopify", "amazon", "etsy"]
}
```

The Product Description Writer's SKILL.md already checks this location on every run — when fresh keywords are present, it weaves them in automatically.

---

## Step 9: Report back

Tell the buyer:
1. Where the audit file is (`computer://` link)
2. Top-line score per platform
3. One sentence on the biggest win available (e.g., "Biggest lift: backend search terms are empty — adding the top 5 keywords lifts your Amazon score from 61 to ~78.")
4. One sentence on next steps (e.g., "Keywords saved to the plugin cache — next time you run the Product Description Writer on this product, it'll use them automatically.")

Keep it short. The buyer wants the audit and the action items, not a lecture.

---

## Connector availability and graceful degradation

The skill works at every connector tier:

- **Both Shopify and Claude in Chrome available**: full pipeline (Shopify pull + Amazon autocomplete + Google suggest + LLM inference)
- **Only Shopify**: skip Amazon autocomplete; lean on Google suggest + LLM
- **Only Claude in Chrome (no Shopify)**: buyer pastes listing or provides URL; full keyword research still works
- **Neither connector**: buyer pastes listing; keyword research uses Google suggest (still no API key needed) + LLM inference

Tell the buyer once when a connector is missing, with installation guidance. Don't nag on subsequent runs.

---

## Edge cases

- **Listing is already excellent**: scores 90+ on all enabled platforms. Still produce the audit but say so plainly. Don't fabricate issues to justify the run. Suggest the buyer focus effort elsewhere.
- **Keywords contradict brand voice**: if scraped keywords skew salesy/spammy and the brand voice is calm/lifestyle, prefer voice over volume. Note the tension in the audit.
- **Greenfield product (no listing yet)**: skip Step 5 (scoring), do Steps 3-4 and 6-9. Output flags this clearly.
- **Restricted or gated categories on Amazon**: backend search terms work differently. Note the constraint and limit recommendations to compliant ones.
- **Adult / regulated products**: refuse for prohibited categories. For age-restricted-but-legal categories, write recommendations that comply with each platform's content policy.
- **Bulk run with hundreds of products**: warn about expected runtime. Offer to score (cheap) all of them first, then rewrite (expensive) only the bottom quartile.

---

## Files in this skill

- `SKILL.md` — this file
- `templates/audit-rubric.md` — 0-100 scoring system with weights and per-sub-score checks
- `templates/keyword-research.md` — full keyword research workflow (LLM + autocomplete scraping + clustering)
- `templates/shopify-seo.md` — Shopify-specific ranking factors and rewrite guidance
- `templates/amazon-seo.md` — Amazon A9 ranking factors and rewrite guidance
- `templates/etsy-seo.md` — Etsy ranking factors and rewrite guidance
- `templates/ebay-seo.md` — eBay ranking factors and rewrite guidance
- `templates/walmart-seo.md` — Walmart Listing Quality Score and rewrite guidance
- `templates/tiktok-shop-seo.md` — TikTok Shop ranking factors and rewrite guidance
- `scripts/config_loader.py` — shared config loader (same as Product Description Writer)
- `scripts/google_suggest_scraper.py` — free Google autocomplete endpoint scraper
- `scripts/score_listing.py` — applies the audit rubric to listing fields
- `scripts/keyword_artifact_writer.py` — writes the shared `keywords.json` cache file
- `scripts/render_audit_docx.py` — renders single-mode audit .docx
- `scripts/render_bulk_audit_xlsx.py` — renders bulk-mode audit .xlsx
- `examples/single-audit-example.md` — reference output for single mode
- `examples/bulk-audit-example.md` — reference output structure for bulk mode
