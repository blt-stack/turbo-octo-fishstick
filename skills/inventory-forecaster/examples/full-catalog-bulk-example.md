# Full Catalog Bulk — Reference Example

Shows what gets produced when the buyer says "Forecast my entire catalog and tell me what I need to reorder this quarter."

**Brand:** {{brand_name}}
**Scope:** All 47 active SKUs in catalog
**Input:** Shopify Orders CSV (15 months) + Amazon Business Reports CSV (12 months for 8 ASINs)
**Output:** `.xlsx` workbook with 5 sheets + reorder triggers cache write

---

## Method distribution across catalog

After the forecast run:

| Method | SKUs | Why |
|---|---|---|
| Holt-Winters (seasonal) | 18 | 180+ days history with detected seasonality (mostly 7-day weekly cycles) |
| Holt (trend only) | 16 | 60-180 days history, or 180+ with no seasonal signal |
| Rolling Average 14d | 9 | <60 days history (mostly newer SKUs) |
| Poisson heuristic | 3 | Sporadic SKUs (<0.5/day avg, lumpy demand) |
| Skipped | 1 | One drop-ship SKU |

---

## Sheet 1: SKU Forecast (47 rows + header)

Sample 6-row excerpt showing the variety:

| SKU | Product | Supplier | Method | Confidence | History Days | Velocity | On Hand | Days to Stockout | 30d P50 | 60d P50 | 90d P50 | Status | Reorder Qty | Deposit Date | Cost | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RS-POUR-OVER-001 | River Stone Pour-Over | shenzhen-stoneworks | Holt-Winters | high | 456 | 12.3 | 220 | 18 | 390 | 780 | 1170 | **URGENT** | 1500 | 2026-04-15 | $6,300 | — |
| STUDIO-BOWL-LRG | Studio Glaze Bowl L | jingdezhen-ceramics | Holt | high | 287 | 6.5 | 320 | 49 | 210 | 420 | 630 | **REORDER SOON** | 800 | 2026-05-03 | $4,880 | — |
| TUMBLER-12OZ | Travel Tumbler 12oz | shenzhen-stoneworks | Holt-Winters | high | 412 | 9.8 | 850 | 87 | 310 | 620 | 920 | HEALTHY | — | — | — | — |
| WEEKEND-TOTE | Weekend Tote Bag | bat-trang-heritage | Holt | medium | 142 | 3.1 | 110 | 35 | 95 | 190 | 280 | **URGENT** | 800 | 2026-04-18 | $4,000 | — |
| NEW-CANDLE-LAUNCH | Forest Candle (launch) | (unmapped) | Rolling Avg 14d | low | 38 | 2.5 | 65 | 26 | 90 | 180 | 270 | **REORDER SOON** | 100 | 2026-04-28 | $250 | low_history |
| GIFT-SET-XMAS | Holiday Gift Set | shenzhen-stoneworks | Holt-Winters (365d) | medium | 540 | 0.4 | 35 | 86 | 14 | 28 | 42 | HEALTHY | — | — | — | — |

Color-coding:
- **Status column**: red (stockout_imminent), orange (urgent), yellow (reorder_soon), green (healthy)
- **Confidence column**: green (high), yellow (medium), orange (low), red (unreliable)

---

## Sheet 2: Stockout Risk (8 rows — only at-risk SKUs)

| SKU | Product | Urgency | Days to Stockout P50 | Lead Time | Days Short | Reorder Qty | Deposit Date | Cost | Expedite? | Action Plan |
|---|---|---|---|---|---|---|---|---|---|---|
| RS-POUR-OVER-001 | River Stone Pour-Over | urgent | 18 | 45 | 27 | 1500 | 2026-04-15 | $6,300 | Yes | (buyer fills in) |
| WEEKEND-TOTE | Weekend Tote Bag | urgent | 35 | 40 | 5 | 800 | 2026-04-18 | $4,000 | Yes | (buyer fills in) |
| TEA-INFUSER | Loose Tea Infuser | urgent | 22 | 45 | 23 | 1000 | 2026-04-15 | $1,800 | Yes | |
| NEW-CANDLE-LAUNCH | Forest Candle (launch) | reorder_soon | 26 | 21 | 0 | 100 | 2026-04-28 | $250 | No | |
| GLASS-CARAFE | Glass Carafe 1L | reorder_soon | 52 | 35 | 0 | 500 | 2026-05-10 | $2,250 | No | |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

The buyer scans this sheet first thing — these are the SKUs that need attention this week.

---

## Sheet 3: Reorder Calendar (chronological)

Same 8 SKUs, sorted by deposit date:

| Deposit Date | SKU | Product | Supplier | Reorder Qty | Cost | Urgency | Expected Arrival |
|---|---|---|---|---|---|---|---|
| 2026-04-15 | RS-POUR-OVER-001 | River Stone Pour-Over | shenzhen-stoneworks | 1500 | $6,300 | urgent | 2026-06-29 |
| 2026-04-15 | TEA-INFUSER | Loose Tea Infuser | shenzhen-stoneworks | 1000 | $1,800 | urgent | 2026-06-04 |
| 2026-04-18 | WEEKEND-TOTE | Weekend Tote Bag | bat-trang-heritage | 800 | $4,000 | urgent | 2026-06-23 |
| 2026-04-28 | NEW-CANDLE-LAUNCH | Forest Candle | (unmapped) | 100 | $250 | reorder_soon | (buyer to confirm) |
| 2026-05-03 | STUDIO-BOWL-LRG | Studio Glaze Bowl L | jingdezhen-ceramics | 800 | $4,880 | reorder_soon | 2026-07-12 |
| 2026-05-10 | GLASS-CARAFE | Glass Carafe 1L | shenzhen-stoneworks | 500 | $2,250 | reorder_soon | 2026-07-05 |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Insight surfaced**: 3 reorders to Shenzhen Stoneworks all clustered in April-May — buyer can consolidate into one combined order to negotiate better pricing tier (potentially via skill #11).

---

## Sheet 4: Seasonality Patterns

| SKU | Product | Seasonal Period | Signal Strength | Method | Confidence |
|---|---|---|---|---|---|
| RS-POUR-OVER-001 | River Stone Pour-Over | 7-day | 0.42 | Holt-Winters | high |
| STUDIO-BOWL-LRG | Studio Glaze Bowl L | 7-day | 0.38 | Holt-Winters | high |
| TUMBLER-12OZ | Travel Tumbler 12oz | 7-day | 0.45 | Holt-Winters | high |
| GIFT-SET-XMAS | Holiday Gift Set | 365-day | 0.71 | Holt-Winters | high |
| MOTHERS-DAY-BUNDLE | Mother's Day Bundle | 365-day | 0.55 | Holt-Winters | medium |
| ... | ... | ... | ... | ... | ... |

**Insight surfaced**: 3 SKUs show 365-day seasonality (holiday-driven). Mother's Day (May 10) is approaching — the MOTHERS-DAY-BUNDLE forecast may be more conservative than the actual surge; buyer should consider safety stock boost before April 25.

---

## Sheet 5: Method Audit Log (47 rows)

| SKU | Method | Rationale | Confidence | History Days | Fallback? | Warnings |
|---|---|---|---|---|---|---|
| RS-POUR-OVER-001 | Holt-Winters | 456 days + seasonal signal at 7-day lag (autocorr 0.42) | high | 456 | No | — |
| STUDIO-BOWL-LRG | Holt | 287 days history; no seasonal signal above threshold | high | 287 | No | — |
| NEW-CANDLE-LAUNCH | Rolling Avg 14d | 38 days history (<60 threshold) — rolling average is robust | low | 38 | No | low_history |
| SPARSE-LIMITED-ED | Poisson | Sporadic SKU: >30% zero days + mean velocity <0.5/day | low | 180 | No | velocity_below_threshold, sporadic_sales |
| RECENT-OUTLIER-SKU | Holt | 95 days history (60-179) — Holt captures trend | medium | 95 | No | recent_outlier |
| ... | ... | ... | ... | ... | ... | ... |

The buyer can scan for low-confidence rows + override methods next run if needed.

---

## Reorder triggers written

To `<plugin-root>/.cache/reorder_triggers/2026-04-15.json`:

```
8 triggers written:
  3 urgent (RS-POUR-OVER-001, WEEKEND-TOTE, TEA-INFUSER)
  5 reorder_soon
  0 stockout_imminent
```

These will surface in skill #11 next time the buyer drafts supplier letters.

---

## What the buyer does next

1. **Open Sheet 2 (Stockout Risk)** — 3 urgent reorders need decisions this week
2. **For each urgent**: review the recommended reorder qty + decide expedite vs. accept gap
3. **Open Sheet 3 (Reorder Calendar)** — see April-May reorders clustered to Shenzhen Stoneworks → opportunity to consolidate
4. **Open Sheet 4 (Seasonality)** — note Mother's Day bundle approaching peak
5. **Run skill #11** — "Draft supplier letters for today's reorder triggers" — pulls from the cache automatically
6. **Map unmapped SKUs** — NEW-CANDLE-LAUNCH has no supplier yet; buyer maps via prompt
7. **Re-forecast in 7-14 days** — monitor velocity drift on hero SKUs

---

## Time savings

Manually:
- Forecast 47 SKUs in a spreadsheet (or guess): 4-8 hours, with much guessing
- Cross-reference each SKU's supplier lead time / MOQ from past invoices: 2-3 hours
- Build reorder calendar manually: 1 hour
- Identify seasonality patterns by eye: rarely done
- Catch sporadic-SKU outliers: rarely done
- **Total: 7-12 hours over 2 days, with poor confidence**

With this skill:
- Skill runs the full catalog: ~30-60 seconds (depending on history depth)
- Buyer reviews + acts on the 8-row Stockout Risk sheet: ~30 min
- **Total: ~30-45 min, with method transparency + supplier integration + auto cache writes**

The real moat: **catching stockout-imminent issues 4-6 weeks before they happen**. For a 47-SKU catalog, missing even one hero SKU's reorder window can cost more than the entire annual subscription to the plugin.
