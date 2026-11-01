---
name: bundle-builder
description: >
  Generates product bundle recommendations using a hybrid discovery engine combining Apriori
  market-basket co-purchase mining, categorical complementarity (use-case mapping), and margin
  optimization. Suggests 5 bundle types: Frequently-Bought-Together, Complementary, AOV-Lift
  (calibrated to free-shipping threshold), Gift Sets, and Starter Kits. Each bundle gets 3 pricing
  tiers and 3 positioning copy variants. Outputs .docx for single bundles or .xlsx (5 sheets) for bulk
  catalog mode. Use this skill when the user mentions bundles, product bundles, bundle ideas,
  frequently bought together, FBT, AOV lift, starter kit, gift set, 'what should I bundle,' 'increase
  my AOV,' 'free shipping threshold,' or 'Shopify bundle setup.' Writes bundle definitions to shared
  cache for downstream skills (PDP copy, ads, landing pages).
---

# Bundle Builder

Suggests product bundles using a hybrid engine: Apriori co-purchase mining + categorical complementarity + margin optimization. Five bundle types. Three pricing tiers. Cross-skill cache writes.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Detect mode.** Single bundle (buyer specifies anchor SKU or use-case) or bulk catalog suggestions.
3. **Ingest sales + product data.** Shopify Orders CSV + product catalog (with categories + cost data if available).
4. **Run hybrid discovery.** Apriori co-purchase mining + categorical complementarity + margin optimization layers.
5. **Filter by bundle type.** FBT / Complementary / AOV-Lift / Gift Set / Starter Kit.
6. **Score + rank.** Each candidate bundle gets a composite score from support, lift, margin, AOV impact.
7. **Compute pricing tiers.** Conservative / standard / aggressive — each with margin impact check.
8. **Generate positioning copy.** Bundle name + 3 copy variants per bundle.
9. **Write bundle cache.** For downstream skills (landing page, product description, ad creative) to consume.
10. **Render output.** Single mode → `.docx`. Bulk mode → `.xlsx`.
11. **Report back.** File path, bundle count, expected AOV-lift estimate, suggested next step.

---

## Step 1: First-run check

Look for `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`. If missing, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

---

## Step 2: Detect mode

**Single bundle mode** when:
- Buyer specifies an anchor SKU ("build a bundle around the River Stone Pour-Over")
- Buyer specifies a use-case ("a gift bundle for Mother's Day")
- Buyer asks for one focused, polished bundle

**Bulk catalog mode** when:
- Buyer uploads a sales CSV without further direction
- Buyer says "suggest bundles," "what bundles should I make," "find me 10 bundle opportunities"
- Buyer asks for catalog-wide AOV-lift opportunities

Confirm out loud before proceeding.

---

## Step 3: Ingest sales + product data

Required:
- **Sales CSV** (orders with line items — Shopify Orders CSV is canonical; same shapes as skill #12 supports)
- **Product catalog** (SKU, product_name, optional: category, cost_usd, retail_price_usd, is_in_stock)

Optional but valuable:
- **Inventory forecast data** from skill #12's last run (favors in-stock + healthy-velocity SKUs)
- **Testimonial cache** from skill #10 (surfaces social proof per bundle)
- **Margin floor** from buyer config

If product catalog cost data is missing, the skill computes bundles but skips margin layers; flags this in output.

Read `templates/data-requirements.md` for full ingest schema.

---

## Step 4: Run hybrid discovery

Three layers, each producing candidate bundles:

### Layer 1: Apriori co-purchase mining

Read `templates/apriori-discovery.md`. Implementation in `scripts/copurchase_analyzer.py`:

1. Build market basket from sales CSV — each order = one basket of SKUs
2. Apriori algorithm computes:
   - **Support** = % of orders containing this item set
   - **Confidence** = P(item B | item A) — probability of B given A
   - **Lift** = P(A,B) / (P(A) × P(B)) — how much more likely they co-occur vs. random
3. Filter at thresholds (config-configurable, defaults below):
   - min support ≥ 0.01 (item set appears in 1%+ of orders)
   - min confidence ≥ 0.20 (≥20% of A buyers also buy B)
   - min lift ≥ 1.5 (1.5× more likely than chance)
4. Output bundle candidates with co-purchase statistics

### Layer 2: Categorical complementarity

Read `templates/categorical-mapping.md`. Implementation in `scripts/categorical_complementarity.py`:

1. Map each SKU to one or more categories (buyer maps during onboarding or skill auto-classifies from product names)
2. Read `templates/use-case-mappings.md` for cross-category combinations that fit a shared use-case:
   - coffee_brewing: pour-over + filters + carafe + grinder
   - skincare_routine: cleanser + toner + serum + moisturizer
   - desk_setup: keyboard + mouse + monitor + cable_organizer
3. For each use-case where the brand has SKUs across 3+ categories, generate a candidate bundle
4. Output bundles with use-case label

### Layer 3: Margin optimization

Read `templates/margin-optimization.md`. Implementation in `scripts/margin_optimizer.py`:

1. For each candidate bundle from layers 1+2, compute:
   - Total individual price (sum of retail prices)
   - Total cost (sum of cost_usd)
   - Current blended margin %
2. For bundles with a low-margin "attractor" SKU + high-margin "add-on" SKUs:
   - Flag as margin-positive bundle (offering bundle improves blended margin vs. discounting attractor alone)
3. Drop candidates where blended margin < config.bundle_builder.margin_floor

---

## Step 5: Filter by bundle type

Each candidate gets assigned one or more of the 5 bundle types:

| Type | Filter logic | Source layer | Template |
|---|---|---|---|
| Frequently-Bought-Together | High co-purchase lift (≥2.0) + high support | Apriori | `templates/type-fbt.md` |
| Complementary Category | Cross-category combo from use-case mapping | Categorical | `templates/type-complementary.md` |
| AOV-Lift | Bundle total above free-shipping threshold + 1-2 SKUs the buyer would otherwise leave | Margin + Apriori | `templates/type-aov-lift.md` |
| Gift Set | Cross-category + presentation-suitable + occasion mapping | Categorical | `templates/type-gift-set.md` |
| Starter Kit | Hero SKU + 1-2 complementary SKUs at deeper discount | Categorical + Margin | `templates/type-starter-kit.md` |

A bundle can qualify for multiple types (e.g., a Coffee Brewing bundle might be both FBT + Complementary). The skill assigns the most relevant primary type and notes secondary types.

---

## Step 6: Score + rank

Each candidate bundle gets a composite score:

```
score = (0.30 × support_score) +
        (0.25 × lift_score) +
        (0.20 × margin_score) +
        (0.15 × aov_lift_potential) +
        (0.10 × in_stock_velocity_score)
```

Where each sub-score is normalized 0-100. The weights are config-tunable.

`in_stock_velocity_score` reads from skill #12's inventory forecast — favors bundles where all SKUs are in stock + have healthy velocity (urgency = "healthy") over bundles with stockout-risk SKUs.

Sort bundles by score descending. Buyer sees top N (default 20) in bulk mode.

---

## Step 7: Compute pricing tiers

Read `templates/pricing-tiers.md`. For each bundle, compute three pricing tiers:

| Tier | Discount | Use case |
|---|---|---|
| Conservative | 5-10% | Low margin risk; safe to test |
| Standard | 12-18% | Typical FBT bundle discount |
| Aggressive | 20-25% | Promo / starter kit / clearance |

For each tier, output:
- Bundle price
- Savings vs. individual ($ and %)
- Blended margin % at this price
- Flag if margin drops below `config.bundle_builder.margin_floor` (default 25%)
- Recommended use case (when to deploy this tier)

The buyer picks the tier per bundle. The skill defaults to "standard" but flags when conservative or aggressive is the better fit (e.g., low-margin attractor bundles default to conservative).

---

## Step 8: Generate positioning copy

Read `templates/positioning-copy.md`. For each bundle, generate:

### Bundle name
Two name styles per bundle:
- **Descriptive** ("Complete Coffee Brewing Set")
- **Evocative** ("The Slow Morning Bundle")

### Positioning copy variants (3 per bundle)
- **Benefit-led**: "Save $X and get everything you need for the perfect cup..."
- **Story-led**: "We built this set the way we drink coffee at home — slow, deliberate, and..."
- **Social-proof-led**: "The pieces our customers reach for together — now at one price."

The Social-proof variant pulls a relevant testimonial from `~/.the-ecommerce-seller/cache/testimonials/` (written by skill #10). Falls back to brand-voice-only if no testimonial available.

---

## Step 9: Write bundle cache

For each finalized bundle, write to:

```
~/.the-ecommerce-seller/cache/bundles/{bundle-slug}.json
```

Schema:

```json
{
  "bundle_id": "coffee-brewing-set",
  "bundle_name_descriptive": "Complete Coffee Brewing Set",
  "bundle_name_evocative": "The Slow Morning Bundle",
  "bundle_type_primary": "complementary",
  "bundle_type_secondary": ["fbt"],
  "skus_included": [
    {"sku": "RS-POUR-OVER-001", "product_name": "River Stone Pour-Over", "qty": 1, "individual_price_usd": 48.00, "cost_usd": 14.00},
    {"sku": "FILTER-100PK", "product_name": "Filter Pack (100)", "qty": 1, "individual_price_usd": 12.00, "cost_usd": 3.00},
    {"sku": "CARAFE-1L", "product_name": "Glass Carafe 1L", "qty": 1, "individual_price_usd": 32.00, "cost_usd": 10.00}
  ],
  "pricing_tiers": {
    "conservative": {"bundle_price_usd": 84.00, "discount_pct": 0.077, "savings_usd": 8.00, "blended_margin_pct": 0.68},
    "standard":     {"bundle_price_usd": 76.50, "discount_pct": 0.16,  "savings_usd": 15.50, "blended_margin_pct": 0.65},
    "aggressive":   {"bundle_price_usd": 69.00, "discount_pct": 0.24,  "savings_usd": 23.00, "blended_margin_pct": 0.61}
  },
  "recommended_tier": "standard",
  "positioning_copy": {
    "benefit_led": "...",
    "story_led": "...",
    "social_proof_led": "..."
  },
  "discovery_evidence": {
    "apriori_support": 0.04,
    "apriori_confidence": 0.41,
    "apriori_lift": 2.8,
    "categorical_use_case": "coffee_brewing",
    "margin_score": 75,
    "in_stock_velocity_score": 92,
    "composite_score": 84.3
  },
  "shopify_setup": {
    "structure": "fixed_bundle",
    "parent_sku": "BUNDLE-COFFEE-BREWING-001",
    "variant_skus": ["RS-POUR-OVER-001", "FILTER-100PK", "CARAFE-1L"]
  },
  "testimonials_referenced": ["judge_me-12345"],
  "created_at": "2026-05-22T10:30:00Z",
  "created_by": "bundle-builder"
}
```

Downstream consumers:
- **Landing Page Copywriter (#3)** reads bundles to generate bundle landing pages
- **Product Description Writer (#1)** reads to generate bundle PDPs
- **Ad Creative Generator (#5)** reads as bundle-format ad concepts
- **Campaign Calendar Planner (#8)** can read for promotional bundle scheduling

---

## Step 10: Render output

### Single bundle mode

Use `scripts/render_bundle_docx.py`. Structure:

```
Bundle: [Bundle name evocative]  (alt: [descriptive])
Type: [primary] (+ [secondary])
Generated: [date]
Composite score: [N/100]

══════════════════════════════════════════════════
SKUS INCLUDED
══════════════════════════════════════════════════
[Table of SKUs with qty, individual price, cost]
Individual total: $X
Cost total: $X

══════════════════════════════════════════════════
PRICING TIERS
══════════════════════════════════════════════════
Conservative — $X (X% off) — Margin: X%
Standard     — $X (X% off) — Margin: X%  ← Recommended
Aggressive   — $X (X% off) — Margin: X%

══════════════════════════════════════════════════
DISCOVERY EVIDENCE
══════════════════════════════════════════════════
- Co-purchase data: Apriori support X%, confidence Y%, lift Z×
- Categorical fit: use-case = [coffee_brewing]
- Margin score: X/100
- In-stock velocity: X/100 (all SKUs healthy)

══════════════════════════════════════════════════
POSITIONING COPY (3 variants)
══════════════════════════════════════════════════
Variant A — Benefit-led:
[Copy]

Variant B — Story-led:
[Copy]

Variant C — Social-proof-led:
[Copy + testimonial reference]

══════════════════════════════════════════════════
SHOPIFY SETUP RECOMMENDATION
══════════════════════════════════════════════════
- Structure: [fixed bundle / mix-and-match / collection]
- Parent SKU: [...]
- Variant SKUs: [...]
- App recommendations: [Shopify Bundles, Bold Bundles, etc.]

══════════════════════════════════════════════════
NEXT STEPS
══════════════════════════════════════════════════
[Suggested workflow to launch]
```

Save to `config.output_folder` as `bundle_{bundle-slug}_{date}.docx`.

### Bulk catalog mode

Use `scripts/render_bundles_xlsx.py`. Five-sheet workbook:

**Sheet 1: Bundle Suggestions** — one row per bundle:
- Rank, name, type, composite score
- SKUs included (semicolon-separated)
- Individual price total, recommended bundle price, savings, margin
- All 3 pricing tiers in columns
- Status (Suggested / Approved / Launched / Rejected — buyer fills in)

**Sheet 2: Bundle Type Breakdown** — counts per type, expected AOV-lift contribution per type, recommended deployment cadence

**Sheet 3: SKU Participation** — which SKUs appear in which bundles, helps the buyer spot SKUs that are over-bundled (every bundle has the same hero SKU) or under-bundled (high-velocity SKUs never recommended)

**Sheet 4: AOV-Lift Analysis** — for AOV-Lift bundles specifically: current cart distribution, target threshold, expected lift if X% of buyers convert to the bundle

**Sheet 5: Discovery Audit** — per-bundle: which discovery layer surfaced it (Apriori / categorical / margin), why it ranked where it did, any warnings

Save as `bundle_suggestions_{date}.xlsx`.

---

## Step 11: Report back

Tell the buyer:
1. File path (`computer://` link)
2. Bundle count + distribution by type
3. Top 3 bundles by composite score (with names + projected savings)
4. Cache write summary ("N bundles written to ~/.the-ecommerce-seller/cache/bundles/ — Landing Page Copywriter and Product Description Writer will see these next time you run them")
5. AOV-lift estimate (if AOV-Lift bundles included)
6. Suggested next step:
   - "Pick 2-3 highest-scoring bundles to launch first; run Landing Page Copywriter to generate bundle landing pages from the cache"
   - "If sales data is sparse, the categorical layer carried more weight — bundles will improve as more data accumulates"
   - "Re-run quarterly to surface new bundle opportunities from accumulating co-purchase data"

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Shopify | Skill works on Shopify CSV; flags direct API as upgrade |
| Inventory forecast cache (skill #12) | Skill skips in-stock velocity scoring; weights margin + score higher |
| Testimonial cache (skill #10) | Social-proof copy variant falls back to brand-voice only |
| Cost data | Skill skips margin layer; produces bundles but flags missing margin analysis |

The skill always produces bundles — connectors enrich.

---

## Edge cases

- **Brand with <50 orders**: Apriori produces sparse / unreliable signals. Skill weights categorical layer higher and surfaces "data-light" disclaimer.
- **Brand with one hero SKU + tail**: every co-purchase bundle includes the hero. Skill flags this and recommends categorical bundles that explore variety.
- **Bundle includes a stockout-risk SKU**: skill flags the bundle and recommends either swapping the SKU or holding the bundle until inventory is restored.
- **Bundle pricing puts margin below floor**: skill flags but doesn't exclude — buyer may want to deploy a temporarily-thin-margin bundle for traffic / acquisition purposes.
- **Sister bundles cannibalize each other**: skill detects when two bundles overlap >70% in SKUs and recommends consolidating into one.
- **Variant SKUs (size/color)**: skill treats all variants as the same SKU for bundling logic (a "Cup Bundle" doesn't suggest you bundle two sizes of the same cup).
- **Mature catalog with seasonality**: skill flags seasonal SKUs based on skill #12's seasonality detection and recommends timing bundles to peak season.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config (extended with bundle_builder section)
- `templates/type-fbt.md` — Frequently-Bought-Together patterns + thresholds
- `templates/type-complementary.md` — Complementary Category patterns
- `templates/type-aov-lift.md` — AOV-Lift bundle math + threshold logic
- `templates/type-gift-set.md` — Gift Set occasion mapping + presentation
- `templates/type-starter-kit.md` — Starter Kit patterns for first-time buyers
- `templates/apriori-discovery.md` — Apriori market-basket methodology
- `templates/categorical-mapping.md` — category-to-category complementarity
- `templates/use-case-mappings.md` — pre-built use-case category combinations
- `templates/margin-optimization.md` — margin-aware bundle construction
- `templates/pricing-tiers.md` — conservative / standard / aggressive tier math
- `templates/positioning-copy.md` — name + 3-variant copy patterns
- `templates/data-requirements.md` — required + optional input schemas
- `templates/bundle-cache.md` — schema for `~/.the-ecommerce-seller/cache/bundles/`
- `scripts/config_loader.py` — shared config loader
- `scripts/copurchase_analyzer.py` — Apriori-style market basket analysis
- `scripts/categorical_complementarity.py` — use-case-based bundle discovery
- `scripts/margin_optimizer.py` — margin scoring + filtering
- `scripts/bundle_engine.py` — orchestrates all 3 layers + scoring + pricing
- `scripts/bundle_cache.py` — writes bundles cache for downstream skills
- `scripts/render_bundle_docx.py` — single bundle .docx renderer
- `scripts/render_bundles_xlsx.py` — bulk bundle .xlsx renderer (5 sheets)
- `examples/single-bundle-example.md`
- `examples/bulk-bundle-catalog-example.md`
- `examples/aov-lift-specific-example.md`
