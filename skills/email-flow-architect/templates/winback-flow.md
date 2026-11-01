# Win-back Flow

Reactivates customers who haven't purchased in 60-180 days. Lapsed customers are 5-7x easier to re-engage than acquiring new customers (existing trust, existing knowledge of the brand). A well-built Win-back flow reactivates 5-15% of lapsed customers per cycle.

## Flow specs

- **Trigger:** customer made a purchase, hasn't purchased again in 60-180 days (specific threshold varies by category — see below)
- **Default:** 3 emails + 1 SMS over 21 days
- **Total duration:** ~21 days
- **Goal:** bring the lapsed customer back for a second (or N-th) purchase

## Lapse threshold by category

The "when to trigger Win-back" depends on natural repurchase cadence:

| Category | Typical lapse threshold |
|---|---|
| Supplements / consumables | 60-90 days |
| Coffee / tea / pantry items | 60-90 days |
| Skincare | 90-120 days |
| Apparel | 120-180 days |
| Home decor | 180-365 days |
| Kitchen tools | 365+ days (or skip — too long) |
| Gift-purchase categories | 60-90 days (annual gifting cycle) |

The skill picks the threshold based on `config.store.primary_category`. Buyer can override.

## Step structure

| Step | Timing | Channel | Purpose |
|---|---|---|---|
| 1 | Day 0 (when threshold reached) | Email | "We miss you" — soft re-engagement |
| 2 | Day 7 | Email | Show what's new since they last bought |
| 3 | Day 14 | SMS | Last-chance offer with discount |
| 4 | Day 21 | Email | Final email with biggest offer + clear "moving on if we don't hear back" |

Total: 3 emails (1, 2, 4) + 1 SMS (3).

---

## Per-step copy patterns

### Step 1: "We miss you" email (day 0)

The "soft" entry. Acknowledge the time gap without being passive-aggressive.

**Subject line patterns:**
- "It's been a while — here's what's new"
- "Did we miss something, [first name]?"
- "Welcome back, if you've been meaning to"

Avoid:
- "We miss you!" (everyone's first subject line — high spam-folder risk)
- "Don't you want to come back?" (manipulative)

**Body:**
1. Light opener acknowledging the gap ("It's been [N] days since your last [product] — hope life's good")
2. One sentence about what they last bought (Klaviyo can dynamically pull)
3. A brand update — what's new since they were last around (a new product, a featured collection, a milestone)
4. Soft CTA: "Come back and look around" (links to homepage or to a curated "best of" collection)

Length: 100-200 words. No offer yet.

### Step 2: "What's new" email (day 7)

Show the buyer what they've missed. New products, new collections, content they might like.

**Subject line patterns:**
- "Three things we've added since [season they last bought]"
- "What's new at [brand]"
- "You missed: [feature/product]"

**Body:**
1. Brief intro
2. 3-4 products or content pieces released since the customer's last visit
3. Each item gets a tiny block (image + 1-line description + price + link)
4. Soft CTA: "Browse everything new"

No offer yet — still building re-engagement.

### Step 3: SMS with discount (day 14)

By day 14, the customer hasn't bought. Time for a real incentive.

```
Hey [first name], we'd love to have you back at [brand] — here's 15% off
to make it easy: WELCOME-BACK-15 (valid 7 days). [shortlink] Reply STOP to opt out.
```

Discount size: 10-20% depending on category margin. Higher discounts work for apparel; lower for low-margin categories.

### Step 4: Final push email (day 21)

The closing email. Sets a clear endpoint — Klaviyo will let the customer back into the regular program after this, but the Win-back flow stops.

**Subject line patterns:**
- "Last call: [discount]% off — and we'll let you settle"
- "We'll stop reaching out after this one"
- "One more invitation"

**Body:**
1. Acknowledge: "This is the last email about coming back — promise"
2. Restate the offer
3. One paragraph about what they were great at when they were a customer (or what made the brand work for them)
4. Final CTA
5. Soft graceful sign-off: "Either way, thanks for being part of the brand"

This email's "we'll let you go" framing actually lifts response rates 5-15% over standard urgency framings — it respects the customer's choice.

---

## Segmentation considerations

- **High-LTV customers** (spent over a threshold across all orders): get the longer, more personal flow + bigger offer
- **One-time buyers** (only ever placed one order): get a shorter version with a stronger offer
- **Customers who unsubscribed from email but still receive SMS:** Win-back via SMS-only
- **Customers who opted out of both:** skip entirely — they've said no

## A/B test plan

1. **Subject line A/B on step 1** — soft vs offer-led vs question-led
2. **Discount size on step 3-4** — 10% vs 15% vs 20%
3. **Send threshold** — 60 days vs 90 days for category default

## Common pitfalls

- **Win-back too soon** — sending at day 30 to a category with 90-day cycles feels like nagging
- **Win-back too late** — sending at day 365 to a 60-day category, the customer has fully forgotten and the discount goes to a stranger
- **No SMS leg** — Win-back is one of the best SMS use cases (the email inbox where the brand lives has gone stale; SMS reaches them)
- **Generic discount code reused across Win-back and Welcome** — can't track which flow drove the recovery

## Performance benchmarks

- Step 1 open rate: 20-35% (lower than active programs — customers are colder)
- Overall flow reactivation rate: 5-15% of lapsed customers
- Win-back ROI: typically 5-10x (acquisition cost for lapsed customers is near-zero)
