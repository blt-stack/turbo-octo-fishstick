---
name: ad-creative-generator
description: >
  Writes paid-ad creative for Meta (Facebook + Instagram), TikTok, and Google Ads. Produces 5 ad
  concepts per run across 5 angle archetypes (problem-aware, social-proof, transformation,
  curiosity-gap, contrarian) in 4 creative formats (static, video wrapper, carousel, collection), with
  strict per-platform character limits enforced. Outputs a .docx brief plus per-platform .csv files
  for bulk Ads Manager upload. Use this skill when the user mentions Meta ads, Facebook ads, Instagram
  ads, TikTok ads, Google ads, 'write ad copy,' 'draft ad creative,' 'primary text,' 'headlines,' 'ad
  variants,' 'ad hooks,' 'creative brief,' 'make me ads for [product],' or 'my ads aren't converting.'
  Coordinates with the UGC Creator Brief Writer via a shared hook cache so video creator briefs and
  paid copy stay in sync.
---

# Ad Creative Generator

Writes paid-ad creative across Meta, TikTok, and Google — 5 concepts per run across 5 angle archetypes, 4 creative formats, all platform character limits enforced. Outputs both a `.docx` brief and per-platform paste-ready `.csv` files for bulk upload.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing. Check for Fal AI key.
2. **Detect platforms.** Meta, TikTok, Google — multiple allowed. Default to Meta if unspecified.
3. **Detect formats.** Static image, video wrapper, carousel, collection — multiple allowed.
4. **Gather product context.** Shopify pull, paste, URL, or photos.
5. **Read shared caches.** `ugc_hooks.json` (from skill #6 if present) and `keywords.json` (from skill #2 if relevant for Google).
6. **Generate 5 ad concepts.** One per angle archetype, each with platform-specific copy variants and format-specific image briefs.
7. **Generate static image creative.** Fal AI when key is set; Canva briefs otherwise.
8. **Render `.docx` creative brief.**
9. **Render per-platform `.csv` files** paste-ready for Ads Manager bulk upload.
10. **Write hooks back to shared cache** so skill #6 can pick them up on its next run.
11. **Report back.** File paths, platforms covered, image source, compliance check, next step.

---

## Step 1: First-run check

Look for `<plugin-root>/.config/the-ecommerce-seller.config.json`. If missing or incomplete, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

After loading config, check `config.api_keys.fal_ai`. If present, static image ads will be generated. If not, output Canva briefs and note that adding a Fal key would generate the images directly.

---

## Step 2: Detect platforms

Three supported platforms. The buyer can pick any combination:

| Platform | Trigger phrases | What changes |
|---|---|---|
| **Meta** (Facebook + Instagram) | "Meta," "Facebook ads," "Instagram ads," "FB ads," "IG ads," "Spark Ads on Meta" | Strict 125/27/27 char limits, per-placement copy variants (Feed vs Reels vs Stories) |
| **TikTok** | "TikTok Ads," "TikTok in-feed," "Spark Ads on TikTok," "top-view," "TopView" | TikTok-native length conventions, hashtag handling, Spark Ad linkage |
| **Google** | "Google Ads," "Search Ads," "Shopping Ads," "Performance Max," "PMax," "RSA," "Display ads" | Keyword-driven (pulls from skill #2's cache), structured asset groups for PMax, 15-char headlines x 30 + 90-char descriptions x 4 for RSAs |

If unclear, ask: "Which paid platforms? Meta (FB+IG), TikTok, Google, or some combination?"

Default to Meta if the user doesn't specify and the request is otherwise clear.

Read `templates/meta-ads-conventions.md`, `templates/tiktok-ads-conventions.md`, or `templates/google-ads-conventions.md` per chosen platform.

---

## Step 3: Detect formats

Four supported creative formats. Buyer can pick multiple per run:

| Format | When to use | What gets generated |
|---|---|---|
| **Static image** | Most DTC ads, lower-budget tests, evergreen creative | Image (Fal or Canva brief) + caption + headline + description |
| **Video wrapper** | When buyer has UGC footage or produced video, wrapping copy around it | Caption + headline + description + thumbnail-text overlay (no image generation — video is shot separately) |
| **Carousel** | Multi-feature showcases, before/after sequences, multi-product upsells | 2-10 cards with per-card copy + overall caption + headline |
| **Collection / Catalog** | Catalog-driven dynamic ads (Meta DPA, TikTok Collection Ads) | Wrapper copy (intro card, headline, description) — catalog images come from buyer's product feed |

If unclear, default to static image (simplest). Ask if the buyer's intent is unclear.

Read `templates/format-library.md` for per-format structural specs.

---

## Step 4: Gather product context

Same flexible input pattern as other skills:

- Shopify connector pull (preferred — captures product + photos + reviews + price)
- Amazon connector pull (where available)
- URL fetch
- Pasted product info
- Photos for vision context

For ads, the skill needs:
- Product name, category, price band
- Top 3-5 benefits in brand voice
- Target audience description (from `config.audience`)
- Key differentiators
- Existing reviews (gold for social-proof archetype copy)
- Reference photos (informs Fal image generation style)

If anything's missing, ask one round of targeted questions.

---

## Step 5: Read shared caches

The skill reads from two shared plugin caches:

### Cache A: UGC hooks cache (bidirectional with skill #6)

**Path:** `<plugin-root>/.cache/ugc_hooks/{product-identifier}.json`

Use `scripts/ugc_hook_cache.py` (load_hooks function). If skill #6 (UGC Creator Brief Writer) has written hooks for this product, capture them. These hooks were designed for in-video creator delivery — they translate naturally to ad-copy thumbnail overlays and opening caption lines. Coordinating ad-side and creator-side hooks across both skills is a real conversion win for paid+UGC campaigns.

If the cache is empty for this product, the skill generates fresh hooks. After generation, the skill writes its ad-side hooks back to the cache so skill #6 can pick them up on its next run.

### Cache B: Keywords cache (read-only, from skill #2)

**Path:** `<plugin-root>/.cache/keywords/{product-identifier}.json`

Use `scripts/keyword_cache_reader.py`. Relevant primarily for Google Ads (Search RSAs and PMax keyword themes use these directly). Meta and TikTok ads barely use keywords for targeting — but keyword weaving in copy still helps when shoppers search for the brand later.

If neither cache exists, the skill works fine — both are enrichment, not requirements.

---

## Step 6: Generate 5 ad concepts

Read `templates/ad-angle-archetypes.md` for the 5 archetype patterns. They mirror skill #6's archetypes by design (Problem-aware, Social-proof, Transformation, Curiosity-gap, Contrarian) so buyers running both skills get a unified creative-and-ads angle library.

For each archetype, generate one ad concept consisting of:

- **Hook** (5-15 words — the line that earns the click)
- **Primary text / caption** (per-platform length adjusted)
- **Headline** (per-platform length adjusted)
- **Description / link description** (per-platform length adjusted)
- **CTA button** (platform-allowed list — "Shop Now," "Learn More," "Sign Up," etc.)
- **Visual brief** (per-format — image, video, carousel)

Each archetype's tone should be distinctly different. Don't write 5 variants that are wordings of the same idea. The 5-archetype model only works when the archetypes are *meaningfully* different arguments.

Apply the buyer's brand voice from `config.brand_voice` to every concept. The brand voice is the constant; the archetype angle is the variable.

---

## Step 7: Generate static image creative (when applicable)

If "static image" is in the chosen formats:

- **If Fal AI key is set:** read `templates/fal-prompts-static.md` for ad-specific prompt patterns (different from skill #4's A+ Content prompts — ad creative needs higher contrast, less negative space). Use `scripts/fal_image_generator.py` to generate one image per archetype concept.
- **If no Fal key:** read `templates/canva-static-briefs.md`. Generate detailed Canva briefs the buyer or their designer can build.

Generated images save with names like `{product-slug}_ad-creative_{archetype}.png` to the output folder.

For video wrapper, carousel, and collection formats: no image generation — those rely on buyer-supplied video, product feed, or product photos.

---

## Step 8: Render the `.docx` creative brief

Use `scripts/render_brief_docx.py` and the `docx` skill (read its SKILL.md if not done this session). Structure:

```
[Product name] — Paid Ad Creative Brief
Generated [date] · Brand: [brand_name] · Platforms: [list] · Formats: [list]
Image source: Fal AI generated | Canva briefs
UGC hooks: coordinated with skill #6 cache | independent
Keywords: from skill #2 cache | none

══════════════════════════════════════════════════
CONCEPT 1 — [Archetype name]
══════════════════════════════════════════════════
[Image preview if generated; brief if not]
Hook: [...]
Per-platform copy:
  Meta:
    Primary text (XX/125): [...]
    Headline (XX/27): [...]
    Description (XX/27): [...]
    CTA: Shop Now
  TikTok:
    Caption (XX/100): [...]
    On-screen overlay: [...]
    CTA: Shop Now
  Google RSA:
    Headlines (each 15/30): [...]
    Descriptions (each 90/90): [...]
[Repeats for all 5 concepts]

══════════════════════════════════════════════════
COMPLIANCE CHECK
══════════════════════════════════════════════════
[Pass/fail per platform's policy categories]

══════════════════════════════════════════════════
HOW TO LAUNCH
══════════════════════════════════════════════════
Step-by-step: upload the CSVs to each Ads Manager.
```

Save to `config.output_folder` with filename `{product-slug}_ad-creative-brief_{date}.docx`.

---

## Step 9: Render per-platform `.csv` files

Use `scripts/render_ads_csv.py` to produce paste-ready CSVs for each platform's bulk-upload tool.

**Meta Ads Manager CSV** (`{product-slug}_meta-ads_{date}.csv`):
- Columns match Meta's Bulk Import template: `Ad Set Name | Ad Name | Body | Title | Link Description | Display Link | Call to Action | Creative Image File` (and a few others)
- One row per ad variant (5 concepts × number of placements covered)

**TikTok Ads Manager CSV** (`{product-slug}_tiktok-ads_{date}.csv`):
- Columns match TikTok's Bulk Upload format: `Campaign Name | Ad Group Name | Ad Name | Ad Text | CTA Button | Display Name | Video File`
- One row per ad variant

**Google Ads Editor CSV** (`{product-slug}_google-ads_{date}.csv`):
- For RSAs: `Campaign | Ad group | Headline 1-15 | Description 1-4 | Path 1 | Path 2 | Final URL`
- For PMax assets: separate sheet (or row block) per asset type (headlines, long headlines, descriptions, business name, image asset references)

Saves these as separate files alongside the `.docx` brief. Buyers paste each CSV into the corresponding Ads Manager bulk-upload screen. Saves 30-45 minutes of manual ads-manager entry per campaign.

---

## Step 10: Write hooks back to shared cache

After all 5 concepts are generated, write the ad-side hooks to the shared UGC hooks cache so skill #6 can read them on its next run.

Use `scripts/ugc_hook_cache.py` (save_hooks function). Path: `<plugin-root>/.cache/ugc_hooks/{product-identifier}.json`.

`source` (`ad-creative-generator`) and `context` (`ad_caption`) are stamped automatically, and hooks whose text is already in the cache are skipped, so re-runs don't create duplicates.

The shared file's schema (so both skills can read each other's writes):

```json
{
  "product_identifier": "river-stone-pour-over",
  "product_name": "River Stone Pour-Over",
  "last_updated": "2026-05-22T16:00:00Z",
  "hooks_by_archetype": {
    "problem_aware": [
      {"text": "...", "source": "ad-creative-generator" | "ugc-creator-brief-writer", "context": "ad_caption" | "creator_script"}
    ],
    "social_proof": [...],
    "transformation": [...],
    "curiosity_gap": [...],
    "contrarian": [...]
  }
}
```

When skill #5 reads from the cache, it prefers hooks tagged `"context": "creator_script"` for video-wrapper ads and hooks tagged `"context": "ad_caption"` (its own previous writes) for static ads.

When skill #6 reads from the cache (in a future skill #6 update), it prefers hooks tagged `"context": "creator_script"` from skill #6's own history and skips hooks tagged `"context": "ad_caption"` (those weren't written for creator delivery).

---

## Step 11: Report back

Tell the buyer:
1. Where all files are (`.docx` brief + per-platform CSVs)
2. Platforms + formats covered, concept count
3. Image source (Fal generated count vs Canva briefs)
4. Whether UGC hooks were pulled from the shared cache (coordination with skill #6)
5. One next step:
   - If buyer hasn't run skill #6 yet for this product: "Want me to write the UGC creator briefs next? Hooks will stay coordinated."
   - If buyer just generated everything: "Upload the CSVs to each Ads Manager. The first thing to A/B test is which archetype's primary text converts best."
   - If a Fal key isn't set: "Add a Fal AI key during your next config update if you want static ad images generated directly."

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Shopify | Skill falls back to URL/paste; no product feed for Collection ads (note for buyer) |
| Amazon | Skill skips Amazon-specific copy adjustments; rest of flow unchanged |
| Meta Ads connector (if exists) | Skill still generates copy; buyer manually uploads via CSV |
| Fal AI key | Static-image format outputs Canva briefs instead of generated images |
| UGC hooks cache (from skill #6) | Skill generates fresh hooks; no coordination with creator briefs |
| Keywords cache (from skill #2) | Skill doesn't weave keywords; particularly affects Google Ads quality |

The skill always works at every tier — it degrades gracefully.

---

## Edge cases

- **Regulated category** (supplements, beauty, financial, weight-loss): tighter compliance review. Meta and TikTok have category-specific policies that auto-reject ads with claims that would be fine for unregulated products. The compliance check flags these explicitly.
- **Restricted product types** (alcohol, gambling, CBD where regulated): the skill will still draft creative but flag the platform restrictions explicitly. Some categories are entirely banned on some platforms (CBD on Meta in most regions, for example).
- **Buyer wants more than 5 concepts**: politely note that 5 across 5 archetypes is the optimal test surface. Generating 10+ concepts dilutes the test signal. Offer to write a 2nd round of 5 concepts using the same archetypes but a different angle dimension (e.g., "lifestyle photo" vs "product-only photo" for the same Problem-aware archetype).
- **Buyer wants ads in a non-English language**: write the ads in the target language. Keep the .docx brief headers in English for the buyer's reference, but the actual ad copy goes in the target language. CSV output uses the target language.
- **Buyer wants one platform only**: skip the other platforms' CSVs. Don't produce empty Meta CSV if the buyer asked for TikTok only.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema
- `templates/meta-ads-conventions.md` — Meta placements, 125/27/27 limits, compliance
- `templates/tiktok-ads-conventions.md` — TikTok ad formats, hashtag handling, Spark linkage
- `templates/google-ads-conventions.md` — Search RSAs, Shopping titles, PMax asset structure
- `templates/format-library.md` — static / video wrapper / carousel / collection formats
- `templates/ad-angle-archetypes.md` — 5 archetypes tuned for ad copy (vs creator scripts)
- `templates/fal-prompts-static.md` — Fal AI prompts for static ad creative
- `templates/canva-static-briefs.md` — Canva brief structure (no-Fal-key fallback)
- `scripts/config_loader.py` — shared config loader
- `scripts/keyword_cache_reader.py` — read shared keywords cache from skill #2
- `scripts/ugc_hook_cache.py` — bidirectional reader/writer for UGC hooks cache (with skill #6)
- `scripts/fal_image_generator.py` — Fal API integration (tuned for ad creative)
- `scripts/render_brief_docx.py` — .docx creative brief renderer
- `scripts/render_ads_csv.py` — per-platform CSV renderer (Meta + TikTok + Google formats)
- `examples/meta-static-example.md` — reference Meta static ads output
- `examples/tiktok-video-wrapper-example.md` — reference TikTok video-wrapper output
- `examples/google-search-pmax-example.md` — reference Google Ads RSA + PMax output
