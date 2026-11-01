# Collection Page Output — Reference Example

Fictional collection used only to show structure.

**Collection:** Slow Mornings (a curated coffee + tea + ritual collection)
**Page type:** Collection
**Framework selected:** FAB (Features → Advantages → Benefits) — fits a curated category where the buyer needs to understand what each piece adds

---

## Brief structure

```
Slow Mornings — Landing Page Brief
Generated 2026-05-21 · Brand: {{brand_name}} · Page type: Collection / Category Page
Framework: FAB — each curated item's contribution to the morning ritual gets named explicitly
Keywords used: pour over, ceramic pour over, slow coffee ritual, morning routine, single cup brewer
  (source: seo_cache — pulled from individual product caches in this collection)

══════════════════════════════════════════════════
PAGE ARCHITECTURE
══════════════════════════════════════════════════

COLLECTION HERO
Purpose: orient the shopper — what this collection is, who it's for, why curated this way.

Headline: Built for the way Saturdays should feel.
Sub-headline: Eight pieces that turn the first hour of your day into something you'd take
  a photo of. Curated for slow drinkers, late risers, and people who like one good cup
  more than three fast ones.
Quick stat: 8 items · Free shipping over $50 on this collection
Visual brief: Full-width lifestyle shot. Slow morning scene: open book, mug in foreground,
  pour-over in soft focus. Avoid stock-photo cliches.

TOP-OF-GRID COPY
Purpose: route the shopper into the grid with one clear suggestion.

The collection's centerpiece is the River Stone Pour-Over. If you're new to slow coffee,
start there — the bundle below pairs it with the right filter and brew journal at a
15% discount.

[CTA: View the starter bundle →]

[Product grid handled by Shopify — 8 products in 4×2 layout. Card tone: scannable,
  voice-aligned product names.]

MID-GRID BREAK (after row 1)
Purpose: editorial break to break visual rhythm.

[Story block with image: 100-word note from the founder about why she curated this set
  — the morning her coffee-shop wifi went down and she had to make her own at home,
  realized she liked it better.]

BELOW-GRID COPY
Purpose: capture the shopper who's about to leave with decision support.

[Collection FAQ — 5 questions:]
- Where should a complete beginner start?
- Can I gift this whole collection as a set?
- Will the ceramic chip if I'm rough with it?
- Are the items in this collection dishwasher safe?
- Do you ship internationally?

[Newsletter capture: "Get our weekly Slow Mornings pick — one new piece + one new playlist."]

CROSS-COLLECTION NAV
- Teaware collection
- Home office desk collection
- Kitchen tools collection

TRUST FOOTER (standard)
```

---

## HTML structure (excerpt)

```html
<!-- =================================================================
     COLLECTION HERO
     Conversion job: orient the shopper to the collection's positioning
     ================================================================= -->
<section class="lp-collection-hero w-full py-16 md:py-24 px-4 md:px-8 bg-stone-100">
  <div class="max-w-7xl mx-auto text-center">
    <h1 class="text-4xl md:text-6xl font-bold tracking-tight text-gray-900">
      Built for the way Saturdays should feel.
    </h1>
    <p class="mt-6 text-lg md:text-xl text-gray-700 leading-relaxed max-w-3xl mx-auto">
      Eight pieces that turn the first hour of your day into something you'd take a photo of. Curated for slow drinkers, late risers, and people who like one good cup more than three fast ones.
    </p>
    <div class="mt-6 text-sm text-gray-600">
      8 items · Free shipping over $50 on this collection
    </div>
  </div>
</section>

<!-- =================================================================
     TOP-OF-GRID COPY
     Conversion job: route the shopper into the grid with one clear suggestion
     ================================================================= -->
<section class="lp-collection-top w-full py-8 md:py-12 px-4 md:px-8">
  <div class="max-w-4xl mx-auto text-center">
    <p class="text-base md:text-lg text-gray-700 leading-relaxed">
      The collection's centerpiece is the <strong>River Stone Pour-Over</strong>. If you're new to slow coffee, start there — the bundle below pairs it with the right filter and brew journal at a 15% discount.
    </p>
    <a href="#" class="mt-6 inline-flex items-center px-6 py-3 text-base font-semibold text-gray-900 border border-gray-900 rounded-lg hover:bg-gray-900 hover:text-white transition-colors">
      View the starter bundle →
    </a>
  </div>
</section>

<!-- ... product grid (Shopify-rendered), mid-grid break, below-grid FAQ, etc. -->
```

---

## Notes

- Collection pages produce fewer "blocks" than PDPs because the product grid does most of the work.
- The skill outputs copy *around* the grid — Shopify renders the grid itself.
- Mid-grid editorial breaks are the highest-leverage block on a collection page; most stores skip them.
- Cross-collection nav makes shoppers feel they're on a curated site, not just scrolling a catalog.
