# PDP Output — Reference Example

Fictional product used only to show structure — never reproduce verbatim.

**Product:** River Stone Ceramic Pour-Over
**Page type:** PDP
**Framework selected:** JTBD (Jobs To Be Done) — fits a tool that's hired for a specific morning ritual
**Keywords source:** Listing SEO Optimizer cache (top 10 keywords woven into hero, value props, FAQ)

---

## Brief (.docx) structure

```
River Stone Ceramic Pour-Over — Landing Page Brief
Generated 2026-05-21 · Brand: {{brand_name}} · Page type: Product Detail Page
Framework: JTBD — product is "hired" for the daily morning coffee ritual
Keywords used: ceramic pour over, handmade ceramic pour over, single cup pour over,
  stoneware pour over, paperless coffee dripper, reusable coffee filter, slow coffee ritual
  (source: seo_cache)

══════════════════════════════════════════════════
PAGE ARCHITECTURE
══════════════════════════════════════════════════

HERO
Purpose: 3-second qualification — confirms the shopper is in the right place.

Headline: One handmade ceramic pour-over. One perfect cup. Three minutes.
Sub-headline: Hand-thrown stoneware dripper with a reusable mesh filter. Built for the
  morning when you want real coffee, not a ritual.
CTA: Shop the pour-over
Trust signals: ★★★★★ 4.8 (1,247 reviews) · Free shipping over $50 · 30-day money-back
Visual brief: Overhead hero shot — dripper on a wooden countertop, brewing in motion, steam
  rising, soft morning light from a window. 1200×1200 sq.
Designer notes: Hero image should feel calm and inhabited, not staged. Use the customer's
  kitchen if possible; otherwise a neutral wood surface with no other props.

VALUE PROPS
Purpose: scan-friendly benefit summary for the shopper who didn't read the hero closely.

[5 icon + benefit bullets]
☕  Slow craft, fast brew — small-batch ceramic that drips one cup in under three minutes
♻️  No paper, no waste — stainless mesh filter included, swaps right in
🏠  Built to live out — dishwasher-safe stoneware and cork base, no babying required
🤚  Single-cup discipline — fits over your mug, no carafe to wash
🌿  Made by hand, not a machine — every piece is slightly its own

[...remaining blocks: STORY, WALKTHROUGH, HOW IT WORKS (skipped — product is self-evident),
  COMPARISON (skipped — pour-over category isn't spec-driven), SOCIAL PROOF, FAQ,
  STICKY CTA, CROSS-SELL, TRUST FOOTER...]

══════════════════════════════════════════════════
ALTERNATE HERO BLOCKS (for A/B testing)
══════════════════════════════════════════════════

Hero A — Problem-aware
Headline: Coffee at home doesn't have to mean a $400 machine.
Sub-headline: Hand-thrown ceramic pour-over. One cup, three minutes, no countertop hog.
Visual brief: Side-by-side: cluttered counter with espresso machine (left) vs clean counter
  with the pour-over (right). Or just the clean counter, with negative space.
CTA: Try the simpler way

Hero B — Outcome-aware
Headline: Slow Saturday mornings start with the perfect cup.
Sub-headline: One cup. Three minutes. No paper, no machines. Just stoneware, hot water,
  and good coffee.
Visual brief: Lifestyle: someone in a robe pouring water into the dripper, mug in hand,
  morning light. Warm, unhurried.
CTA: Shop the pour-over

Hero C — Social-proof-aware
Headline: 1,247 five-star reviews. Featured in The Sprudge Coffee Guide. Yours next.
Sub-headline: Hand-thrown ceramic pour-over with reusable filter. The pour-over coffee
  reviewers keep saying changed their morning.
Visual brief: Clean overhead shot with three small press logos and a single pull-quote
  from a review.
CTA: Order yours

══════════════════════════════════════════════════
RECOMMENDED A/B TEST
══════════════════════════════════════════════════
Test first: Hero B (Outcome-aware)
Why: The current main hero is JTBD-framed (job/constraints/outcome). The biggest unknown is
  whether the audience responds more to the *outcome* angle (slow mornings, perfect cup) than
  to the *task* angle (brews one cup in three minutes). Hero B isolates that.
Test duration: 14-21 days depending on traffic volume.
Expected lift band: 5-15% on add-to-cart rate if the audience skews lifestyle-aspirational
  (likely for a $68 ceramic pour-over).
```

---

## HTML (.html) structure (excerpt)

```html
<!--
  Landing Page HTML — River Stone Ceramic Pour-Over
  Generated 2026-05-21 · Brand: {{brand_name}} · Page type: Product Detail Page
  Framework: JTBD

  USAGE: paste any section into your Shopify section / page builder. Tailwind required.
  ...
  TABLE OF CONTENTS:
    1. HERO
    2. VALUE PROPS
    3. STORY
    4. WALKTHROUGH
    5. SOCIAL PROOF
    6. FAQ
    7. FINAL CTA
    8. TRUST FOOTER
    Alternate hero blocks (for A/B testing):
      - Hero A — Problem-aware
      - Hero B — Outcome-aware
      - Hero C — Social-proof-aware
-->

<!-- =================================================================
     HERO
     Conversion job: 3-second qualification — confirms shopper is in the right place
     ================================================================= -->
<section class="lp-hero w-full py-12 md:py-20 px-4 md:px-8 bg-stone-50">
  <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
    <div>
      <h1 class="text-3xl md:text-5xl font-bold tracking-tight text-gray-900">
        One handmade ceramic pour-over. One perfect cup. Three minutes.
      </h1>
      <p class="mt-6 text-lg md:text-xl text-gray-700 leading-relaxed">
        Hand-thrown stoneware dripper with a reusable mesh filter. Built for the morning when you want real coffee, not a ritual.
      </p>
      <div class="mt-8 flex flex-col sm:flex-row gap-4">
        <a href="#" class="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition-colors w-full sm:w-auto">
          Shop the pour-over
        </a>
      </div>
      <div class="mt-6 flex items-center gap-4 text-sm text-gray-600">
        <span aria-label="Rating: 4.8 out of 5">★★★★★ 4.8 · 1,247 reviews</span>
        <span>· Free shipping over $50</span>
        <span>· 30-day money-back</span>
      </div>
    </div>
    <div>
      <img
        src="REPLACE_WITH_YOUR_IMAGE"
        alt="Hero shot: River Stone ceramic pour-over on a wooden countertop, brewing in motion, steam rising, soft morning light"
        width="1200"
        height="1200"
        class="w-full h-auto rounded-lg object-cover"
      />
    </div>
  </div>
</section>

<!-- =================================================================
     VALUE PROPS
     Conversion job: scan-friendly benefit summary
     ================================================================= -->
<section class="lp-value-props w-full py-12 md:py-20 px-4 md:px-8">
  <div class="max-w-7xl mx-auto">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div class="text-center">
        <div class="text-4xl mb-3">☕</div>
        <h3 class="text-xl font-semibold text-gray-900">Slow craft, fast brew</h3>
        <p class="mt-2 text-base text-gray-700">Small-batch ceramic that drips one cup in under three minutes.</p>
      </div>
      <!-- ... 4 more value-prop cards ... -->
    </div>
  </div>
</section>

<!-- ... STORY, WALKTHROUGH, SOCIAL PROOF, FAQ, FINAL CTA, TRUST FOOTER blocks ... -->

<!-- =================================================================
     ALTERNATE HERO BLOCKS (A/B TEST CANDIDATES)
     Each alternate is independently runnable in your A/B testing tool.
     Copy one at a time. Don't ship multiple heroes live simultaneously.
     ================================================================= -->

<!-- =================================================================
     ALTERNATE Hero A — Problem-aware
     For A/B testing against the main hero above.
     ================================================================= -->
<section class="lp-hero lp-hero-alt-a w-full py-12 md:py-20 px-4 md:px-8 bg-stone-50">
  <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
    <div>
      <h1 class="text-3xl md:text-5xl font-bold tracking-tight text-gray-900">
        Coffee at home doesn't have to mean a $400 machine.
      </h1>
      <p class="mt-6 text-lg md:text-xl text-gray-700 leading-relaxed">
        Hand-thrown ceramic pour-over. One cup, three minutes, no countertop hog.
      </p>
      <div class="mt-8">
        <a href="#" class="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition-colors w-full sm:w-auto">
          Try the simpler way
        </a>
      </div>
    </div>
    <div>
      <img src="REPLACE_WITH_YOUR_IMAGE" alt="Side-by-side comparison: cluttered counter with espresso machine vs clean counter with pour-over" width="1200" height="1200" class="w-full h-auto rounded-lg object-cover" />
    </div>
  </div>
</section>

<!-- ... Hero B (Outcome-aware) and Hero C (Social-proof-aware) follow ... -->
```

---

## Notes on this exemplar

- Framework selection is explicit in both outputs (JTBD chosen because the product is hired for a specific morning ritual).
- Keywords from the SEO Optimizer cache are woven into the headline ("ceramic"), sub-headline ("hand-thrown stoneware"), value props ("paperless"), and FAQ ("dishwasher safe", "reusable filter").
- Three alternate heroes use distinctly different angles, not minor word swaps.
- A/B test recommendation is specific and grounded in the main hero's framework.
- HTML is mobile-first (single column on mobile, two-column on desktop).
- Every image has a real `alt` attribute describing what the image *should be* (the buyer rewrites these as shopper-facing alt once they swap in real images).
- The .docx brief is for the buyer to read and share; the .html file is for the buyer to paste into their store.
