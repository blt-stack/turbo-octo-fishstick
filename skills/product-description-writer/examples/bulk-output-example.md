# Bulk-Mode Output — Reference Structure

When the buyer runs the skill in bulk mode (CSV upload, full Shopify collection, or named list of products), the output is a single `.xlsx` workbook with three sheets.

---

## Sheet 1: Products

One row per product. Columns expand based on which platforms the buyer has enabled in their config.

| Column | Source | Notes |
|---|---|---|
| `Product Name` | Input | From CSV, Shopify pull, etc. |
| `SKU` | Input | If available |
| `Source` | Input | "Shopify", "URL", "Pasted", "Photo" |
| `Shopify Title v1` | Generated | If Shopify enabled |
| `Shopify Body v1` | Generated | Full long-form description |
| `Shopify Meta v1` | Generated | 150-160 char meta description |
| `Shopify Title v2` | Generated | Second angle |
| `Shopify Body v2` | Generated | |
| `Shopify Meta v2` | Generated | |
| `Amazon Title v1` | Generated | If Amazon enabled |
| `Amazon Bullets v1` | Generated | Pipe-separated, 5 bullets |
| `Amazon Description v1` | Generated | |
| `Amazon Search Terms v1` | Generated | |
| `Amazon Title v2` | Generated | |
| ... | ... | (repeats for Amazon v2, then Etsy v1/v2, eBay, Walmart, TikTok Shop) |

Cell content is full prose — buyers copy directly into each platform's backend.

---

## Sheet 2: Character Counts

Same shape as Sheet 1 but each cell shows `actual/limit`. Used for at-a-glance verification that nothing's over.

| Product Name | Amazon Title v1 | Amazon Bullet 1 v1 | Etsy Title v1 | TikTok Name v1 | ... |
|---|---|---|---|---|---|
| River Stone Pour-Over | 147/200 | 138/250 | 96/140 | 32/34 | ... |

Conditional formatting:
- Green fill: cell ≤ 80% of limit
- Yellow fill: cell 80-99% of limit
- Red fill: cell ≥ 100% of limit (over)

---

## Sheet 3: Source Info

Per-product audit trail for the buyer.

| Product Name | Input Source | Voice Profile Version | Keywords Used | Generated At | Notes |
|---|---|---|---|---|---|
| River Stone Pour-Over | Shopify handle: river-stone-pour-over | v2026-05-21 | pour over, ceramic, handmade | 2026-05-21 14:32 | Inferred "stoneware" from product images |

---

## Workbook conventions

- Header row frozen (View → Freeze Top Row)
- Column widths set so each platform's variant pair is visually grouped
- Sheet 1 cells set to wrap text
- Sheet 2 uses conditional formatting (red for over-limit)
- Filename pattern: `{store_name}_descriptions_{date}.xlsx` (set in config)
- Saved to the buyer's configured output folder
