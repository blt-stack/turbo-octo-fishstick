# Data Sources

The digest pulls from four sources. This file documents the metric schema per source, the fallback when a source is missing, and the buyer-side setup expectations.

## Shopify (primary — REQUIRED in practice)

The store's source of truth for revenue, orders, and SKU-level data.

### Connection options
- **Connector via MCP**: real-time pull from Shopify Admin GraphQL API (preferred)
- **Daily CSV export**: buyer uploads `orders.csv` and `products.csv` from Shopify admin export each morning (fallback)
- **Manual paste of yesterday's numbers**: degraded mode for first-run before connector is configured

### Metric schema

```json
{
  "date": "2026-05-22",
  "timezone": "America/New_York",
  "revenue": {
    "gross_usd": 4820.50,
    "discounts_usd": 320.00,
    "refunds_usd": 0.00,
    "shipping_revenue_usd": 145.00,
    "net_usd": 4500.50
  },
  "orders": {
    "count": 47,
    "avg_order_value_usd": 102.56,
    "new_customer_orders": 18,
    "returning_customer_orders": 29
  },
  "conversion": {
    "sessions": 1820,
    "conversion_rate_pct": 2.58
  },
  "top_skus_by_revenue": [
    {"sku": "RS-POUR-OVER-001", "product_name": "River Stone Pour-Over", "units": 18, "revenue_usd": 864.00},
    {"sku": "FILTER-100PK", "product_name": "Filter Pack 100", "units": 22, "revenue_usd": 264.00}
  ],
  "top_skus_by_units": [
    {"sku": "FILTER-100PK", "product_name": "Filter Pack 100", "units": 22}
  ],
  "refunds_returns": {"count": 1, "amount_usd": 48.00, "reasons": ["damaged_in_transit"]}
}
```

### Common buyer-facing issues
- "Why does revenue here differ from my Shopify Home?" — Shopify Home rounds; this skill pulls reconciled order data. Numbers match by end of day.
- "AOV looks low" — check if discount codes are over-applied; this skill computes AOV gross of discounts.
- "Refunds aren't showing" — refunds are dated by day-of-refund, not day-of-original-order. The digest reflects yesterday's refund actions.

---

## Klaviyo (email + SMS)

Marketing automation source. The digest covers both campaigns (one-off sends) and flows (triggered automations).

### Connection options
- **Connector via MCP**: real-time pull from Klaviyo API
- **CSV export**: from Klaviyo Analytics → Custom Reports → daily export

### Metric schema

```json
{
  "date": "2026-05-22",
  "campaigns_sent_yesterday": [
    {
      "name": "Memorial Day Sale Reminder",
      "channel": "email",
      "sent_count": 14200,
      "delivered_count": 13880,
      "open_rate_pct": 32.4,
      "click_rate_pct": 4.1,
      "revenue_usd": 1280.00,
      "revenue_per_send_usd": 0.092,
      "unsubscribes": 8
    }
  ],
  "campaigns_sent_count": 1,
  "total_email_revenue_usd": 1280.00,
  "total_sms_revenue_usd": 0.00,
  "email_pct_of_total_revenue": 28.4,
  "active_flows_performance": [
    {
      "flow_name": "Welcome Series",
      "emails_sent_yesterday": 142,
      "revenue_yesterday_usd": 380.00,
      "open_rate_pct": 48.2,
      "click_rate_pct": 12.1
    },
    {
      "flow_name": "Abandoned Cart",
      "emails_sent_yesterday": 88,
      "revenue_yesterday_usd": 520.00,
      "open_rate_pct": 41.3,
      "click_rate_pct": 8.4
    }
  ],
  "list_growth": {"new_subscribers": 28, "unsubscribes_total": 14, "net_change": 14}
}
```

### What the digest does with this
- Compares each campaign's open/click/RPS against the campaign-type rolling baseline (welcome vs. promo vs. content)
- Surfaces top-performing campaign in the digest
- Flags flows whose performance has dropped (e.g., welcome flow open rate <30% suggests broken segment or stale list)
- Computes email revenue as % of total — a healthy DTC brand typically sees 20-35%

---

## Meta Ads (paid social)

### Connection options
- **Connector via MCP**: Meta Marketing API
- **Daily CSV export**: from Ads Manager → Export reports

### Metric schema

```json
{
  "date": "2026-05-22",
  "spend_usd": 480.00,
  "purchase_value_usd": 1450.00,
  "roas": 3.02,
  "impressions": 38400,
  "reach": 22800,
  "clicks": 982,
  "ctr_pct": 2.56,
  "cpm_usd": 12.50,
  "cpc_usd": 0.49,
  "frequency": 1.68,
  "purchases": 14,
  "cost_per_purchase_usd": 34.29,
  "campaigns": [
    {
      "name": "Cold prospecting — broad",
      "spend_usd": 220.00,
      "revenue_usd": 620.00,
      "roas": 2.82,
      "purchases": 6,
      "frequency": 1.45,
      "ctr_pct": 2.81,
      "objective": "purchase"
    },
    {
      "name": "Retargeting — 30d viewers",
      "spend_usd": 180.00,
      "revenue_usd": 720.00,
      "roas": 4.00,
      "purchases": 7,
      "frequency": 3.42,
      "ctr_pct": 3.12,
      "objective": "purchase"
    }
  ],
  "top_ad_creative": {"ad_name": "...", "spend_usd": 80.00, "roas": 5.20},
  "worst_ad_creative": {"ad_name": "...", "spend_usd": 65.00, "roas": 0.40}
}
```

### What the digest does with this
- Compares ROAS to the 7-day rolling ROAS baseline
- Flags campaigns where frequency >3.5 (fatigue threshold) — recommends rotating creative
- Flags worst-performing campaigns where ROAS dropped below break-even or 1.0x for 3+ days running — recommends pausing
- Surfaces top + worst creative for the day

---

## GA4 (traffic + on-site behavior)

### Connection options
- **Connector via MCP**: GA4 Data API
- **CSV export**: from GA4 Explore → Custom Report

### Metric schema

```json
{
  "date": "2026-05-22",
  "sessions": 1820,
  "users": 1620,
  "new_users": 1280,
  "engaged_sessions": 1240,
  "engagement_rate_pct": 68.1,
  "bounce_rate_pct": 31.9,
  "avg_engagement_time_seconds": 142,
  "source_medium_breakdown": [
    {"source_medium": "google / organic", "sessions": 620, "purchase_revenue_usd": 1100.00, "conv_rate_pct": 2.4},
    {"source_medium": "facebook / paid", "sessions": 480, "purchase_revenue_usd": 1450.00, "conv_rate_pct": 2.9},
    {"source_medium": "(direct) / (none)", "sessions": 310, "purchase_revenue_usd": 920.00, "conv_rate_pct": 3.5},
    {"source_medium": "klaviyo / email", "sessions": 220, "purchase_revenue_usd": 1280.00, "conv_rate_pct": 5.9}
  ],
  "top_landing_pages": [
    {"page": "/products/river-stone-pour-over", "sessions": 480, "conversions": 18, "revenue_usd": 864.00},
    {"page": "/", "sessions": 380, "conversions": 12, "revenue_usd": 580.00}
  ],
  "funnel": {
    "sessions": 1820,
    "view_item_pct": 78.2,
    "add_to_cart_pct": 8.4,
    "begin_checkout_pct": 4.2,
    "purchase_pct": 2.6
  }
}
```

### What the digest does with this
- Cross-references session count vs. conversion to flag traffic-up-orders-down or vice versa
- Surfaces top landing pages + which one drove most conversions
- Channel attribution (email vs. paid vs. organic share) goes into the channel breakdown section
- Funnel step drop-offs vs. baseline → flags conversion-killing pages

---

## When a source is missing

| Source missing | Digest behavior |
|---|---|
| Shopify | Digest cannot run; ask buyer to paste yesterday's numbers manually or upload CSV |
| Klaviyo | Email section blank; flag upgrade path; rest of digest fully runs |
| Meta Ads | Paid ads section blank; flag upgrade path; if total revenue is reported but no spend, digest notes ROAS cannot be computed |
| GA4 | Traffic + funnel section blank; conversion rate omitted from Shopify section; flag upgrade path |

The skill never silently omits — every missing source is called out in the digest so the buyer knows what they're not seeing.

---

## Timezone normalization

Every source reports in different timezones natively:
- Shopify: store's configured timezone (usually buyer's local)
- Klaviyo: configured per account, often UTC
- Meta Ads: account timezone (defaults to UTC)
- GA4: property timezone

The skill normalizes all "yesterday" boundaries to `daily_store_digest.timezone` (config field). This means:
- "Yesterday" = midnight to midnight in the buyer's configured timezone
- Each source query uses that boundary in its own timezone convention
- Numbers may differ slightly from each source's native dashboard because of timezone offset; the digest documents this explicitly when noticeable
