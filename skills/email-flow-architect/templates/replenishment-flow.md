# Replenishment Flow

For consumable products (supplements, skincare, coffee, pet food, household goods), reminds the customer to reorder before they run out. Very high-converting because it lands at the moment of need rather than the moment of marketing.

## Flow specs

- **Trigger:** customer placed an order for a replenishable product, N days have passed (where N = the product's typical use period)
- **Default:** 2 emails + 1 SMS over 14 days
- **Total duration:** ~14 days
- **Goal:** repeat purchase of the consumable product before the customer's supply runs out

## Prerequisite: replenishable products

This flow only applies to categories with predictable consumption cycles. Skip for apparel, home decor, and one-time-purchase categories.

## Trigger timing by category

The N-days-after-purchase trigger varies dramatically by category:

| Category | Trigger at day |
|---|---|
| Daily supplements (30-day supply) | 25 |
| Daily supplements (60-day supply) | 50 |
| Skincare (single product, daily) | 45 |
| Skincare (single product, weekly) | 90 |
| Skincare (full routine, daily) | 60 |
| Whole-bean coffee (1 lb bag) | 14 |
| Whole-bean coffee (5 lb bag) | 45 |
| Loose-leaf tea (50g) | 45 |
| Pet food (small bag) | 21 |
| Pet food (large bag) | 60 |
| Household refills | 45 |

For multi-product orders, use the shortest-cycle product. For subscription-suitable products, the buyer should be running a Subscribe & Save program — Replenishment is for the one-time-purchase customers who haven't subscribed yet.

## Step structure

| Step | Timing | Channel | Purpose |
|---|---|---|---|
| 1 | N-7 days (1 week before estimated runout) | Email | "Restocking up?" — soft heads-up |
| 2 | N+2 days (just after estimated runout) | SMS | "Running low?" reminder with reorder link |
| 3 | N+7 days (1 week past runout) | Email | "Don't forget" — with subscription offer |

Total: 2 emails (1, 3) + 1 SMS (2).

---

## Per-step copy patterns

### Step 1: "Restocking up?" email (N-7 days)

**Subject line patterns:**
- "You might be running low on [product]"
- "Quick check — need more [product]?"
- "Restock [product] before you run out"

**Body:**
1. Soft opener referencing the original purchase
2. The product (image + name + price + restock link)
3. Hint at the subscription option if available: "Want it auto-shipped every 30 days? You'll save 10% on every order"
4. CTA: "Reorder now"
5. Reassurance: "If you're not ready, no worries — we'll check in once more"

Length: 100-150 words.

### Step 2: SMS reminder (N+2 days)

```
Hey [first name], you might be out of [product] by now. Reorder here in 30
seconds: [shortlink]. Reply STOP to opt out.
```

### Step 3: "Don't forget" email + subscription pitch (N+7 days)

If the customer hasn't reordered by N+7, they may have switched brands or fallen off the routine. Last email with a stronger subscription pitch.

**Subject line patterns:**
- "Skip the reorder hassle — subscribe to [product]"
- "[Product] auto-ships, you save"
- "Last reminder — and a subscription option"

**Body:**
1. Acknowledge it's been a while
2. The subscription pitch: how it works, how much they save (typically 10-15%), how to skip / cancel anytime
3. Subscribe button
4. Or — single reorder option (with restock link)
5. Final sign-off

This email's secondary purpose is to convert one-time buyers into subscribers, which dramatically improves customer lifetime value.

---

## Segmentation considerations

- **Filter out customers who have already reordered** — Klaviyo handles this automatically when the flow checks "has not placed an order containing X in the last 7 days"
- **Filter out customers already on Subscribe & Save** for this product — they don't need replenishment reminders
- **For high-LTV customers**, optionally include a small thank-you incentive ("here's a free sample with your next order")

## A/B test plan

1. **Subject line A/B on step 1** — soft check-in vs offer-led
2. **Subscription pitch position** — step 1 vs step 3
3. **Trigger timing test** — N-7 vs N-3 vs N exactly

## Common pitfalls

- **Generic restock email** — works less well than product-specific framing
- **No subscription pitch** — Replenishment is a natural moment to upgrade one-time buyers to subscribers
- **Wrong timing per category** — replenishment for a 90-day skincare product at day 14 feels like nagging

## Performance benchmarks

- Step 1 open rate: 35-50%
- Reorder rate from flow: 15-30% of triggered customers
- Subscription-upgrade rate (one-time → Subscribe & Save) from step 3: 5-15%
- Revenue contribution: 5-15% of program revenue for consumable-heavy stores
