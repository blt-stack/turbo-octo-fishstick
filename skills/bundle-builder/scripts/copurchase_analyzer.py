"""
Apriori-style market basket analysis.

Computes support, confidence, and lift for SKU pairs (and optionally triples)
from sales order baskets.

Usage:
    from copurchase_analyzer import build_baskets, apriori_pairs, apriori_triples

    baskets = build_baskets(canonical_sales_rows)  # canonical from sales_csv_parser
    pairs = apriori_pairs(baskets, min_support=0.01, min_confidence=0.25, min_lift=2.0)
    triples = apriori_triples(baskets, min_support=0.005, min_confidence=0.20, min_lift=2.5)

Pure stdlib — no numpy/pandas dependency.
"""

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations


def build_baskets(canonical_rows: list[dict], order_key: str = "order_id") -> list[set[str]]:
    """
    Convert canonical sales rows into baskets (sets of SKUs per order).

    If order_id is not present in rows, falls back to grouping by (date, customer_email)
    if customer_email is present; otherwise treats each row as its own basket.
    """
    if not canonical_rows:
        return []

    # Determine grouping key
    sample = canonical_rows[0]
    if order_key in sample:
        key_fn = lambda r: r[order_key]
    elif "order_id" in sample:
        key_fn = lambda r: r["order_id"]
    elif "customer_email" in sample and "date" in sample:
        key_fn = lambda r: (r.get("customer_email", ""), r.get("date", ""))
    elif "date" in sample:
        # Last-resort: group by date (treats all sales on same day as one basket — coarse but better than nothing)
        key_fn = lambda r: r["date"]
    else:
        return [{r.get("sku", "")} for r in canonical_rows if r.get("sku")]

    grouped: dict = defaultdict(set)
    for row in canonical_rows:
        sku = row.get("sku")
        if not sku:
            continue
        grouped[key_fn(row)].add(sku)

    # Remove single-SKU baskets (can't co-occur with anything)
    baskets = [b for b in grouped.values() if len(b) >= 2]
    return baskets


def apriori_pairs(
    baskets: list[set[str]],
    min_support: float = 0.01,
    min_confidence: float = 0.25,
    min_lift: float = 2.0,
) -> list[dict]:
    """
    Returns a list of pair dicts that pass all three thresholds.
    Each dict has: sku_a, sku_b, support, confidence_ab, confidence_ba, lift, co_occurrence_count.
    """
    if not baskets:
        return []

    total = len(baskets)

    # Item frequencies
    item_counts: Counter = Counter()
    for basket in baskets:
        for sku in basket:
            item_counts[sku] += 1

    # Pre-filter to frequent items (support filter)
    frequent_items = {sku for sku, c in item_counts.items() if c / total >= min_support}

    # Pair counts
    pair_counts: Counter = Counter()
    for basket in baskets:
        filtered = sorted(basket & frequent_items)
        for pair in combinations(filtered, 2):
            pair_counts[pair] += 1

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
                "sku_a": a,
                "sku_b": b,
                "skus": [a, b],
                "support": round(support, 4),
                "confidence_ab": round(confidence_ab, 3),
                "confidence_ba": round(confidence_ba, 3),
                "confidence_max": round(max(confidence_ab, confidence_ba), 3),
                "lift": round(lift, 3),
                "co_occurrence_count": c,
                "basket_total": total,
                "order": 2,
            })

    return sorted(results, key=lambda x: (x["lift"], x["support"]), reverse=True)


def apriori_triples(
    baskets: list[set[str]],
    min_support: float = 0.005,
    min_confidence: float = 0.20,
    min_lift: float = 2.5,
) -> list[dict]:
    """
    Returns frequent 3-item sets (triples). Same threshold semantics.
    """
    if not baskets:
        return []

    total = len(baskets)

    # First get frequent pairs (to prune the triple search)
    pairs = apriori_pairs(baskets, min_support=min_support, min_confidence=0.05, min_lift=1.0)
    frequent_pair_skus = set()
    for p in pairs:
        frequent_pair_skus.add(p["sku_a"])
        frequent_pair_skus.add(p["sku_b"])

    # Count triples (only among SKUs that appear in at least one frequent pair)
    triple_counts: Counter = Counter()
    for basket in baskets:
        filtered = sorted(basket & frequent_pair_skus)
        for triple in combinations(filtered, 3):
            triple_counts[triple] += 1

    item_counts: Counter = Counter()
    for basket in baskets:
        for sku in basket:
            item_counts[sku] += 1

    results = []
    for triple, c in triple_counts.items():
        support = c / total
        if support < min_support:
            continue
        a, b, c_sku = triple
        # Confidence: P(triple) / P(any 2 of the triple)
        # We'll use the max single-item-driven confidence as a proxy
        confidences = []
        for sku in triple:
            confidences.append(c / item_counts[sku] if item_counts[sku] > 0 else 0)
        confidence_max = max(confidences)
        # Lift = P(triple) / (P(a) × P(b) × P(c))
        product = (item_counts[a] / total) * (item_counts[b] / total) * (item_counts[c_sku] / total)
        lift = support / product if product > 0 else 0
        if confidence_max >= min_confidence and lift >= min_lift:
            results.append({
                "skus": list(triple),
                "support": round(support, 4),
                "confidence_max": round(confidence_max, 3),
                "lift": round(lift, 3),
                "co_occurrence_count": c,
                "basket_total": total,
                "order": 3,
            })

    return sorted(results, key=lambda x: (x["lift"], x["support"]), reverse=True)


def auto_tune_thresholds(num_baskets: int) -> dict:
    """Return suggested thresholds based on basket count."""
    if num_baskets < 100:
        return {"min_support": 0.03, "min_confidence": 0.30, "min_lift": 1.7}
    elif num_baskets < 500:
        return {"min_support": 0.02, "min_confidence": 0.30, "min_lift": 1.8}
    elif num_baskets < 2000:
        return {"min_support": 0.01, "min_confidence": 0.25, "min_lift": 2.0}
    elif num_baskets < 10000:
        return {"min_support": 0.005, "min_confidence": 0.20, "min_lift": 2.5}
    else:
        return {"min_support": 0.002, "min_confidence": 0.15, "min_lift": 3.0}


if __name__ == "__main__":
    # Smoke test: synthesize baskets and run apriori
    import random
    random.seed(42)
    # Create 500 baskets simulating a coffee brand
    POOL_HERO = ["RS-POUR-OVER", "STUDIO-MUG", "TUMBLER"]
    POOL_ACCESSORY = ["FILTER-100PK", "CARAFE-1L", "GRINDER", "KETTLE"]
    POOL_OTHER = ["GIFT-CARD", "JOURNAL", "CANDLE"]

    baskets = []
    for _ in range(500):
        hero = random.choice(POOL_HERO)
        basket = {hero}
        # Strong association: pour-over + filter + carafe co-occur
        if hero == "RS-POUR-OVER":
            if random.random() < 0.4:
                basket.add("FILTER-100PK")
            if random.random() < 0.25:
                basket.add("CARAFE-1L")
        # Random additions
        if random.random() < 0.15:
            basket.add(random.choice(POOL_OTHER))
        if len(basket) >= 2:
            baskets.append(basket)

    print(f"Generated {len(baskets)} multi-item baskets")
    thresholds = auto_tune_thresholds(len(baskets))
    print(f"Thresholds: {thresholds}")
    pairs = apriori_pairs(baskets, **thresholds)
    print(f"\n{len(pairs)} FBT pairs found:")
    for p in pairs[:10]:
        print(f"  {p['sku_a']:18s} + {p['sku_b']:18s}  lift={p['lift']:.2f}  conf={p['confidence_max']:.2f}  support={p['support']:.3f}")
