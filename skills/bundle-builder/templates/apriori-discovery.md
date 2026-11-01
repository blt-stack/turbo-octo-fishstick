# Apriori Market Basket Mining

The data-driven layer of bundle discovery. Mines actual customer purchase patterns to find SKUs that co-occur in orders more often than chance.

## The three metrics

For an item pair (A, B):

| Metric | Formula | Interpretation |
|---|---|---|
| **Support** | P(A ∩ B) = orders_with_both / total_orders | How common is this pair? Baseline filter. |
| **Confidence** | P(B \| A) = orders_with_both / orders_with_A | Of A-buyers, what % also bought B? Direction-dependent. |
| **Lift** | P(A ∩ B) / (P(A) × P(B)) | How much more likely than chance? > 1.0 = real association. |

## The Apriori algorithm in plain English

1. Build all orders as baskets — `{SKU_a, SKU_b, ...}` per order
2. Count single SKU frequencies → keep SKUs with support ≥ min_support
3. Generate pairs from frequent SKUs → keep pairs with support ≥ min_support
4. Generate triples from frequent pairs → keep triples with support ≥ min_support
5. ...continue to higher-order item sets until no more frequent sets exist
6. For each frequent set, compute confidence + lift
7. Filter by min_confidence and min_lift

## Threshold defaults

The skill ships with these defaults (buyer can override):

```json
"bundle_builder": {
  "apriori": {
    "min_support": 0.01,
    "min_confidence": 0.25,
    "min_lift": 2.0,
    "max_basket_size": 6
  }
}
```

### Adjusting for brand size

| Monthly orders | min_support | min_confidence | min_lift |
|---|---|---|---|
| < 100 | 0.03 | 0.30 | 1.7 |
| 100-500 | 0.02 | 0.30 | 1.8 |
| 500-2000 | 0.01 | 0.25 | 2.0 |
| 2000-10000 | 0.005 | 0.20 | 2.5 |
| > 10000 | 0.002 | 0.15 | 3.0 |

The skill auto-detects monthly volume from the input data and tunes thresholds. Buyer can override.

## Sample size warning

When fewer than 50 orders contain a candidate pair, the lift estimate is noisy. The skill flags these candidates as "low-sample" in the discovery audit. Bundles built on low-sample data should be re-validated as more orders accumulate.

## Implementation notes

Python implementation in `scripts/copurchase_analyzer.py`:

```python
def apriori_pairs(baskets: list[set[str]], min_support: float, min_confidence: float, min_lift: float):
    # Count item frequencies
    item_counts = Counter()
    for basket in baskets:
        for sku in basket:
            item_counts[sku] += 1
    total = len(baskets)

    # Filter to frequent items
    frequent_items = {sku for sku, c in item_counts.items() if c / total >= min_support}

    # Generate pair counts
    pair_counts = Counter()
    for basket in baskets:
        filtered = basket & frequent_items
        for pair in combinations(sorted(filtered), 2):
            pair_counts[pair] += 1

    # Score each pair
    results = []
    for (a, b), c in pair_counts.items():
        support = c / total
        if support < min_support:
            continue
        confidence_ab = c / item_counts[a]
        confidence_ba = c / item_counts[b]
        lift = support / ((item_counts[a] / total) * (item_counts[b] / total))
        if max(confidence_ab, confidence_ba) >= min_confidence and lift >= min_lift:
            results.append({
                "sku_a": a, "sku_b": b,
                "support": support,
                "confidence_ab": confidence_ab,
                "confidence_ba": confidence_ba,
                "lift": lift,
                "co_occurrence_count": c
            })
    return sorted(results, key=lambda x: x["lift"], reverse=True)
```

For triples and quadruples, the algorithm extends naturally. The skill caps at quadruples (4-SKU bundles); higher-order sets are rare in practice and computationally expensive.

## Time complexity

Apriori is O(2^N) in the worst case where N = number of unique SKUs. For typical e-commerce catalogs:

- 50 SKUs, 500 orders: < 1 second
- 200 SKUs, 2000 orders: 2-5 seconds
- 500 SKUs, 10000 orders: 10-30 seconds

For larger catalogs, the skill applies pruning aggressively (only generates higher-order sets from pairs above 2× the threshold).

## Common patterns that emerge

In practice, Apriori surfaces a few patterns repeatedly:

### Hero + Accessory pairs (most common)
Hero SKU (high volume) + accessory SKU (lower volume, high attach rate)
- Confidence: high in one direction (accessory → hero), lower in reverse
- Lift: 2-4×
- Bundle action: easy FBT bundle

### Consumable refill pairs
Consumable that runs out + refill SKU
- Confidence: high (people buy the refill once they know about it)
- Lift: 3-6× (very specific co-occurrence)
- Bundle action: subscription bundle, multi-pack bundle

### Use-case completion pairs
Two SKUs that solve a use case together
- Confidence: moderate (both directions similar)
- Lift: 2-3×
- Bundle action: complementary category bundle

### Coincidence pairs (NOT real bundles)
Two popular SKUs that co-occur because they're both popular
- Confidence: moderate
- Lift: barely above 1.0 (this is the giveaway)
- Bundle action: skip — the lift filter catches these

The lift filter (≥ 2.0 by default) is the single most important threshold for avoiding coincidence pairs.

## Symmetric vs. asymmetric pairs

Apriori finds the pair {A, B} — the same set whether you bought A then B or B then A. But the *confidence* differs by direction:

- confidence(A→B) = P(B | A)
- confidence(B→A) = P(A | B)

These can be very different. Example:
- 90% of filter buyers also bought the pour-over (P(pour-over | filter) = 0.90)
- 8% of pour-over buyers also bought filters at the same time (P(filter | pour-over) = 0.08)

This asymmetry tells you the bundle's "direction" — filters lead to pour-over, but pour-over doesn't lead to filters as strongly. For bundle positioning, both directions matter.

The skill shows max(confidence_ab, confidence_ba) in summary output but logs both directions for the buyer to review.

## Filtering out promo artifacts

Some Apriori pairs are artifacts of past promotions ("Buy A and B together for $X"). To avoid surfacing these:

- The skill checks promotional history (if Shopify export includes discount codes per order)
- Pairs with > 60% of co-occurrence orders involving a discount code get flagged as "promo-driven"
- Buyer can review and exclude these from bundle suggestions

Otherwise, the skill might recommend a bundle that already exists because of a prior promo, missing the actual organic patterns.

## Multi-variant SKUs

When a "product" has multiple SKU variants (e.g., size or color), Apriori has two modes:

1. **Strict mode** (default): each variant SKU is independent — variants are different items
2. **Aggregated mode** (opt-in): variants roll up to parent product for Apriori; final bundle picks the most-popular variant

Strict mode is more accurate but produces noisier results for catalogs with many variants. The skill defaults to strict but recommends aggregated for catalogs with >20 variants per product.

## Apriori output flows into

The Apriori results feed into:
- **type-fbt.md**: highest-lift, well-supported pairs → FBT bundles
- **type-aov-lift.md**: data-validated SKU attach rates → AOV-Lift bundles
- **type-complementary.md**: data confirms (or contradicts) categorical hypotheses → strengthens complementary bundles

The bundle engine uses Apriori as the strongest signal when sample size is sufficient, and falls back to categorical mappings when data is sparse.
