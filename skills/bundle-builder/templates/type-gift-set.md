# Bundle Type: Gift Set

Bundles curated for gifting occasions. Different from FBT and Complementary bundles because:
- The buyer (gifter) is not the user (recipient) — positioning addresses both
- Occasion timing matters (seasonal peaks around Mother's Day, holidays, etc.)
- Presentation matters (packaging, gift-wrapping, gift notes)
- Pricing perception is different (gifters compare to "I-spent-$X-on-them" not "I-got-a-deal")

## Source layer

Categorical complementarity + occasion mapping. See `categorical-mapping.md`.

## Filter thresholds

A gift bundle qualifies when:
- Bundle is from cross-category combinations (single-category items rarely make great gifts)
- Bundle includes 2-4 SKUs
- Bundle price range fits the occasion's typical spend ($30-100 for casual occasions, $50-150 for major gifts)
- SKUs are giftable (consumable, presentable, photogenic — skill checks brand-level taxonomy)
- At least one SKU has healthy stock + velocity

## Occasion mapping

The skill ships with pre-built occasion mappings. Buyer can override or add custom ones:

| Occasion | Typical spend | Timing window | Audience |
|---|---|---|---|
| Mother's Day | $40-100 | Mid-April to early May | Adult children gifting parents |
| Father's Day | $40-100 | Late May to mid-June | Adult children gifting parents |
| Valentine's Day | $30-150 | Late January to Feb 13 | Romantic partners |
| Christmas | $30-200 | Early November to Dec 22 | Friends + family wide |
| Hanukkah | $30-200 | Mid-November to mid-Dec | Friends + family |
| Birthday | $30-100 | Year-round | Various |
| Housewarming | $30-75 | Year-round | Friends gifting new homes |
| Wedding | $50-200 | Year-round | Wedding guest |
| Thank You | $20-50 | Year-round | Various |
| Self-Care Sunday | $30-80 | Year-round (treat-yourself) | Self-gifting |
| New Baby | $30-100 | Year-round | Friends/family of new parents |
| Graduation | $30-100 | May-June | Family of graduates |

The skill flags when current date is within 4-8 weeks of an occasion peak as "imminent — promote now."

## Bundle structure

Gift bundles aim for 2-3 SKUs across distinct categories. Common patterns:

### "Indulgence" trio (consumable + accessory + extra)
- Hero consumable (candle, chocolate, tea, skincare)
- Companion accessory (cup, holder, tray)
- Small extra (chocolate, sample, card)

### "Routine" set
- Multiple SKUs supporting a self-care ritual (skincare AM kit, evening tea set, morning coffee set)

### "Discovery" sampler
- Multiple smaller SKUs from a product line, allowing the recipient to explore

### "Project" kit
- Items for a hobby or activity (gardening starter, knitting starter)

## Pricing strategy

Gift bundles use **Conservative tier (5-10% off)**. Why:
- Gifters don't reward themselves for finding a deal as much as for finding a good gift
- A 5-10% discount feels like a small reward; 20-25% off can signal "trying too hard" or "the brand wants the inventory cleared"
- Gift-wrapping and presentation are part of the value — the bundle should feel premium

Exceptions:
- Holiday season gift sets (especially Q4 promotional periods): standard tier (12-18%) is acceptable since the comparison set includes other discounted holiday gift options
- Post-occasion clearance: aggressive tier (20-25%) to move remaining inventory

## Positioning angle

Gift bundles position as **thoughtful**:
> "A complete gift, beautifully packaged."
> "For the [recipient role] who loves [thing]."
> "Easy to give. Easy to love."

Mention recipient archetype explicitly: "for the early-morning gym person," "for the home-cook," "for the person who can't get enough candles."

Avoid:
- "Save $X" leading the copy (gifters care less about savings than fit)
- Generic "perfect gift" language (specific is better)
- Pricing comparisons ("retail $XX, you pay $YY") in early copy (mention later)

## Presentation considerations

Gift bundles imply gift-presentation. The skill recommends:
- **Gift box / wrap option** at checkout (separate paid add-on, optional)
- **Gift note** option at checkout
- **Direct ship to recipient** option (different shipping address than buyer)
- **Schedule delivery** option (deliver on a specific date, not as soon as possible)

These are Shopify checkout configurations, not bundle-builder concerns directly, but the bundle's success depends on them being available.

## Why these bundles work

Gift-buying is an under-served e-commerce category for solo brands. Customers:
1. Want to give a thoughtful gift but don't know the brand well enough to pick the right item
2. Are time-pressured (especially around occasions)
3. Want assurance that the curation is good

A gift bundle solves all three. The buyer pays a small premium for the curation, presentation, and reduced decision fatigue.

## Example Gift Sets

### Mother's Day "Slow Morning"
```
- Organic Tea Sampler        $24
- Hand-thrown Mug           $36
- Lavender Hand Cream        $18

Individual total: $78
Bundle (8% off): $72
Savings: $6 + free gift wrap

Audience: adult children gifting moms who appreciate slow rituals
Spend tier: $72 (fits $40-100 Mother's Day range)
Imminent: yes (today is April 20; Mother's Day in 18 days)
```

### Father's Day "Workshop Essentials"
```
- Leather-bound Notebook    $32
- Premium Pencil 4-Pack     $14
- Brass Sharpener           $18

Individual total: $64
Bundle (10% off): $58
Savings: $6 + free gift wrap

Audience: family members gifting dads who appreciate analog tools
Spend tier: $58 (fits $40-100 Father's Day range)
```

### Birthday "Home Bar Starter"
```
- Cocktail Shaker             $42
- Jigger                      $14
- Bitters 2-Pack              $24

Individual total: $80
Bundle (8% off): $74
```

### Wedding "Housewarming"
```
- Glass Carafe                $32
- Tea Towel Set (2)           $28
- Hand Soap + Lotion duo      $32

Individual total: $92
Bundle (5% off — conservative): $87
```

### Self-Care Sunday
```
- Bath Salt                  $18
- Eye Mask                   $14
- Lavender Spray             $16

Individual total: $48
Bundle (10% off): $43
Audience: self-gifters
```

## When gift bundles fail

- **Not actually gift-appropriate**: items don't present well, recipient doesn't see "gift" feeling
- **Wrong audience read**: bundle aimed at one recipient but copy describes another
- **Underpriced for the occasion**: $28 Mother's Day gift feels cheap; needs to clear ~$40
- **No gift-wrap infrastructure**: bundle suggests "give as a gift" but Shopify checkout doesn't offer gift packaging
- **Timing miss**: holiday gift bundles surfaced in February have no urgency

## Recurring vs. one-time gift bundles

The skill distinguishes:
- **Always-on gifts** (birthday, housewarming, thank-you) — permanent collection
- **Seasonal gifts** (Mother's Day, holidays) — promoted in window, archived after

The bundle cache tags each bundle with `is_seasonal: true/false` and `occasion_window_dates: [start, end]` so downstream skills (Campaign Calendar Planner, Ad Creative Generator) can time promotions correctly.

## Buyer-configurable

```json
"bundle_builder": {
  "gift_set_min_price_usd": 30,
  "gift_set_max_price_usd": 150,
  "active_occasions": ["mothers_day", "fathers_day", "christmas", "birthday", "housewarming"],
  "default_gift_wrap_available": true,
  "custom_occasions": []
}
```
