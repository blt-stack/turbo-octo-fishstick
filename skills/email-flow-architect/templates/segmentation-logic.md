# Segmentation Logic

How to define the audience for each flow + each step within a flow. Segmentation is what separates a generic email program from one that converts. The skill defines per-flow filters in the .docx brief; the buyer applies them in Klaviyo's flow editor.

---

## Universal exclusion segment

Every flow should EXCLUDE this segment to avoid sending to disengaged or unsubscribed contacts:

```
Unsubscribed contacts (Klaviyo's built-in unsubscribed list)
+ Bounced contacts (hard-bounced in last 90 days)
+ Marked as spam (any time)
+ Disengaged contacts (no email open in 180+ days AND no purchase in 180+ days)
```

Klaviyo lets you create a "Master Suppression" segment combining these and exclude it from every flow. The skill recommends this setup.

---

## Per-flow segmentation

### Welcome flow

**Inclusion:**
- Joined the email list within the past hour (the trigger condition)

**Exclusion:**
- Already received the Welcome flow before (Klaviyo's "Once per profile" setting handles this)
- Has previously placed an order (they're a returning subscriber, not a new one — use a separate "returning subscriber" Welcome variant)

**Step-level filters:**
- Step 1 (offer email): all new subscribers
- Step 2 (SMS): only subscribers who opted into SMS
- Steps 3-5 (brand story, bestsellers, social proof): all subscribers, no further filter
- Step 6 (SMS last-chance): only subscribers who opted into SMS AND haven't purchased yet
- Step 7 (re-engagement email): only subscribers who haven't purchased by day 10

### Abandoned Cart flow

**Inclusion:**
- Started Checkout event fired in past hour
- AND no Placed Order event for that checkout
- AND cart total > 0

**Exclusion:**
- Has placed an order since the abandonment (they completed)
- Currently in another Abandoned Cart flow (avoid double-firing for the same customer)
- Suppressed (universal suppression segment)

**Step-level filters:**
- Step 1 (1-hour email): all qualifying carts
- Step 2 (4-hour SMS): only subscribers who opted into SMS
- Step 3 (24-hour friction email): all qualifying carts who haven't purchased
- Step 4 (48-hour SMS with discount): only subscribers who opted into SMS AND cart value above the no-discount threshold (typically $30)
- Step 5 (72-hour final): all qualifying carts who haven't purchased

**Segment by cart value:**

```
High-value cart (>$150):
- Send all 5 steps
- Add a "personal touch" task at step 5 (notify buyer to send personal email)

Mid-value cart ($30-$150):
- Send all 5 steps
- Include 5-10% discount in step 4-5

Low-value cart (<$30):
- Send steps 1-3 only (skip the discount step)
```

### Post-Purchase flow

**Inclusion:**
- Placed Order event fired in past hour

**Exclusion:**
- (None — every customer goes through this flow at minimum)

**Step-level filters:**
- Step 1 (order confirmation): all customers
- Step 2 (shipping SMS): only SMS-opted-in customers; fires when Shopify marks the order shipped
- Step 3 (engagement check-in): all customers
- Step 4 (review request): all customers, fires 14 days after delivery date
- Step 5 (replenishment SMS or cross-sell SMS): SMS-opted-in customers; replenishment for consumable categories, cross-sell otherwise
- Step 6 (loyalty / next purchase): all customers

**Segment by customer value:**

```
High-LTV customer (lifetime value > $500):
- Add a personal-touch task at step 6 (notify buyer to send personal thank-you)
- Skip review request (high-LTV customers leave reviews unprompted)

First-time customer:
- Standard flow

Repeat customer:
- Skip "welcome to the brand" framing in step 1
- Use "thanks for coming back" instead
```

### Browse Abandonment flow

**Inclusion:**
- Viewed Product event in past hour
- AND no Added to Cart event for that product in same window
- AND customer is identifiable (logged in OR has email cookie)

**Exclusion:**
- Has purchased this product before
- Currently in Abandoned Cart flow (Abandoned Cart wins — different trigger, deeper signal)
- Suppressed

**Step-level filters:**
- Step 1 (4-hour email): all qualifying browsers
- Step 2 (24-hour SMS): SMS-opted-in
- Step 3 (48-hour friction email): all qualifying browsers who haven't purchased

### Win-back flow

**Inclusion:**
- Has placed at least 1 Order in lifetime
- Has NOT placed an Order in the past [category-specific threshold — 60-180 days]

**Exclusion:**
- Currently in another flow (Welcome, Abandoned Cart)
- Has unsubscribed
- Has placed an order in the past [threshold] days (they're active again)

**Step-level filters:**
- Step 1 (day 0 email): all lapsed customers
- Step 2 (day 7 "what's new" email): all who haven't returned
- Step 3 (day 14 SMS): SMS-opted-in lapsed customers
- Step 4 (day 21 final email): all who haven't returned

**Segment by lifetime value:**

```
High-LTV lapsed (>$500 lifetime):
- Add personal-touch task
- Bigger discount in step 3-4 (typically 20-25%)

Standard:
- 10-15% discount

One-time low-value customer:
- Shorter flow (skip step 2 "what's new"; jump to discount in step 3)
- Single-touchpoint version
```

### Birthday flow

**Inclusion:**
- Customer has a Birthday Date on their profile
- Today is 7 days before that birthday (or recurring annual trigger)

**Exclusion:**
- Has unsubscribed
- Has purchased within past 7 days (skip — feels redundant)

**Step-level filters:**
- Step 1 (email): all birthday-data customers
- Step 2 (SMS): only SMS-opted-in

### Replenishment flow

**Inclusion:**
- Placed Order N days ago (N = category-specific replenishment cycle)
- AND order included a replenishable product
- AND has NOT placed a follow-up order containing that product

**Exclusion:**
- Already subscribed to that product on Subscribe & Save
- Has unsubscribed
- Currently in another flow

**Step-level filters:**
- Step 1 (email at N-7 days from estimated runout): all qualifying customers
- Step 2 (SMS at N+2 days): SMS-opted-in
- Step 3 (email at N+7 days): all who haven't reordered

### Back-in-stock flow

**Inclusion:**
- Customer is on the waitlist for a specific product
- AND that product just transitioned to in-stock

**Exclusion:**
- Has purchased that product since joining the waitlist (already converted)
- Has unsubscribed

**Step-level filters:**
- Step 1 (immediate notification): all waitlist subscribers; email + SMS for SMS-opted-in
- Step 2 (24-hour follow-up): only waitlist subscribers who didn't convert within 24 hours

---

## Segmentation in Klaviyo's UI

The buyer applies these filters in Klaviyo's flow editor at three levels:

1. **Flow trigger** — the initial qualifying event (e.g., "Added to list," "Started Checkout")
2. **Flow filters** — conditions that must be true for the customer to enter the flow at all
3. **Step filters** — conditions checked at each step (so a customer can be in the flow but skip individual steps if they've already met the goal)

The .docx brief documents all three layers per flow. The Klaviyo paste-ready blocks include the segment specification in the file header so the buyer doesn't have to cross-reference the .docx while configuring.

---

## When the buyer's data doesn't support a segment

Sometimes the buyer can't apply a segment because they don't have the data:

- **No SMS opt-in collected:** all SMS steps get filtered out automatically (segment is empty)
- **No birthday data:** Birthday flow can't trigger
- **No purchase history (new store):** Win-back and Replenishment flows can't trigger
- **No waitlist mechanism:** Back-in-stock flow can't trigger

The skill flags these as prerequisites in the .docx brief so the buyer knows what to set up before activating the relevant flow.
