# Categorical Mapping

The non-data layer of bundle discovery. Maps SKUs to categories, then maps category combinations to bundle use-cases. Useful when sales data is sparse or when discovery should be opinionated (not purely data-driven).

## Two-level mapping

### Level 1: SKU → Category

Each SKU maps to one or more categories. Sources of category mapping:

1. **Shopify product type field** (most common; buyer-set during product creation)
2. **Shopify collections** (one SKU may be in multiple collections)
3. **Skill auto-classification** (when explicit categories are missing — keyword inference from product names)
4. **Buyer manual mapping** (in config.bundle_builder.sku_to_category overrides)

### Level 2: Category combinations → Use-case

The skill ships with a use-case library mapping category combinations to bundle archetypes. See `use-case-mappings.md`.

Example mapping fragment:

```python
USE_CASES = {
    "coffee_brewing_complete": {
        "required_categories": ["pour_over_device", "filters"],
        "optional_categories": ["carafe", "grinder", "kettle", "scale", "beans"],
        "min_skus": 3,
        "max_skus": 4,
        "preferred_combos": [
            ["pour_over_device", "filters", "carafe"],
            ["pour_over_device", "filters", "grinder"],
            ["pour_over_device", "kettle", "beans"]
        ]
    },
    "skincare_routine_am": {
        "required_categories": ["cleanser", "moisturizer"],
        "optional_categories": ["toner", "serum", "spf", "eye_cream"],
        "min_skus": 3,
        "max_skus": 5,
        "preferred_combos": [
            ["cleanser", "serum", "moisturizer_spf"],
            ["cleanser", "toner", "moisturizer"]
        ]
    },
    ...
}
```

## Auto-classification for SKUs without category

When a SKU has no category, the skill infers from product name + description using keyword patterns:

```python
KEYWORD_TO_CATEGORY = {
    "pour-over": "pour_over_device",
    "pour over": "pour_over_device",
    "filter": "filters",
    "filters": "filters",
    "carafe": "carafe",
    "grinder": "grinder",
    "kettle": "kettle",
    "cleanser": "cleanser",
    "moisturizer": "moisturizer",
    "moisturiser": "moisturizer",
    "serum": "serum",
    "toner": "toner",
    "spf": "spf",
    "sunscreen": "spf",
    ...
}
```

The skill scores each keyword match and picks the highest-confidence category. Below the confidence threshold, the SKU stays uncategorized and the skill flags it for buyer mapping.

## Custom use-cases

Buyers can add custom use-cases to `config.bundle_builder.custom_use_cases`:

```json
"custom_use_cases": [
  {
    "name": "morning_ritual",
    "label": "Morning Ritual",
    "required_categories": ["candle", "journal"],
    "optional_categories": ["tea", "pen", "incense"],
    "min_skus": 2,
    "max_skus": 4
  }
]
```

The skill respects custom use-cases and surfaces bundles that match.

## Category overlap (a SKU in multiple use-cases)

A SKU can belong to multiple use-cases. For example, a "ceramic mug" might fit:
- `coffee_brewing` (as serving vessel)
- `gift_set_housewarming` (as gift item)
- `tea_setup` (cross-category, also useful)

The skill considers all use-cases the SKU fits. When ranking bundles, the same SKU appearing in multiple bundles is fine — it's just well-suited.

## Cross-use-case bundles

Some bundles span multiple use-cases. Example: "Slow Morning Set" might combine:
- Coffee brewing
- Stationery (journal, pen)
- Aromatherapy (candle)

These cross-use-case bundles get tagged as `cross_use_case: true` and require manual buyer review since they're more inferential than single-use-case bundles.

## Category preferences per brand

Some brands sell heavily in one category and lightly in others. The skill detects category dominance:

- Dominant category > 50% of revenue
- Secondary categories < 20% each

For these brands, categorical bundles often combine dominant category items with secondary category items as "stretch" bundles to explore upsell opportunities.

For balanced brands (no dominant category), the skill suggests bundles across many combinations.

## Mapping confidence audit

The skill outputs a category mapping audit in the .xlsx Sheet 5 (Discovery Audit):

| SKU | Mapped Category | Mapping Source | Confidence |
|---|---|---|---|
| RS-POUR-OVER-001 | pour_over_device | shopify_product_type | 1.0 |
| FILTER-100PK | filters | keyword_inference | 0.95 |
| MYSTERY-SKU-X | uncategorized | none | 0.0 — buyer review |
| CLEANSER-GENTLE | cleanser | buyer_override | 1.0 |
| LIP-BALM-001 | spf | keyword_inference | 0.4 — low |

Low-confidence mappings get flagged. Buyer can confirm or remap before re-running bundle discovery.

## When categorical mapping fails

- **Generic catalog with poor categorization**: every product is "miscellaneous" → use-cases can't match
- **Highly specialized catalog**: brand's products don't fit standard use-case patterns → skill defaults to FBT-only mode
- **One-category brand**: brand only sells in one category → cross-category bundles aren't possible; skill switches to within-category bundling (e.g., size combinations, color combinations)

The skill recommends a config-level workflow:
1. First forecast run: skill maps SKUs to categories using available sources
2. Buyer reviews the mapping audit and corrects low-confidence mappings
3. Subsequent runs use the corrected mappings, surfacing better bundles

## Multilingual / regional category mapping

The skill's default categories are English-language. For brands selling internationally:
- SKUs with names in other languages may not match the keyword inference
- Buyer can extend `config.bundle_builder.keyword_to_category` with their own language keywords
- The skill respects category mappings regardless of language (e.g., a SKU named in French can still map to `pour_over_device`)

## Cross-skill integration

The categorical mapping is shared with:
- **Skill #2 (Listing SEO Optimizer)**: uses categories to inform keyword research
- **Skill #1 (Product Description Writer)**: uses categories to pick appropriate templates
- **Skill #3 (Landing Page Copywriter)**: uses categories for collection page architecture

If the buyer has used those skills, the category mapping may already exist; the bundle builder reads it from the shared config rather than re-inferring.
