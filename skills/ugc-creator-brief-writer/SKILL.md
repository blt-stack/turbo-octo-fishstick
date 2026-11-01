---
name: ugc-creator-brief-writer
description: >
  Writes briefs for UGC creators across TikTok, Reels, Stories, and YouTube Shorts. Three brief types
  — organic (no payment), paid partnership, and affiliate. Each brief includes 10 hook options across
  5 archetypes (problem-aware, social-proof, transformation, curiosity-gap, contrarian), b-roll shot
  patterns, FTC and usage-rights language, and platform-specific conventions. Single mode (one
  creator) outputs .docx; campaign mode (multi-creator) outputs .docx briefs plus an .xlsx assignment
  workbook. Use this skill when the user mentions UGC, creator brief, TikTok brief, Reels brief,
  'brief for my creator,' 'script for my UGC creator,' 'hooks for [product],' or 'I need a UGC plan.'
---

# UGC Creator Brief Writer

Writes briefs that go to UGC creators before they shoot — covering organic, paid, and affiliate types across TikTok, Reels, Stories, and YouTube Shorts. Supports single-creator and multi-creator campaign modes.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Detect mode.** Single brief (default) or campaign (multi-creator).
3. **Detect brief type.** Organic, paid, or affiliate — based on user language.
4. **Detect platforms.** Pick from TikTok, Reels, Stories, Shorts. Multiple OK.
5. **Gather product context.** Shopify pull, paste, URL, or photos.
6. **Generate hooks.** Read the shared hooks cache first, then write 10 hooks across 5 angle archetypes, weighted to the product and brand voice. Save them back to the cache.
7. **Build the brief.** Product context, hooks, b-roll shot list, talking points, do's-and-don'ts, FTC + rights language (when paid), deliverables.
8. **Render output.** Single mode → `.docx` brief. Campaign mode → master `.docx` + per-creator `.docx` files + `.xlsx` hook-assignment workbook.
9. **Report back.** File paths, brief type detected, hook archetypes used, next step.

---

## Step 1: First-run check

Look for `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`. If missing or incomplete, run the onboarding flow from `../product-description-writer/templates/onboarding.md`. The config is shared across all skills in this plugin — same brand voice, same audience, same output folder. Use `scripts/config_loader.py`.

---

## Step 2: Detect mode

**Single mode is the default.** Switch to campaign mode when any of these are true:

- The user mentions multiple creators by name (e.g., "I'm working with @amyhouse, @lifestylebymeg, and @threecutekids")
- The user says "campaign," "creator roster," "wave," "multi-creator," "batch," or similar
- The user provides a list of 3+ creator handles or names
- The user references a creator platform's matched list (Whalar, Aspire, LTK, Insense, Cartwheel)

Confirm the mode out loud. For campaign mode, also ask:
- How many creators? (used to size the .xlsx)
- Are the creators all on the same platform, or a mix?

---

## Step 3: Detect brief type

Three brief types are supported:

| Type | Trigger phrases | What changes in the brief |
|---|---|---|
| **Organic** | "for my own social," "I want to repost it," "organic content," no mention of ads or affiliate | No FTC #ad required, no usage-rights paragraph, lighter compliance section |
| **Paid (Spark / Whitelisted)** | "Spark Ads," "whitelisted ads," "I'll run it as an ad," "boost the post," "ads through their handle" | Required FTC disclosure language, usage-rights paragraph, brand-safety guardrails, allowlisting handshake (when whitelisted) |
| **Affiliate / commission** | "affiliate," "commission," "tracked link," "discount code," "earn % of sales" | Tracked link visibility requirements, on-screen code display rules, deliverable for "show the code/link on screen" |

If unclear, ask one focused clarifying question: "Is this for organic content (you'll repost), paid ads (you'll boost or run as Spark Ads), or affiliate (creator earns commission)?"

The brief type drives which sections appear in the brief and what compliance language gets included. Read `templates/brief-types-library.md` for the per-type structural differences.

---

## Step 4: Detect platforms

Up to 4 platforms supported per brief:
- **TikTok** — most common UGC ask. Vertical 9:16, 15-60s sweet spot, audio-on.
- **Instagram Reels** — same 9:16, 15-90s, often cross-posted from TikTok with adjustments.
- **Instagram Stories** — 9:16, 15s clips, more casual/raw.
- **YouTube Shorts** — 9:16, up to 60s, SEO-aware (Shorts titles affect discoverability).

If the user says "TikTok and Reels," brief covers both with platform-specific notes per section. If they say "give me everything," brief covers all 4. If they don't specify, ask once — different platforms have different hook timing and caption conventions.

Read `templates/platform-conventions.md` for the per-platform specs.

---

## Step 5: Gather product context

Same flexible input pattern as the other skills in this plugin:

- **Shopify connector pull** — captures product info, photos, reviews, price, variants
- **URL fetch** — buyer drops a Shopify or marketplace URL
- **Paste** — buyer writes a quick spec block
- **Photos** — buyer attaches product images (vision used to infer materials, context)

For a UGC brief, the skill needs:
- Product name + category
- Top 3-5 benefits (in brand voice)
- Target audience description (from `config.audience`)
- Visual context — what does the product look like, how is it used
- Brand voice (from `config.brand_voice` — informs creator tone direction)
- Existing reviews if available — gold for sourcing real customer language for hooks and talking points
- Any specific differentiators the brand wants creators to emphasize

If anything's missing, ask one round of targeted questions before drafting.

---

## Step 6: Generate hooks

### 6a. Read the shared hooks cache

Before writing anything, check whether the Ad Creative Generator (or an earlier run of this skill) already saved hooks for this product.

**Path:** `~/.the-ecommerce-seller/cache/ugc_hooks/{product-identifier}.json`

Use `scripts/ugc_hook_cache.py`: call `find_hooks_for_product(shopify_handle=..., amazon_asin=..., product_name=...)` with whatever identifiers you have. The product identifier is the Shopify handle when there is one, else the Amazon ASIN, else the slugified product name — use the same identifier when saving in 6c.

If hooks exist:
- **`creator_script` hooks** (from earlier UGC briefs) — reuse the strongest ones when the buyer is running a follow-up wave, so the campaign stays consistent, but don't repeat a hook a creator has already shot.
- **`ad_caption` hooks** (from the Ad Creative Generator) — these are written for ad captions and thumbnails. Use them as raw material: keep the angle, rewrite each as a spoken line a creator would actually say on camera, and keep it under 8 words for TikTok/Reels. When a paid campaign runs both ads and creator videos, matching the ad hook and the video hook for the same archetype improves message consistency.

Tell the buyer in one line what you found (e.g., "Found 5 ad hooks from your last Ad Creative Generator run — I adapted 3 of them for creators"). If the cache is empty, write fresh hooks — the cache is enrichment, not a requirement.

### 6b. Write the hooks

10 hooks across 5 angle archetypes (2 per archetype). Read `templates/hook-archetypes.md` for full archetype definitions and examples.

The 5 archetypes:

- **Problem-aware** — names a pain the audience already feels
- **Social-proof** — references how many other people / what credentials are behind it
- **Transformation** — paints the after-state
- **Curiosity gap** — sets up a question or unexpected setup that requires the rest of the video to resolve
- **Contrarian** — challenges a common belief in the category

Hooks should be:
- Short enough to land in the first 1-2 seconds of the video (under 8 words for TikTok/Reels, slightly longer ok for YouTube Shorts)
- Specific to the product (no generic templates)
- Voice-aligned with the brand (loaded from `config.brand_voice`)
- Format-appropriate per platform (TikTok hook style ≠ YouTube Shorts hook style)

In campaign mode, the 10 hooks get assigned across creators (via the .xlsx workbook) so no two creators are shooting the same hook.

### 6c. Save the hooks back to the cache

Once the buyer is happy with the hooks, save all 10 so the Ad Creative Generator can reuse the creator-side lines in its video-wrapper ad copy:

```python
from ugc_hook_cache import save_hooks
save_hooks(product_identifier, product_name, {
    "problem_aware": [{"text": "...", "platform": "tiktok"}, ...],
    "social_proof": [...],
    "transformation": [...],
    "curiosity_gap": [...],
    "contrarian": [...],
})
```

`source` (`ugc-creator-brief-writer`) and `context` (`creator_script`) are filled in automatically, hooks already in the cache are skipped, and existing ad-side hooks are kept.

---

## Step 7: Build the brief

Read the brief-type structure from `templates/brief-types-library.md` and assemble:

**Universal sections (in every brief regardless of type):**
- Product context (brand voice version of what the product is)
- The ask (1-2 sentences: what the buyer wants from this content)
- Audience (who the creator should imagine they're talking to)
- 10 hooks across 5 archetypes
- B-roll shot list (5-10 specific shots — read `templates/bsroll-shotlist-patterns.md`)
- Talking points (3-5 things to mention organically, framed as soft suggestions)
- Tone-of-voice direction (creator-facing — what register, what to avoid)
- Do's and don'ts (5-7 each, brand-safety focused)
- Deliverables (number of videos, formats, durations, aspect ratio per platform)
- Timeline (shooting deadline, delivery deadline)
- How to deliver (Dropbox link, Frame.io, WeTransfer, etc.)

**Type-specific sections:**

For **paid UGC** briefs, add:
- FTC disclosure language (exact wording — read `templates/ftc-and-rights.md`)
- Usage rights paragraph (what the buyer is licensed to do with the footage, and for how long)
- Brand-safety guardrails (things never to say or imply that could trigger ad rejection)
- Whitelisting handshake instructions (when applicable — what permissions the creator needs to enable)

For **affiliate** briefs, add:
- Tracked link / discount code instructions
- On-screen display requirements (where + when to show the link or code)
- Disclosure language (FTC + platform-specific affiliate disclosure)
- Commission structure summary (no need to negotiate — just confirm)

**Optional sections (include when relevant):**
- Reference videos (links to creators / videos that capture the desired vibe)
- Music guidance (trending sounds vs licensed audio, what to avoid)
- Examples of what NOT to do (anti-references)

The brief should feel like a smart marketer wrote it for a creator they respect — not a corporate document. Read `templates/brief-types-library.md` for tone notes per type.

---

## Step 8: Render output

### Single mode

Produce a polished `.docx` brief using the `docx` skill (read its SKILL.md if not done this session) and `scripts/render_brief_docx.py`. Filename: `{product-slug}_ugc_brief_{platform}_{date}.docx`.

Save to `config.output_folder`.

### Campaign mode

Produce three deliverables:

1. **Master brief** (`.docx`) — the full canonical brief with all 10 hooks. Used by the buyer for reference and as the starting point.
2. **Per-creator briefs** (`.docx` each) — one per creator, lightly personalized. Same product context, same do's-and-don'ts, but each creator gets their assigned 2-3 hooks (not all 10), their assigned angle archetype focus, and a personalized "your role in this campaign" intro.
3. **Hook assignment .xlsx** — workbook with one row per creator showing: handle, assigned hooks, assigned angle archetype, platform, delivery deadline, payment terms, status column.

Read `templates/campaign-mode.md` for the hook-distribution logic. The goal is to assign hooks so the campaign produces 3-5 distinctly different videos rather than 5 near-identical ones.

Use `scripts/render_campaign_xlsx.py` for the workbook.

---

## Step 9: Report back

Tell the buyer:
1. Where the file(s) are (`computer://` links)
2. Brief type detected and platforms covered
3. Hook archetypes used + assignment summary (in campaign mode)
4. One suggested next step (e.g., "Run the Influencer Outreach Pro skill next to draft the DM that gets these creators to say yes," or "Run the Ad Creative Generator next — it will pick up these hooks for your video ads")

Keep it short.

---

## Connector availability and graceful degradation

- **Shopify connected**: best context (product details, reviews, photos)
- **No Shopify**: buyer pastes specs — brief still gets written, hooks still pulled from product info + brand voice
- **No connectors at all**: skill works fully from pasted context. UGC briefs don't depend on connectors the way other skills do.

---

## Edge cases

- **Creator has already shot something the buyer doesn't like and wants a redo brief**: ask what specifically didn't work. Use that as anti-direction in the do's-and-don'ts. Write the new brief tighter on those dimensions.
- **Creator is shooting for a regulated category (supplements, beauty claims, financial)**: pull in the relevant compliance constraints from the buyer's industry. Always include the FTC disclosure for paid. Flag claims the buyer wants but that creators legally cannot make.
- **Multi-language UGC**: brief defaults to English. If the buyer says "creators in [language]," produce the brief in English (for the buyer) with the hooks and talking points translated for the creator at the bottom.
- **Tight turnaround (under 48 hours)**: warn the buyer that quality UGC takes time. Tight briefs lead to thin content. Offer to write a more focused brief (fewer hooks, fewer b-roll asks) that creators can execute fast.
- **Creator is doing a "day in the life" or vlog-style integration** (vs a dedicated product ad): use a different b-roll structure — fewer dedicated product shots, more product-in-context shots. Note in the brief.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema
- `templates/brief-types-library.md` — organic / paid / affiliate brief structures
- `templates/platform-conventions.md` — TikTok / Reels / Stories / YouTube Shorts specs
- `templates/hook-archetypes.md` — 5 archetypes with examples per archetype
- `templates/bsroll-shotlist-patterns.md` — b-roll shot patterns for product UGC
- `templates/ftc-and-rights.md` — FTC disclosure language + usage rights for paid
- `templates/campaign-mode.md` — multi-creator hook distribution + per-creator personalization
- `scripts/config_loader.py` — shared config loader
- `scripts/ugc_hook_cache.py` — shared hooks cache reader/writer (identical copy ships with the Ad Creative Generator, Email Flow Architect and Campaign Calendar Planner)
- `scripts/render_brief_docx.py` — single + per-creator brief renderer
- `scripts/render_campaign_xlsx.py` — campaign hook-assignment workbook renderer
- `examples/single-organic-tiktok-example.md` — reference output, organic TikTok
- `examples/single-paid-reels-example.md` — reference output, Spark Ads on Reels
- `examples/campaign-mode-example.md` — reference output, multi-creator campaign
