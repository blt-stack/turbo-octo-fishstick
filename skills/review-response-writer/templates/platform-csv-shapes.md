# Platform CSV Shapes

When the buyer uploads a CSV of reviews, the skill parses based on the platform. Each platform's export format differs. The skill auto-detects which platform produced the export by inspecting column headers, then maps to the canonical internal schema.

## Canonical internal schema

After parsing, every review row maps to this schema:

```json
{
  "platform": "judge_me",
  "product_name": "River Stone Pour-Over",
  "product_id": "...",
  "product_handle": "river-stone-pour-over",
  "reviewer_name": "Sarah M.",
  "reviewer_email": "sarah.m@example.com",
  "star_rating": 5,
  "review_title": "Beautiful piece",
  "review_body": "Full review text...",
  "received_at": "2026-05-10T14:23:00Z",
  "verified_purchase": true,
  "order_id": "#1024",
  "platform_review_id": "..."
}
```

Downstream pipeline operates on canonical schema. Per-platform parsers handle the column-name mapping.

## Judge.me CSV export

Path: Judge.me dashboard → Manage Reviews → Export → CSV

Columns (as exported):
- `Order ID`
- `Product handle`
- `Product Name`
- `Rating` (1-5)
- `Title`
- `Body`
- `Reviewer Name`
- `Reviewer Email`
- `Posted at`
- `Verified Buyer` (yes/no)
- `Reply` (existing reply if any)
- `Curated` (yes/no)
- `Published` (yes/no)

Skill ignores reviews where `Reply` is non-empty (already replied) unless buyer requests "re-reply" mode. Skill ignores reviews where `Published` is "no" by default.

## Loox CSV export

Path: Loox dashboard → Reviews → Export reviews → CSV

Columns:
- `Created at`
- `Product ID`
- `Product Title`
- `Rating`
- `Name`
- `Email`
- `Verified` (true/false)
- `Body`
- `Has photo` (true/false)
- `Has video` (true/false)
- `Reply`

Loox doesn't export product handles consistently; map by Product Title where handle is missing.

## Yotpo CSV export

Path: Yotpo dashboard → Reviews → Manage Reviews → Export

Columns:
- `Review id`
- `Score` (1-5)
- `Title`
- `Content`
- `Date`
- `Email`
- `Name`
- `Product Name`
- `Product Url`
- `Verified Buyer` (Yes/No)
- `Reviewer Response` (existing reply)

## Amazon Seller Central export

Path: Seller Central → Brand Registry → Customer Reviews → Download

Columns:
- `Date`
- `ASIN`
- `Product`
- `Rating` (1-5)
- `Title`
- `Body`
- `Verified Purchase` (Yes/No)
- `Customer Name`
- `Helpful Votes`

Amazon doesn't export reviewer emails (privacy). The skill operates without email for Amazon batches — Buyer-Seller Messaging is the only follow-up channel.

## Etsy CSV export

Etsy doesn't provide a native review export. The buyer either:
1. Uses a third-party scraper (the skill ingests the resulting CSV)
2. Manually copies reviews into the canonical CSV template (see `templates/etsy-csv-template.md`)
3. Pastes individual reviews into single mode

Common third-party scrapers produce columns:
- `Date`
- `Listing ID`
- `Listing Title`
- `Rating`
- `Review`
- `Buyer Name`

Skill auto-detects and maps.

## Google Business Profile export

Path: Google Business Profile manager → Reviews → Export (or via Google API for Business)

Columns:
- `Reviewer Name`
- `Star Rating`
- `Review Text`
- `Review Date`
- `Profile Link`
- `Reply`
- `Reply Date`

Google's export is limited; some metadata not available.

## Trustpilot CSV export

Path: Trustpilot Business → Reviews → Export → CSV

Columns:
- `Date`
- `Reviewer Name`
- `Reviewer Country`
- `Stars` (1-5)
- `Title`
- `Body`
- `Source` (organic, invitation, etc.)
- `Verified` (Yes/No)
- `Reply`
- `Reply Date`
- `Tags`
- `Order Reference` (when provided)

Trustpilot's CSV is the most detailed of all platforms.

## Facebook Recommendations export

Facebook doesn't provide a native review export. The buyer either:
1. Copies recommendations into the canonical template
2. Uses Meta's Business Suite export (limited fields)

Manual entry is common — single-mode is often more practical for Facebook batches.

## Auto-detection logic

The skill detects platform by header signature:

| Header signature | Platform |
|---|---|
| Has `Product handle` AND `Verified Buyer` | Judge.me |
| Has `Has photo` AND `Has video` | Loox |
| Has `Score` AND `Product Url` | Yotpo |
| Has `ASIN` AND `Helpful Votes` | Amazon |
| Has `Reviewer Country` AND `Source` | Trustpilot |
| Has `Star Rating` AND `Profile Link` | Google |
| Has `Listing ID` (any column ID format) | Etsy |
| Otherwise | Generic / unknown — ask user |

When the platform can't be detected, the skill asks the buyer to confirm which platform the CSV came from before parsing.

## Generic CSV template

For buyers who want to combine reviews from multiple platforms into one CSV, the canonical template is:

```csv
platform,product_name,reviewer_name,reviewer_email,star_rating,review_title,review_body,received_at,verified_purchase,order_id
shopify_judge_me,River Stone Pour-Over,Sarah M.,sarah.m@example.com,5,Beautiful,Full review text...,2026-05-10,true,#1024
amazon,River Stone Pour-Over,Marcus T.,,2,Arrived broken,Body text...,2026-05-15,true,
```

Any column subset is accepted; missing fields default to null. The `platform` column must be one of: `shopify_judge_me`, `shopify_loox`, `shopify_yotpo`, `shopify_stamped`, `shopify_reviews_io`, `amazon`, `etsy`, `google`, `trustpilot`, `facebook`.

## Parsing edge cases

- **Newlines in body fields:** Most exports preserve them; the skill normalizes.
- **Unicode / emojis in reviewer names:** Preserve exactly as exported.
- **Missing star rating:** Default to neutral handling (3★ tier) and flag in report.
- **Missing review body:** Skip — can't draft a reply to an empty review.
- **Existing reply present:** Skip by default unless buyer explicitly requests re-reply mode.
- **Duplicate reviews:** Detect by (reviewer_name, product, received_at) tuple; flag in report.
