# Bundle Cache — Schema and Downstream Consumers

The bundles the skill produces are persisted to a shared cache. Downstream skills (Landing Page Copywriter, Product Description Writer, Ad Creative Generator, Campaign Calendar Planner) read from this cache to generate bundle-specific content automatically.

## Cache location

```
~/.the-ecommerce-seller/cache/bundles/{bundle-slug}.json
```

One file per bundle. Bundle slug is derived from the bundle name (descriptive style):

```python
def bundle_slug(bundle_name_descriptive: str) -> str:
    return slugify(bundle_name_descriptive)[:80]
```

Example: "Complete Coffee Brewing Set" → `complete-coffee-brewing-set`

## Schema

```json
{
  "bundle_id": "complete-coffee-brewing-set",
  "bundle_name_descriptive": "Complete Coffee Brewing Set",
  "bundle_name_evocative": "The Slow Morning Bundle",
  "bundle_type_primary": "complementary",
  "bundle_type_secondary": ["fbt"],
  "use_case_label": "coffee_brewing_complete",
  "skus_included": [
    {
      "sku": "RS-POUR-OVER-001",
      "product_name": "River Stone Pour-Over",
      "qty": 1,
      "individual_price_usd": 48.00,
      "cost_usd": 14.00,
      "category": "pour_over_device",
      "is_in_stock": true,
      "velocity_units_per_day": 12.3
    },
    {
      "sku": "FILTER-100PK",
      "product_name": "Filter Pack (100)",
      "qty": 1,
      "individual_price_usd": 12.00,
      "cost_usd": 3.00,
      "category": "filters",
      "is_in_stock": true,
      "velocity_units_per_day": 4.5
    },
    {
      "sku": "CARAFE-1L",
      "product_name": "Glass Carafe 1L",
      "qty": 1,
      "individual_price_usd": 32.00,
      "cost_usd": 10.00,
      "category": "carafe",
      "is_in_stock": true,
      "velocity_units_per_day": 6.1
    }
  ],
  "pricing_tiers": {
    "conservative": {"discount_pct": 0.075, "bundle_price_usd": 84.80, "savings_usd": 7.20, "blended_margin_pct": 0.68, "passes_margin_floor": true},
    "standard":     {"discount_pct": 0.15,  "bundle_price_usd": 78.20, "savings_usd": 13.80, "blended_margin_pct": 0.65, "passes_margin_floor": true},
    "aggressive":   {"discount_pct": 0.22,  "bundle_price_usd": 71.76, "savings_usd": 20.24, "blended_margin_pct": 0.62, "passes_margin_floor": true}
  },
  "recommended_tier": "standard",
  "positioning_copy": {
    "names": {
      "descriptive": "Complete Coffee Brewing Set",
      "evocative": "The Slow Morning Bundle"
    },
    "variants": {
      "benefit_led": {
        "tagline": "Save $14 when you buy the pour-over, filters, and carafe together.",
        "body": "Three pieces that work together to make a proper pour-over morning. Skip the guesswork on what goes with what.",
        "cta": "Add the Bundle"
      },
      "story_led": {
        "tagline": "The way we drink coffee at home: slow, deliberate, one cup at a time.",
        "body": "We picked these three pieces because they work together — the pour-over has the spout balance for clean pours, the carafe matches the volume, and the filters are the only kind we'd use ourselves.",
        "cta": "Try the Ritual"
      },
      "social_proof_led": {
        "tagline": "\"Hearing that the grip 'feels balanced from the first pour' is exactly what we hoped for.\"",
        "body": "The three pieces our customers reach for most often, together at a lower price.",
        "attribution": "Sam K., verified buyer",
        "testimonial_source": "judge_me-12345",
        "cta": "See the Bundle"
      }
    },
    "ad_headlines": [
      "Three pieces. One ritual.",
      "Save $14 on the brewing set.",
      "What our customers buy together."
    ],
    "ad_primary_text": [
      "The pour-over, filters, and carafe — now in one bundle. Save $14 vs. buying separately.",
      "We picked these three pieces because they work together. Make the perfect cup.",
      "\"This pour-over makes my whole morning feel different.\" Try the bundle."
    ],
    "ad_cta_options": ["Shop the Bundle", "See What's Included", "Make the Morning"]
  },
  "discovery_evidence": {
    "apriori_support": 0.04,
    "apriori_confidence_max": 0.41,
    "apriori_lift": 2.8,
    "co_occurrence_count": 12,
    "categorical_use_case": "coffee_brewing_complete",
    "categorical_match_strength": "strong",
    "margin_score": 75,
    "margin_improvement_vs_hero_discount": 0.12,
    "in_stock_velocity_score": 92,
    "composite_score": 84.3
  },
  "shopify_setup": {
    "structure": "fixed_bundle",
    "parent_sku": "BUNDLE-COFFEE-BREWING-001",
    "variant_skus": ["RS-POUR-OVER-001", "FILTER-100PK", "CARAFE-1L"],
    "recommended_apps": ["Shopify Bundles", "Fast Bundle", "Bold Bundles"],
    "inventory_strategy": "track_parent_only"
  },
  "tags": [],
  "occasion": null,
  "is_seasonal": false,
  "is_starter_kit": false,
  "is_active": true,
  "created_at": "2026-05-22T10:30:00Z",
  "last_updated": "2026-05-22T10:30:00Z",
  "created_by": "bundle-builder",
  "downstream_consumed_by": []
}
```

## Field semantics

### `recommended_tier`
The skill's recommendation; buyer can override. Used by downstream skills to know which pricing tier to apply.

### `discovery_evidence`
Why the bundle was suggested. Allows buyers to audit and downstream skills to surface reasoning.

### `tags`
Buyer-applied tags for filtering downstream:
- "evergreen" — permanent bundle
- "promo_q4_2026" — tied to a promotional window
- "test" — buyer is A/B testing
- "deprecated" — bundle no longer recommended

### `is_seasonal` + `occasion`
For gift-set bundles tied to occasions. Drives timing in skill #8 (Campaign Calendar Planner).

### `is_starter_kit`
Special-case flag. Skill #7 (Email Flow Architect) checks this when triggering first-time-customer flows.

### `is_active`
Buyer can deactivate bundles without deleting them. Inactive bundles don't surface in downstream skills until reactivated.

### `downstream_consumed_by`
Track record of which downstream skills have consumed this bundle:

```json
"downstream_consumed_by": [
  {"skill": "landing-page-copywriter", "consumed_at": "2026-05-23T11:00:00Z", "output_path": "..."},
  {"skill": "product-description-writer", "consumed_at": "2026-05-24T09:15:00Z", "output_path": "..."}
]
```

Helps the buyer see which bundles have been operationalized and which are still candidate-only.

## How downstream skills consume the cache

### Landing Page Copywriter (skill #3)

```python
from pathlib import Path
import json

def get_active_bundles(plugin_root):
    cache_dir = plugin_root / "~/.the-ecommerce-seller/cache" / "bundles"
    bundles = []
    for path in cache_dir.glob("*.json"):
        with path.open() as f:
            data = json.load(f)
        if data.get("is_active", True):
            bundles.append(data)
    return bundles
```

Used to:
- Generate dedicated bundle landing pages with hero, SKU breakdown, pricing, social proof, FAQ
- Apply the appropriate positioning variant per page type
- Pull testimonials referenced in the bundle

### Product Description Writer (skill #1)

Reads bundle cache when generating bundle PDPs. Uses:
- `skus_included` for the "What's included" section
- `pricing_tiers.recommended_tier` for the price + savings copy
- `positioning_copy.variants.benefit_led` for the main description (Shopify PDP context typically benefit-led)

### Ad Creative Generator (skill #5)

Reads bundle cache when generating ad concepts. Uses:
- `positioning_copy.ad_headlines` and `ad_primary_text` as starting drafts
- Adapts per ad platform (Meta vs. TikTok vs. Google)
- Generates 5 ad variants per bundle per platform

### Campaign Calendar Planner (skill #8)

Reads bundle cache to know which bundles to promote when:
- `is_seasonal: true` bundles promoted in their occasion windows
- `is_starter_kit: true` bundles promoted via acquisition campaigns
- AOV-Lift bundles promoted during free-shipping push periods

## Cache updates over time

The bundle cache evolves:

- **New bundles added**: each forecast run can suggest new bundles
- **Existing bundles updated**: re-running the engine on fresh data can update pricing, testimonials, or evidence
- **Bundles deactivated**: buyer marks a bundle as inactive; cache retains it for history
- **Bundles archived**: after N months of inactivity, the skill can archive to `~/.the-ecommerce-seller/cache/bundles/archive/`

The skill never auto-deletes bundles. The buyer can manually delete files from `~/.the-ecommerce-seller/cache/bundles/` to forget bundles.

## Bundle conflicts

When two bundles overlap > 70% in SKUs, the skill flags them as potentially redundant. Example:
- "Coffee Brewing Bundle A": Pour-over + Filters + Carafe
- "Coffee Brewing Bundle B": Pour-over + Filters + Grinder

These share 2/3 SKUs. The skill recommends:
- Keep both if they target different use-cases (Carafe = serving; Grinder = brewing prep)
- Consolidate into one 4-SKU bundle
- Choose between based on data signal strength

Buyer decides. The skill doesn't auto-resolve.

## Cache cleanup

The skill provides a CLI for bundle management:

```bash
python bundle_cache.py list                # list all cached bundles
python bundle_cache.py show <bundle-id>    # show full bundle
python bundle_cache.py deactivate <id>     # mark as inactive
python bundle_cache.py archive <id>        # archive (move to archive subdir)
python bundle_cache.py prune --age 180     # archive bundles inactive > 180 days
```

Helps the buyer manage the bundle library as the brand evolves.

## Versioning

The cache schema includes a version field for future migrations:

```json
"_schema_version": 1
```

Future versions of the skill can read older cache files and migrate fields if needed.

## Cross-skill data flow summary

```
[Sales CSV] + [Product catalog] + [Inventory cache] + [Testimonial cache]
        │
        ▼
[Skill #13 Bundle Builder runs all 3 discovery layers]
        │
        ▼
[Writes to ~/.the-ecommerce-seller/cache/bundles/{slug}.json per bundle]
        │
        ├──→ Skill #1 (PDW) reads for bundle PDPs
        ├──→ Skill #3 (LPC) reads for bundle landing pages
        ├──→ Skill #5 (ACG) reads for bundle ad concepts
        └──→ Skill #8 (CCP) reads for promotional scheduling
```

The bundle cache becomes the central registry of the brand's bundle strategy. Downstream skills don't need to be told about new bundles — they read the cache and act.
