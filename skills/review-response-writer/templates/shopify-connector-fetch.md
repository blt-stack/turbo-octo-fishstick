# Shopify Connector Fetch — Judge.me / Loox / Yotpo Metafield Paths

When the buyer has the Shopify connector enabled and uses Judge.me, Loox, or Yotpo, the skill can auto-fetch reviews without requiring a CSV export. Each app stores reviews in different Shopify metafield namespaces.

## Why metafields instead of the app's own API?

Each review app has its own API, but adding direct API integration per app would require per-app auth setup. The Shopify connector is already authenticated, and most Shopify-integrated review apps mirror their review data into product metafields so the brand can display reviews on the storefront.

This means the skill can read recent reviews from Shopify metafields without additional setup.

## Limitations

- Metafields are typically synced with a lag (5-60 minutes), so the freshest reviews may not yet be available
- Some apps only sync summary data (count, average) to metafields, not full review text
- Free-tier apps often skip metafield sync; paid tiers usually include it

When metafield sync isn't available or returns nothing, the skill falls back to asking the buyer for a CSV export.

## Judge.me metafield paths

Judge.me syncs reviews to two namespaces:

```
namespace: judgeme
keys:
  - reviews            (JSON: array of recent reviews, typically last 25)
  - review_count       (integer)
  - average_score      (float)
  - badge              (HTML snippet)
```

Each review in the `judgeme.reviews` JSON has:

```json
{
  "id": 123456,
  "rating": 5,
  "title": "Beautiful piece",
  "body": "Full review text...",
  "reviewer": {
    "name": "Sarah M.",
    "email": "sarah.m@example.com",
    "verified_buyer": true
  },
  "created_at": "2026-05-10T14:23:00Z",
  "reply": null,
  "published": true,
  "curated": false
}
```

Map directly to canonical schema.

## Loox metafield paths

Loox syncs to:

```
namespace: loox
keys:
  - reviews            (JSON: recent reviews)
  - rating             (float)
  - num_reviews        (integer)
```

Review object:

```json
{
  "id": "...",
  "rating": 5,
  "title": "...",
  "text": "...",
  "name": "Sarah",
  "email": "sarah.m@example.com",
  "created_at": "2026-05-10",
  "verified": true,
  "reply": null,
  "has_image": true,
  "image_urls": ["..."]
}
```

Note: Loox uses `text` not `body`. Map accordingly.

## Yotpo metafield paths

Yotpo syncs to:

```
namespace: yotpo
keys:
  - reviews            (JSON: recent reviews)
  - bottomline         (JSON: aggregate stats)
```

Review object:

```json
{
  "id": "...",
  "score": 5,
  "title": "...",
  "content": "...",
  "name": "Sarah",
  "email": "sarah.m@example.com",
  "date": "2026-05-10",
  "verified_buyer": true,
  "is_published": true
}
```

Note: Yotpo uses `score` not `rating`, `content` not `body`. Map accordingly.

## Stamped and Reviews.io

Stamped and Reviews.io don't reliably sync to Shopify metafields. For these apps, the buyer must export CSV from the app's own dashboard. The skill flags this in the report.

## Fetching all products vs. selective

When the buyer says "process all my recent reviews," the skill:
1. Queries Shopify for all products
2. For each, fetches the relevant metafield namespace
3. Aggregates reviews across products
4. Filters by `created_at` >= N days ago (default 7)
5. Filters out reviews where `reply` is already populated
6. Returns up to the buyer-specified count (default 25)

When the buyer says "process recent reviews for [product name]," the skill:
1. Queries Shopify for the specific product
2. Reads metafields for that product only
3. Returns reviews matching same filters

## Fallback flow

If the connector returns 0 reviews or an error:

1. Skill checks if metafield namespace exists at all
2. If not: tells buyer "Your review app doesn't appear to sync to Shopify metafields — please export a CSV from [app] and re-run"
3. If yes but 0 reviews: tells buyer "No new reviews in the last [N] days. Want to extend the window?"
4. If error: tells buyer the specific error and recommends CSV upload as fallback

## Connector availability check

The skill calls a Shopify connector availability check at the start of bulk mode. If unavailable, it skips the auto-fetch path entirely and asks for CSV upload.

## Rate limiting

Shopify rate limits the metafield read endpoint at 40 calls per minute (REST) or 1000 cost-points per second (GraphQL). For brands with > 100 products, the skill paginates with respect to rate limits — typically takes 1-3 minutes for a full-catalog fetch.

For most solo sellers (10-50 SKUs), the fetch completes in under 30 seconds.

## Future expansion

When the skill matures, direct API integration with Judge.me / Loox / Yotpo / Trustpilot will be added as optional connectors. For now, the metafield path + CSV fallback covers ~95% of practical use cases.
