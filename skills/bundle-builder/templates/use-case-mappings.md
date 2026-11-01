# Use-Case Mappings — Built-In Library

Pre-built use-case definitions the skill uses to discover complementary bundles. Buyers can override or extend in config.

## Coffee & Tea

### coffee_brewing_complete
- Required: pour_over_device, filters
- Optional: carafe, grinder, kettle, scale, beans
- Min 3, max 4 SKUs
- Bundle archetype: "Complete Brewing Set"

### tea_setup
- Required: teapot, tea_loose_leaf
- Optional: tea_infuser, mug, kettle, tea_storage
- Min 3, max 4
- Bundle archetype: "Tea Ritual Set"

### morning_caffeine_starter
- Required: coffee_or_tea, mug
- Optional: spoon, sweetener, milk_frother
- Min 2, max 4
- Bundle archetype: "Morning Drinks Starter"

## Personal Care

### skincare_routine_am
- Required: cleanser, moisturizer
- Optional: toner, serum, spf, eye_cream
- Min 3, max 5
- Bundle archetype: "Morning Skincare Routine"

### skincare_routine_pm
- Required: cleanser, moisturizer
- Optional: toner, retinol, serum, eye_cream, sleeping_mask
- Min 3, max 5
- Bundle archetype: "Evening Skincare Routine"

### body_care
- Required: body_wash, body_lotion
- Optional: body_scrub, body_oil, hand_cream
- Min 2, max 4
- Bundle archetype: "Body Care Trio"

### hair_care_routine
- Required: shampoo, conditioner
- Optional: hair_oil, hair_mask, leave_in
- Min 2, max 4
- Bundle archetype: "Hair Care Routine"

## Home & Living

### candle_ritual
- Required: candle
- Optional: wick_trimmer, snuffer, matches, candle_tray
- Min 2, max 3
- Bundle archetype: "Candle Care Set"

### bath_self_care
- Required: bath_salt_or_bubble
- Optional: body_oil, eye_mask, candle, robe
- Min 2, max 4
- Bundle archetype: "Bath Ritual Set"

### bedroom_essentials
- Required: pillowcase_or_sheet
- Optional: throw, eye_mask, lavender_spray, sleep_drops
- Min 2, max 4
- Bundle archetype: "Bedroom Comfort Set"

### kitchen_essentials
- Required: kitchen_towel_or_apron
- Optional: oven_mitt, dish_soap, kitchen_brush, candle
- Min 2, max 4
- Bundle archetype: "Kitchen Essentials"

### dining_table
- Required: napkin_or_placemat
- Optional: candle_holder, vase, table_runner, coasters
- Min 2, max 4
- Bundle archetype: "Table Setting Trio"

## Workspace

### desk_setup_basic
- Required: notebook, pen
- Optional: pencil_set, sharpener, desk_pad
- Min 2, max 4
- Bundle archetype: "Desk Set"

### desk_setup_mobile
- Required: keyboard, mouse
- Optional: cable_organizer, laptop_stand, mouse_pad
- Min 2, max 4
- Bundle archetype: "Mobile Workspace"

### stationery_starter
- Required: notebook
- Optional: pen, pencil_set, eraser, ruler, washi_tape
- Min 3, max 5
- Bundle archetype: "Stationery Starter"

## Wellness

### wellness_supplement_starter
- Required: daily_vitamin
- Optional: omega_3, magnesium, probiotic, multi
- Min 2, max 4
- Bundle archetype: "Daily Wellness Set"

### sleep_set
- Required: sleep_aid_supplement
- Optional: eye_mask, lavender_spray, sleep_tea, journal
- Min 2, max 4
- Bundle archetype: "Better Sleep Set"

### yoga_meditation
- Required: yoga_mat
- Optional: meditation_cushion, journal, candle, palo_santo
- Min 2, max 4
- Bundle archetype: "Mindfulness Set"

## Food & Drink

### cocktail_home_bar
- Required: shaker, jigger
- Optional: strainer, bar_spoon, glasses, bitters
- Min 3, max 5
- Bundle archetype: "Home Bar Kit"

### baking_essentials
- Required: rolling_pin_or_baking_dish
- Optional: measuring_cups, mixing_bowls, spatula, parchment
- Min 3, max 5
- Bundle archetype: "Baking Essentials"

### grilling_set
- Required: grill_tongs_or_spatula
- Optional: grill_brush, marinade_brush, rub_or_seasoning
- Min 2, max 4
- Bundle archetype: "Grill Master Set"

## Outdoor

### camping_essentials
- Required: tent_or_shelter, sleeping_bag_or_pad
- Optional: headlamp, cooking_setup, water_filter
- Min 3, max 5
- Bundle archetype: "Camping Starter"

### picnic_set
- Required: picnic_blanket
- Optional: thermos, picnic_basket, napkins, cutlery_set
- Min 2, max 4
- Bundle archetype: "Picnic Day Set"

### gardening_starter
- Required: gardening_gloves, tool_set
- Optional: seeds, planters, watering_can
- Min 2, max 4
- Bundle archetype: "Garden Starter"

## Apparel & Accessories

### athleisure_outfit
- Required: top, bottom
- Optional: socks, headband, water_bottle
- Min 2, max 4
- Bundle archetype: "Athleisure Set"

### travel_essentials
- Required: tote_or_weekender, packing_cube
- Optional: travel_pouch, eye_mask, water_bottle
- Min 2, max 4
- Bundle archetype: "Travel Essentials"

### loungewear_set
- Required: top_lounge, bottom_lounge
- Optional: socks_lounge, robe, eye_mask
- Min 2, max 4
- Bundle archetype: "Loungewear Set"

## Gift-Specific

### mothers_day_curated
- Required: 2+ categories popular as Mother's Day gifts
- Preferred combos: candle + tea + spa-like_item, jewelry + skincare, journal + tea + soft_textile
- Min 2, max 4
- Tags: occasion=mothers_day, premium_presentation

### holiday_curated
- Required: 2+ categories from holiday-popular items
- Preferred: candle + chocolate + holiday_decoration, sweater + scarf + gloves
- Min 2, max 4
- Tags: occasion=holiday, seasonal_only

## Customization

The buyer can extend these in config:

```json
"custom_use_cases": [
  {
    "name": "tomato_garden_pack",
    "label": "Tomato Garden Pack",
    "required_categories": ["seeds_tomato", "soil_amendment"],
    "optional_categories": ["stake", "fertilizer_organic", "watering_can"],
    "min_skus": 2,
    "max_skus": 4,
    "tags": ["seasonal_only", "occasion=spring"]
  }
]
```

## Use-case tagging

Each use-case can carry tags that affect downstream behavior:

- `seasonal_only` — bundle only surfaces in season; archived out of season
- `occasion=X` — bundle tied to specific occasion; informs timing
- `premium_presentation` — bundle expects gift wrap / special packaging
- `subscription_friendly` — bundle works as a subscription
- `consumable_refill_pair` — bundle pairs durable + consumable for repeat orders

The bundle cache propagates these tags to downstream skills so they can position accordingly.

## When to add a new use-case

Add a new use-case when:
- Three or more catalog SKUs naturally combine in a way no existing use-case captures
- Customer feedback or search queries reveal a use-case the brand hadn't articulated
- A new product category enters the brand

Don't add a use-case for one-off seasonal promotions — those work better as ad-hoc Gift Set bundles.
