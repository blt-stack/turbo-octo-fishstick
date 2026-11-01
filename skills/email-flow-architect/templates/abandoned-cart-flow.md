# Abandoned Cart Flow

The single highest-revenue automated flow for most e-commerce stores. Carts are abandoned at 60-80% rates in e-commerce; a strong Abandoned Cart flow recovers 8-15% of those carts. For a store doing $500K/year, that's often $40-80K in recovered revenue annually.

## Flow specs

- **Trigger:** customer adds product to cart, doesn't complete checkout within X minutes (typically 30 min)
- **Default:** 3 emails + 2 SMS over 3 days
- **Total duration:** ~72 hours
- **Goal:** recover the cart by removing whatever friction caused abandonment

## Step structure

| Step | Timing | Channel | Purpose |
|---|---|---|---|
| 1 | 1 hour after abandonment | Email | Gentle reminder + cart contents |
| 2 | 4 hours after abandonment | SMS | Mobile reminder |
| 3 | 24 hours after abandonment | Email | Address the friction (shipping, returns, sizing, etc.) |
| 4 | 48 hours after abandonment | SMS | Last reminder with optional discount |
| 5 | 72 hours after abandonment | Email | Final push with discount + scarcity (if relevant) |

Total: 3 emails (steps 1, 3, 5) + 2 SMS (steps 2, 4).

---

## Per-step copy patterns

### Step 1: Gentle reminder email (1 hour)

This email is the highest-converting in the flow. Most recovered carts come from this step. Don't pitch hard — most customers were genuinely interrupted, not bargain-hunting.

**Subject line patterns (low-pressure):**
- "You left something behind"
- "Still thinking it over?"
- "[Product name] is still in your cart"
- "We saved your cart for you"

Avoid:
- "Don't miss out!" (too pushy)
- "FREE SHIPPING just for you" (offering a discount this early teaches buyers to abandon carts to get one)
- "Only X left in stock!" (artificial urgency this early reads as fake)

**Preview text patterns:**
- "Your [product] is waiting. We'll hold it for [X] hours."
- "Pick up where you left off."
- "[Product] · [Price] · still here"

**Body structure:**
1. Friendly opener acknowledging the abandonment without making the customer feel watched
2. The cart contents (product image, name, price — Klaviyo's dynamic cart block)
3. One clear CTA: "Complete your order"
4. Soft reassurance about brand (returns policy, customer service availability)

**Length target:** 100-200 words. Short and frictionless.

**No discount in step 1.** Discount comes later if needed.

### Step 2: SMS reminder (4 hours)

**Pattern:**
```
Hey [first name], your cart at [brand] is still here: [shortlink]. We'll
hold it for the next 24 hours. Reply STOP to opt out.
```

Brief, friendly, no offer yet.

### Step 3: Friction-addressing email (24 hours)

This email assumes the customer didn't return because of a specific friction. The most common frictions in DTC: shipping cost, return policy uncertainty, sizing/fit confusion, brand-trust concerns.

**Subject line patterns:**
- "About shipping..."
- "We make returns easy."
- "Questions about [product]?"
- "Sizing help — and your cart"

**Body structure:**
1. Address the most likely friction directly: "If shipping or returns held you back, here's how we handle it..."
2. Specific reassurance — concrete numbers, not vague claims ("30-day money-back returns" > "easy returns")
3. Cart contents reminder
4. CTA: "Complete your order"
5. Optional: link to FAQ or to a customer service chat

If the buyer's category has a specific friction (e.g., color/size uncertainty for apparel), customize this email for that friction. The skill checks `config.audience` and `config.store.primary_category` to pick the friction-addressing angle.

### Step 4: SMS last reminder + optional discount (48 hours)

Only include the discount if the buyer has authorized one. Discounts in Abandoned Cart should be modest (5-10%) — bigger discounts train customers to always abandon for the discount.

**Pattern (with discount):**
```
Last reminder — your [brand] cart, plus a 10% discount: SAVE10. Expires in
24 hrs. [shortlink] Reply STOP to opt out.
```

**Pattern (without discount):**
```
Hey [first name], your cart is still waiting. We can hold it one more day:
[shortlink]. Reply STOP to opt out.
```

### Step 5: Final push email (72 hours)

Last email in the sequence. If the buyer hasn't converted by 72 hours, they're likely not going to from this cart. But a final, slightly more urgent email recovers another 1-3% of remaining carts.

**Subject line patterns:**
- "Last chance — your cart"
- "[Discount code] expires tonight"
- "We're letting your cart go after this"

**Body structure:**
1. Acknowledge this is the last email about this cart
2. Restate the offer if there is one
3. Cart contents
4. Add one trust signal not yet used (a customer review, a press mention)
5. Clear final CTA

After step 5, the cart is released back to the customer's general browsing — they're no longer "in the Abandoned Cart flow."

---

## Segmentation considerations

The Abandoned Cart flow benefits from segmentation by cart value:

| Cart value | Flow adjustment |
|---|---|
| Under $30 | Skip the discount in step 4/5 — discount eats too much of the margin |
| $30-$150 | Standard flow with 5-10% discount in step 4-5 |
| $150-$500 | Standard flow + add a personal-touch email from "customer service" in step 5 |
| $500+ | High-touch flow: a real person reaches out (use Klaviyo's task creation to notify the buyer to send a personal email) |

Other useful segments:
- **Repeat customer cart abandonment:** treat as warmer (less hard-sell, more "we noticed you didn't finish, anything we can help with?")
- **First-time customer:** standard flow, slightly stronger trust signals throughout
- **Subscriber but not customer:** standard flow, also link to their welcome offer if still active

Read `segmentation-logic.md` for the Klaviyo filter syntax.

---

## A/B test plan

1. **Subject line A/B on step 1** — pre-purchase intent is highest here; subject line is the leverage
2. **Discount on step 4 vs no discount** — test whether the 5-10% discount lifts recovery enough to justify the margin hit
3. **Step 3 angle test** — shipping-focused vs returns-focused vs sizing-focused (depending on category)
4. **Send delay on step 1** — 1 hour vs 2 hours vs 4 hours

---

## Common pitfalls

- **Sending step 1 too late** — past 24 hours, recovery rates drop sharply. Sub-2-hour delay is critical.
- **Offering a discount in step 1** — trains customers to abandon for the discount
- **Generic copy** — "you left something in your cart" is everyone's flow. Brand voice + specific product mention beats generic.
- **No SMS leg** — Abandoned Cart SMS recovery rates often beat email rates because mobile-cart-abandoners check phones, not inboxes.
- **Fake urgency in step 1** — "Only 3 left!" when there are 300. Customers see through this and trust drops permanently.
- **Skipping the friction-addressing email** — step 3 is often the conversion difference for high-consideration purchases.

---

## Performance benchmarks

For a healthy Abandoned Cart flow:

- Step 1 open rate: 45-65%
- Step 1 click rate: 12-20%
- Overall flow recovery rate (% of abandoned carts that convert within 72 hours): 8-15%
- Recovered revenue as % of store revenue: 5-15% (the more sophisticated the flow, the higher)

If the buyer's flow underperforms, the most common causes are: delayed step 1, generic copy, no SMS, no segmentation by cart value.
