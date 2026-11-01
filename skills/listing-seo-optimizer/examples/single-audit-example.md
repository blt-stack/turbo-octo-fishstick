# Single-Audit Output — Reference Example

This is the structure the renderer produces for a single product. The product below is fictional and exists only to show the shape — never reproduce it verbatim in real output.

---

## Example product

- **Name:** River Stone Ceramic Pour-Over
- **Source:** Shopify product handle `river-stone-pour-over`
- **Existing listing fields:** title, body description, some images without alt text, no meta description, default URL handle

---

## Output structure to match

```
River Stone Ceramic Pour-Over — SEO Audit & Optimization
Generated 2026-05-21 · Brand: {{brand_name}} · Source: Shopify

══════════════════════════════════════════════════
AUDIT SUMMARY
══════════════════════════════════════════════════
Shopify: 64.5/100  (Mediocre)
Amazon:  58.0/100  (Weak)
Etsy:    72.5/100  (Strong)
TikTok Shop: — (not enabled)

Shopify — sub-score breakdown
  • Keyword Coverage: 18.0/30
  • Title Strength: 16.0/20
  • Bullet Quality: 14.0/20  (rescaled for Shopify value-prop block)
  • Backend Structured: 4.5/15
  • Completeness: 12.0/15

Amazon — sub-score breakdown
  • Keyword Coverage: 21.0/30
  • Title Strength: 14.0/20
  • Bullet Quality: 12.0/20
  • Backend Structured: 4.0/15  ← biggest miss
  • Completeness: 7.0/15

Etsy — sub-score breakdown
  • Keyword Coverage: 24.0/30
  • Title Strength: 18.0/20
  • Bullet Quality: 14.0/20  (rescaled — Etsy uses description structure)
  • Backend Structured: 9.5/15
  • Completeness: 7.0/15

Strongest dimensions across all platforms: title strength, keyword coverage
Weakest dimensions: backend / structured fields, completeness

══════════════════════════════════════════════════
KEYWORD RESEARCH
══════════════════════════════════════════════════
Top 18 ranked keywords:

1. **ceramic pour over** [transactional] [sources: amazon_autocomplete, google_suggest, llm]
    → Use in: amazon_title, shopify_title, shopify_meta_title, etsy_title
    Note: Primary head term. Should appear in the first 5 words of every title.

2. **handmade ceramic pour over** [transactional] [sources: amazon_autocomplete, llm]
    → Use in: shopify_title, etsy_title, etsy_tag

3. **single cup pour over** [transactional] [sources: google_suggest, amazon_autocomplete, llm]
    → Use in: amazon_title, amazon_bullet_1, etsy_tag

4. **stoneware pour over** [transactional] [sources: amazon_autocomplete, llm]
    → Use in: amazon_bullet_2, etsy_tag, shopify_body

5. **paperless coffee dripper** [transactional] [sources: google_suggest, llm]
    → Use in: amazon_bullet_2, amazon_backend, shopify_body

6. **reusable coffee filter** [transactional] [sources: amazon_autocomplete, google_suggest]
    → Use in: amazon_bullet_3, amazon_backend, etsy_tag

7. **slow coffee ritual** [audience/occasion] [sources: llm]
    → Use in: shopify_body, etsy_tag, shopify_meta_description

8. **single serve coffee maker no electricity** [transactional] [sources: google_suggest]
    → Use in: amazon_backend, etsy_tag

[...continues to keyword 18...]

══════════════════════════════════════════════════
SHOPIFY — Audit + Rewrite
══════════════════════════════════════════════════
Issues found:
  • Meta description missing — Shopify is auto-generating from body
  • 3 of 5 images missing alt text
  • URL handle is /products/river-stone-product-43 (auto-generated) — should be /products/ceramic-pour-over-coffee-dripper or similar
  • Body keyword coverage misses "paperless coffee dripper" and "reusable coffee filter"

Rewrite:
  Meta title (58/60): Ceramic Pour Over Coffee Dripper | Handmade Stoneware | {{brand_name}}
  Meta description (152/160): Hand-thrown ceramic pour-over for one perfect cup. Reusable stainless filter included, dishwasher safe. Made in small batches. Shop now.
  URL handle: /products/ceramic-pour-over-coffee-dripper

  Recommended alt text per image:
    Image 1: Ceramic pour over coffee dripper — front view, on cork base
    Image 2: Ceramic pour over in use — pouring water through coffee grounds
    Image 3: Reusable stainless steel mesh filter — close-up
    Image 4: Ceramic pour over showing matte stoneware glaze
    Image 5: Ceramic pour over on kitchen counter — lifestyle shot

  Body keyword integration notes:
    - Primary keyword "ceramic pour over" should appear in: H1 (×1), intro paragraph (×1), Materials section heading (×1), FAQ answer (×1)
    - Add a "Paperless brewing" sub-section to cover "paperless coffee dripper" and "reusable coffee filter" keywords naturally
    - Use semantic variations: pour over dripper, pour over coffee maker, ceramic dripper

  Schema markup notes:
    - Verify your theme outputs Product schema (most Shopify themes do)
    - Add aggregateRating + review schema once you have reviews
    - Verify offers.price is exposed (some themes hide this)

══════════════════════════════════════════════════
AMAZON — Audit + Rewrite
══════════════════════════════════════════════════
Issues found:
  • Backend search terms field is empty (0/250 bytes) — biggest miss
  • Only 4 of 5 bullets used
  • Title is 87/200 chars — well under sweet spot (150-180)
  • No A+ Content (skill notes if brand registered)
  • 2 of 5 bullets don't open with a clear benefit headline

Rewrite:
  Title (162/200): {{brand_name}} Ceramic Pour Over Coffee Dripper, Handmade Stoneware Single Cup Brewer with Reusable Stainless Filter, Dishwasher Safe, Paperless Coffee Maker
  Bullet 1 (193/250): ONE PERFECT CUP — Single-cup ceramic pour over brews 10-12 oz of pour-over coffee in under three minutes, no carafe or extra gear required.
  Bullet 2 (201/250): PAPERLESS BREWING — Included reusable stainless mesh filter eliminates paper waste and pays for itself in months — fits a paperless coffee dripper routine.
  Bullet 3 (188/250): BUILT FOR DAILY USE — Dishwasher-safe stoneware and cork-based stability mean you'll keep this ceramic pour over on the counter, not stashed in a cabinet.
  Bullet 4 (192/250): HOLDS HEAT EVENLY — Stoneware body retains brewing temperature better than glass or plastic, producing a more even extraction every time.
  Bullet 5 (198/250): HAND-THROWN, NOT MASS-PRODUCED — Each piece is shaped individually in a small studio, with subtle variations that make every dripper one-of-a-kind.

  Description (1840/2000): [full 1800-char description with keyword integration]

  Backend search terms (231/250 bytes):
  paperless coffee dripper reusable stainless filter single serve no electricity slow ritual brewer barista gift handcrafted matte glaze kitchen drip morning coffee artisan small batch

  Compliance check:
    ✓ Title under 200 chars
    ✓ No trademark symbols
    ✓ No external URLs
    ✓ No CTAs
    ✓ No prohibited claims

  A+ Content notes:
    - If brand registered, recommend a 3-module A+ Content layout: Hero comparison module, Materials/craft module, Care/use module. Defer module creation to the A+ Content Creator skill.

══════════════════════════════════════════════════
ETSY — Audit + Rewrite
══════════════════════════════════════════════════
[same structure]

══════════════════════════════════════════════════
ACTION CHECKLIST
══════════════════════════════════════════════════
Ordered by estimated impact:
☐ Fill Amazon backend search terms (231 bytes available) — biggest single SEO lift, ~+14 pts to Amazon score
☐ Write Amazon Bullet 5 (currently empty) — ~+3 pts
☐ Add Shopify meta description (152 chars) — improves Google CTR
☐ Set Shopify URL handle to /products/ceramic-pour-over-coffee-dripper (redirect old handle)
☐ Add alt text to all 5 Shopify product images
☐ Add Etsy tag #9-13 (currently 8/13 used)
☐ Rewrite Amazon Bullet 2 to open with benefit headline
☐ Fill Etsy attributes: Occasion (gift), Recipient (coffee lover), Style (minimalist)
☐ Verify Shopify product schema in theme code (or install Schema App)
☐ If brand-registered on Amazon, queue A+ Content build via A+ Content Creator skill
```

---

## Notes on this exemplar

- Sub-scores are itemized so the buyer sees exactly *why* a score is what it is.
- Every issue gets a fix in the rewrite section — no dead-end criticism.
- The action checklist is ordered by impact, not by platform — buyer can knock down the highest-leverage items first.
- Character counts shown inline on every constrained field.
- Keywords show their source so the buyer knows whether the recommendation is grounded in real autocomplete data or LLM inference alone.
- The Amazon section flags compliance separately from scoring — title compliance failures suppress listings entirely, not just rank lower.
- The skill writes `~/.the-ecommerce-seller/cache/keywords/river-stone-pour-over.json` after this run, so the Product Description Writer auto-picks-up these keywords next time it runs on this product.
