# Bulk Bundle Catalog — Reference Example

Shows what gets produced when the buyer says "Suggest bundles across my whole catalog."

**Brand:** {{brand_name}} (47-SKU ceramics + coffee accessories catalog)
**Sales data:** 12 months Shopify Orders CSV (3,400 orders)
**Cost data:** 38 of 47 SKUs have cost data (81%)
**Output:** `.xlsx` workbook with 5 sheets

---

## Pipeline outcomes

After running all 3 discovery layers:

- **Apriori pairs found**: 18 SKU pairs pass support ≥ 1%, lift ≥ 2.0, confidence ≥ 25%
- **Apriori triples found**: 4 SKU triples pass the 3-item thresholds
- **Categorical bundles**: 6 from use-case mappings (coffee brewing, candle ritual, gift sets)
- **Total candidates (after dedupe)**: 24 unique bundles
- **After scoring + tier computation**: 18 ranked bundles (top 18 by composite score)

---

## Sheet 1: Bundle Suggestions (18 rows + header)

Sample 5-row excerpt:

| Rank | Bundle Name | Evocative | Type | Composite Score | SKUs | Recommended Price | Tier | Savings | Margin | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Complete Coffee Brewing Set | The Slow Morning Bundle | Complementary (+FBT) | 84.3 | RS-POUR-OVER-001; FILTER-100PK; CARAFE-1L | $78.20 | standard | $13.80 | 65.5% | Suggested |
| 2 | Pour-Over + Filters | (no evocative) | FBT | 81.0 | RS-POUR-OVER-001; FILTER-100PK | $51.00 | standard | $9.00 | 68.0% | Suggested |
| 3 | Candle Care Set | The Slow Burn Set | Complementary | 76.5 | CANDLE-001; WICK-TRIMMER; SNUFFER | $58.00 | standard | $10.00 | 60.3% | Suggested |
| 4 | Mug + Filter Pack | (no evocative) | FBT | 71.2 | STUDIO-MUG; FILTER-100PK | $33.20 | standard | $5.80 | 64.0% | Suggested |
| 5 | Mother's Day Slow Morning Set | (gift) | Gift Set | 68.8 | TEA-SAMPLER; STUDIO-MUG; LAVENDER-CREAM | $72.00 | conservative | $6.00 | 59.0% | Suggested |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

Color-coding:
- **Type column**: each bundle type colored consistently (FBT = blue, Complementary = green, Gift Set = pink, etc.)

---

## Sheet 2: Type Breakdown

```
Bundle Type      Count   Avg Score   Total Potential Savings
FBT                12      75.4         $148.50
Complementary       4      72.1         $58.30
AOV-Lift            1      62.0         $9.50
Gift Set            1      68.8         $6.00
Starter Kit         0      —             —
```

**Insight surfaced**: 12 FBT bundles is a lot — buyer should pick top 4-6 to launch as fixed bundles, not all 12 (would dilute discovery).

**Action prompt**: "No starter kit detected — recommend defining one for first-time customer acquisition. Hero SKU (River Stone Pour-Over) + 1-2 complementary items at 22% off would be the standard starter-kit play."

---

## Sheet 3: SKU Participation

Sorted by # bundles each SKU appears in:

| SKU | Participates In # Bundles | Bundle Names |
|---|---|---|
| FILTER-100PK | 8 | Complete Coffee Brewing Set; Pour-Over + Filters; Mug + Filter Pack; ... |
| RS-POUR-OVER-001 | 5 | Complete Coffee Brewing Set; Pour-Over + Filters; ... |
| STUDIO-MUG | 4 | Mother's Day Slow Morning; Mug + Filter Pack; ... |
| CARAFE-1L | 3 | Complete Coffee Brewing Set; Carafe + Filter; ... |
| CANDLE-001 | 2 | Candle Care Set; Candle + Snuffer |
| WICK-TRIMMER | 2 | Candle Care Set; Candle + Trimmer |
| SNUFFER | 2 | Candle Care Set; Candle + Snuffer |
| ... | ... | ... |
| Single-occurrence SKUs | 1 | ... |

**Insight surfaced**: FILTER-100PK is the most-bundled SKU (in 8 of 18 bundles). This SKU is the brand's "connector" — it ties to nearly everything. Consider promoting it more standalone, or stocking it deeper because it sells alongside many things.

**Insight surfaced**: 12 SKUs in the catalog don't appear in any suggested bundles. These are either niche items or unmapped — buyer should review.

---

## Sheet 4: AOV-Lift Analysis

```
free_shipping_threshold_usd = 75 (from buyer config)

Bundle              Bundle Price   Above Threshold By   Expected Conversion   Est. AOV Lift
The AOV Booster      $79             $4 over             10-20%                 $11.85/conversion
```

Only 1 AOV-Lift bundle suggested. The skill explains:
> "Most bundles in this catalog clear the $75 threshold already at standard pricing. Only the smaller-anchor bundles qualified as AOV-Lift. If buyer wants more AOV-Lift opportunities, consider lowering the free-shipping threshold to $50 — this would expand to ~5 candidate bundles."

---

## Sheet 5: Discovery Audit

| Bundle | Source Layer | Apriori Support | Apriori Lift | Co-occurrence Count | Categorical Use-Case | Margin Score | In-Stock Score | Composite Score |
|---|---|---|---|---|---|---|---|---|
| Complete Coffee Brewing Set | apriori+categorical | 4.00% | 2.80× | 136 | coffee_brewing_complete | 75 | 92 | 84.3 |
| Pour-Over + Filters | apriori | 8.00% | 3.20× | 272 | — | 75 | 92 | 81.0 |
| Candle Care Set | categorical | — | — | — | candle_ritual | 65 | 88 | 76.5 |
| Mug + Filter Pack | apriori | 2.00% | 2.10× | 68 | — | 71 | 90 | 71.2 |
| Mother's Day Slow Morning Set | categorical | — | — | — | mothers_day_curated | 56 | 80 | 68.8 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

The buyer can scan for:
- Bundles with weak apriori evidence (might want to validate before launching)
- Bundles with strong evidence (high-confidence launches)
- Categorical-only bundles (depend on use-case judgment more than data)

---

## Bundle cache writes

All 18 bundles written to `~/.the-ecommerce-seller/cache/bundles/`:

```
~/.the-ecommerce-seller/cache/bundles/
  ├── complete-coffee-brewing-set.json
  ├── pour-over-filters.json
  ├── candle-care-set.json
  ├── mug-filter-pack.json
  ├── mothers-day-slow-morning-set.json
  ├── ...
  └── (18 files total)
```

Skill #1, #3, #5, #8 will see all 18 next time they run.

---

## What the buyer does next

1. **Open Sheet 1 (Bundle Suggestions)** — scan top 5 ranked bundles
2. **Pick 4-6 to launch** — not all 18; quality over quantity
3. **Mark Status = "Approved"** on the chosen bundles
4. **Run skill #3 (Landing Page Copywriter)** — generates bundle landing pages from cache for approved bundles
5. **Run skill #1 (Product Description Writer)** — generates bundle PDPs from cache
6. **Run skill #5 (Ad Creative Generator)** — generates bundle-format ad concepts for approved bundles
7. **Set bundle SKUs up in Shopify** with the recommended bundle app
8. **Re-run bundle-builder in 90 days** — fresh co-purchase data may surface new opportunities

---

## Time savings

Manually:
- Run market basket analysis (Excel pivot tables): 2-4 hours
- Pick complementary bundles by intuition: 1-2 hours
- Calculate pricing + margin for each bundle: 30 min × 18 = 9 hours
- Write positioning copy: 30-60 min per bundle × 18 = 9-18 hours
- Track which bundles overlap, which SKUs are over/under-bundled: rarely done
- **Total: 22-33 hours, with limited rigor on the discovery layer**

With this skill:
- Skill runs the full pipeline: ~30-60 seconds
- Buyer reviews + selects 4-6 bundles: ~45 min
- **Total: ~1 hour to actionable bundle strategy**

The real moat: data-driven Apriori discovery surfaces patterns the buyer wouldn't have intuited. The combination of data + categorical + margin produces bundles that are both rigorous AND strategic — without the buyer having to choose between the two.
