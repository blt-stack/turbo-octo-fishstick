# Bulk-Audit Output — Reference Structure

When the buyer runs SEO audit in bulk mode (CSV, Shopify collection, or named list), the output is a single `.xlsx` workbook with three sheets.

---

## Sheet 1: Scores

One row per product, with total + sub-score columns per enabled platform. Conditional formatting on the Total columns: green ≥ 80, yellow 60-79, red < 60.

| Product Name | SKU | Shopify Total | Shopify KW Cov | Shopify Title | Shopify Bullets | Shopify Backend | Shopify Complete | Amazon Total | Amazon KW Cov | Amazon Title | Amazon Bullets | Amazon Backend | Amazon Complete | Etsy Total | ... |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| River Stone Pour-Over | RSP-001 | 64.5 | 18.0 | 16.0 | 14.0 | 4.5 | 12.0 | 58.0 | 21.0 | 14.0 | 12.0 | 4.0 | 7.0 | 72.5 | ... |
| Velvet Hair Claw 4-Pack | VHC-4PK | 81.0 | 25.0 | 18.0 | 17.0 | 9.0 | 12.0 | 76.5 | 24.0 | 16.0 | 15.5 | 9.0 | 12.0 | — | ... |
| Wool Throw Blanket | WTB-002 | 52.0 | 12.0 | 13.0 | 11.0 | 6.0 | 10.0 | 48.0 | 14.0 | 12.0 | 9.0 | 4.0 | 9.0 | 65.0 | ... |

Use the conditional formatting to triage: sort by Amazon Total ascending and the bottom of the list is where the biggest rewrites are needed.

---

## Sheet 2: Rewrites

One row per product, with optimized copy fields per enabled platform.

| Product Name | SKU | Shopify Meta Title | Shopify Meta Description | Shopify URL Handle | Amazon Title | Amazon Bullets | Amazon Description | Amazon Backend Search Terms | Etsy Title | Etsy Tags | Etsy Description | ... |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| River Stone Pour-Over | RSP-001 | Ceramic Pour Over Coffee Dripper \| Handmade Stoneware \| Brand | Hand-thrown ceramic pour-over... | /products/ceramic-pour-over-coffee-dripper | Brand Ceramic Pour Over Coffee Dripper, Handmade... | ONE PERFECT CUP — Single-cup... \| PAPERLESS BREWING — ... \| ... | The River Stone Pour-Over is built for... | paperless coffee dripper reusable stainless filter single serve... | Handmade Ceramic Pour Over, Single Cup Coffee Dripper... | ceramic pour over, handmade coffee, slow coffee, ... | The pour-over that lives on your counter... | ... |

Bullets use pipe `|` separators within a single cell (so the buyer can split when pasting into Seller Central). Tags use comma separators.

Buyers copy each cell directly into the platform's backend — no re-typing or re-formatting needed.

---

## Sheet 3: Action Items

One row per (product × issue), auto-filtered for easy triage. Buyers sort by issue type or by product to focus their work.

| Product Name | SKU | Platform | Issue |
|---|---|---|---|
| River Stone Pour-Over | RSP-001 | Amazon | Backend search terms only use 0/250 bytes — fill it up |
| River Stone Pour-Over | RSP-001 | Amazon | Only 4 of 5 bullets used |
| River Stone Pour-Over | RSP-001 | Shopify | Meta description missing or over 160 chars |
| River Stone Pour-Over | RSP-001 | Shopify | 3 of 5 images missing alt text |
| Wool Throw Blanket | WTB-002 | Amazon | Backend search terms only use 0/250 bytes — fill it up |
| Wool Throw Blanket | WTB-002 | Amazon | Top-5 keywords missing from listing: ['wool blanket', 'merino throw'] |
| Wool Throw Blanket | WTB-002 | Etsy | Only 7 of 13 tag slots used |
| ... | ... | ... | ... |

The Auto-Filter on the header lets the buyer sort all "Backend search terms empty" issues together and fix them in one batch.

---

## Workbook conventions

- Header row frozen on every sheet
- Auto-filter enabled on Action Items
- Column widths set per sheet purpose (narrow numeric columns for Scores, wide text columns for Rewrites)
- Wrap text on Rewrites and Action Items so long values stay legible
- Conditional formatting only on numeric Total columns in Sheet 1
- Filename pattern: `{store_name}_seo_audit_{date}.xlsx` (set in config)
- Saved to the buyer's configured output folder

## What the buyer does with this

Typical workflow:
1. Open Sheet 1 (Scores), sort by lowest Total across all platforms to find biggest wins
2. Switch to Sheet 3 (Action Items), filter for the products from Step 1
3. Open Sheet 2 (Rewrites), copy each suggested field into the matching backend (Seller Central, Shopify admin, Etsy listing editor)
4. Re-audit those products in a week to see score lift

The `keywords.json` artifact is also written for each product, so future runs of the Product Description Writer on these products pick up the fresh keyword list automatically.
