# Single Bundle Deep-Dive — Reference Example

Shows what gets produced when the buyer says "Build a coffee brewing bundle around the River Stone Pour-Over."

**Brand:** {{brand_name}} (ceramics + coffee accessories)
**Anchor SKU:** River Stone Pour-Over
**Bundle type detected:** Complementary (primary) + FBT (secondary)
**Output:** Single `.docx`

---

## Discovery process

The skill checks the anchor SKU and adjacent data:

1. **Apriori layer**: River Stone Pour-Over has 8% co-purchase support with Filter Pack (lift 2.8×). Co-purchase exists; FBT bundle is data-validated.
2. **Categorical layer**: Pour-Over maps to `pour_over_device` category. Matching use-case `coffee_brewing_complete` includes filters + carafe + grinder + kettle + beans. Brand has all 5 available; selects best 3.
3. **Margin layer**: All 3 selected SKUs have cost data. Blended margin at standard tier (15% off) = 65% — well above the 25% floor.

Selected SKUs:
- River Stone Pour-Over (anchor, required category)
- Filter Pack 100 (required category + Apriori match)
- Glass Carafe 1L (optional category, high velocity)

---

## .docx output structure

```
Bundle: The Slow Morning Bundle
Aka: Complete Coffee Brewing Set
Type: Complementary Category (+ FBT)
Generated: 2026-05-22
Composite score: 84.3/100
```

### SKUS INCLUDED

- 1 × River Stone Pour-Over (RS-POUR-OVER-001) — $48.00 [cost $14.00]
- 1 × Filter Pack 100 (FILTER-100PK) — $12.00 [cost $3.00]
- 1 × Glass Carafe 1L (CARAFE-1L) — $32.00 [cost $10.00]

- Individual price total: $92.00
- Cost total: $27.00

### PRICING TIERS

- **Conservative**: $85.10 (7.5% off, save $6.90) — margin 68.3%
- **Standard**: $78.20 (15.0% off, save $13.80) — margin 65.5% ← Recommended
- **Aggressive**: $71.76 (22.0% off, save $20.24) — margin 62.3%

All tiers pass the 25% margin floor.

### DISCOVERY EVIDENCE

- Source layer: apriori + categorical
- Co-purchase support: 4.00% of orders (over 500 baskets)
- Co-purchase confidence: 41.0%
- Co-purchase lift: 2.80× (well above 2.0× threshold)
- Co-occurrence count: 20
- Categorical use-case: coffee_brewing_complete
- Margin score: 75/100
- In-stock velocity score: 92/100 (all SKUs healthy)

### POSITIONING COPY

**Names**
- Descriptive: Complete Coffee Brewing Set
- Evocative: The Slow Morning Bundle

**Variant A — Benefit-led** (recommended for: cart/retargeting)
> "Save $14 when you buy the pour-over, filters, and carafe together."
>
> "Three pieces that work together to make a proper pour-over morning. Skip the guesswork on what goes with what."
>
> CTA: Add the Bundle

**Variant B — Story-led** (recommended for: brand pages/social)
> "The way we drink coffee at home: slow, deliberate, one cup at a time."
>
> "We picked these three pieces because they work together — the pour-over has the spout balance for clean pours, the carafe matches the volume, and the filters are the only kind we'd use ourselves."
>
> CTA: Try the Ritual

**Variant C — Social-proof-led** (recommended for: cold traffic)
> "Hearing that the grip 'feels balanced from the first pour' is exactly what we hoped for."
> — Sam K., verified buyer
>
> "The three pieces our customers reach for most often, together at a lower price."
>
> CTA: See the Bundle

(Testimonial pulled from .cache/testimonials/river-stone-pour-over.json)

**Ad headlines (3 variants)**
- Three pieces. One ritual.
- Save $14 on the brewing set.
- What our customers buy together.

**Ad primary text (3 variants)**
- The pour-over, filters, and carafe — now in one bundle. Save $14 vs. buying separately.
- We picked these three pieces because they work together. Make the perfect cup.
- "This pour-over makes my whole morning feel different." Try the bundle.

### SHOPIFY SETUP RECOMMENDATION

- Structure: Fixed bundle
- Parent SKU: BUNDLE-COMPLETE-COFFEE-BREWING
- Variant SKUs: RS-POUR-OVER-001, FILTER-100PK, CARAFE-1L
- Recommended bundle apps: Shopify Bundles (native), Fast Bundle, Bold Bundles

### NEXT STEPS

1. Create the parent bundle SKU in Shopify
2. Set bundle price at the recommended tier ($78.20)
3. Pick a positioning variant — start with Variant A for PDP, Variant B for landing page
4. Run Landing Page Copywriter (skill #3) — bundle cache is already populated
5. Re-evaluate after 30 days based on sales

---

## Bundle cache write

To `<plugin-root>/.cache/bundles/complete-coffee-brewing-set.json`:

```json
{
  "bundle_id": "complete-coffee-brewing-set",
  "bundle_name_descriptive": "Complete Coffee Brewing Set",
  "bundle_name_evocative": "The Slow Morning Bundle",
  "bundle_type_primary": "complementary",
  "bundle_type_secondary": ["fbt"],
  ...
  "downstream_consumed_by": []
}
```

Skill #1 (Product Description Writer), #3 (Landing Page Copywriter), and #5 (Ad Creative Generator) will see this bundle next time they run.

---

## Time savings

Manually building this bundle:
- Identify the right SKU combination: 15-30 min
- Compute pricing tiers + margin math: 20 min
- Write 3 positioning copy variants: 45-60 min
- Pull a relevant testimonial: rarely done well
- Document the Shopify setup: 10 min
- **Total: 90-120 min, with varying quality**

With this skill:
- Skill runs: ~5 seconds
- Buyer reviews + picks tier + copy variant: ~10 min
- **Total: ~10 min, with cache write + 3 polished copy variants + audit trail**

The compounding value: every bundle gets written to the cache, so the next 9 bundles in the buyer's bundle strategy are all easier (downstream skills already wired in).
