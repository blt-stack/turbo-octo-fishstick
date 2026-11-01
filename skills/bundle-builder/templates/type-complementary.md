# Bundle Type: Complementary Category

Bundles formed from cross-category combinations that fit a shared use-case. Useful when:
- Brand has new SKUs that haven't accumulated co-purchase history yet
- Brand has products across distinct categories that solve a shared problem
- Co-purchase data exists but is noisy / small-sample

These bundles are **inferred from product structure**, not from customer behavior.

## Source layer

Categorical complementarity. See `categorical-mapping.md` for the use-case map.

## Filter thresholds

A complementary bundle qualifies when:
- All SKUs map to categories in the same use-case
- The use-case has ≥3 categories with products in the brand catalog
- The bundle includes 2-4 SKUs (more becomes unwieldy)
- At least one SKU has healthy stock + velocity (read from skill #12)

## Use-case categories (examples)

The skill ships with a pre-built use-case map in `use-case-mappings.md`. Examples:

### Coffee Brewing
- pour_over_device
- filters
- carafe
- grinder
- kettle
- coffee_beans
- accessories (trivet, scoop, scale)

A complementary "Coffee Brewing" bundle includes 3-4 items across these categories.

### Skincare Routine (AM)
- cleanser
- toner
- serum
- moisturizer
- spf

### Desk Setup
- keyboard
- mouse
- monitor_arm
- cable_organizer
- desk_pad
- lamp

### Camping Kit
- tent / shelter
- sleeping_pad
- sleeping_bag
- cooking_setup
- water_filtration
- light

### Home Bar
- shaker
- jigger
- strainer
- glasses
- bar_spoon
- garnish_set

### Gift Categories (separate from use-cases)
- birthday_gift_for_him
- birthday_gift_for_her
- housewarming
- thank_you
- new_baby
- wedding

## Bundle structure

Complementary bundles aim for **3 SKUs** as the sweet spot:
- 2 SKUs feels like a small upsell, not a curated set
- 3 SKUs reads as "complete solution"
- 4+ feels like a kit or a project; reserve for Gift Sets and Starter Kits

The skill prefers including:
- 1 hero/anchor SKU from the dominant category
- 1-2 complementary SKUs from supporting categories

Avoid:
- All anchor SKUs from the same category (no diversity)
- Random cross-category pairs without shared use-case (just because two products are different categories doesn't mean they belong together)

## Pricing strategy

Complementary bundles typically use **Standard tier (12-18% off)** but can go conservative (5-10%) when:
- Bundle exists primarily for discovery / education (customer didn't know these go together)
- Brand wants the bundle to anchor a landing page without competing with single-product margins

## Positioning angle

Complementary bundles position as **completeness**:
> "Everything you need for [use-case]"
> "A complete [use-case] set"
> "Three pieces that work together"

The copy emphasizes the *solution*, not the products.

## Why these bundles work

Customers often don't know which combinations make sense in an unfamiliar category. A complementary bundle:
1. **Reduces decision fatigue** — buyer doesn't have to research the right pairing
2. **Signals expertise** — brand demonstrates curation knowledge
3. **Onboards new customers** — high-touch entry point for unfamiliar use-cases

For brands selling into specialized categories (coffee, skincare, home goods), complementary bundles are often the most-converting bundle type.

## Example Complementary bundles

### Pour-Over Brewing Set
```
SKUs:
- River Stone Pour-Over (pour_over_device)
- Burr Grinder (grinder)
- Gooseneck Kettle (kettle)

Use-case: coffee_brewing
Individual total: $144
Bundle (15% off): $122
Savings: $22
```

### AM Skincare Routine
```
SKUs:
- Gentle Cleanser (cleanser)
- Vitamin C Serum (serum)
- Daily Moisturizer SPF 30 (moisturizer + spf)

Use-case: skincare_routine_am
Individual total: $98
Bundle (12% off): $86
Savings: $12
```

### Mobile Desk Setup
```
SKUs:
- Travel Keyboard (keyboard)
- Compact Mouse (mouse)
- Cable Organizer (cable_organizer)

Use-case: desk_setup_mobile
Individual total: $185
Bundle (10% off — conservative since SKUs are premium) : $166
Savings: $19
```

## When complementary bundles fail

- **Bundle is too obvious / unhelpful**: the customer already knew these go together (Sneakers + Socks isn't a complementary bundle; it's FBT)
- **Use-case is fictional**: the buyer thinks the items go together but customers don't see it the same way
- **One SKU dominates value**: 80% of the bundle's value is one item; the others feel like padding
- **Discount feels manufactured**: customers can see the items are barely-discounted and not actually complementary

The skill flags these patterns in the discovery audit.

## Buyer override

The buyer can:
- Define custom use-cases in `config.bundle_builder.custom_use_cases`
- Disable specific use-cases for their brand
- Force certain SKUs to map to certain categories
- Set per-category bundle preferences (e.g., "always include filters in coffee-brewing bundles")

These overrides live in the config and persist across forecast runs.
