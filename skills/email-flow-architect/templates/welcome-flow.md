# Welcome Flow

The Welcome flow is the highest-leverage flow in an e-commerce email program. Subscribers are warmest in the first 14 days after signup — open rates and click rates often 2-3x normal program averages. Most Welcome flows under-spend on this window by sending only 1-2 emails.

## Flow specs

- **Trigger:** new subscriber joins a list (typically via popup signup, footer signup, or in-store opt-in)
- **Default:** 5 emails + 2 SMS over 14 days
- **Total duration:** 14 days
- **Goal:** convert the subscriber into a first-time buyer (or for already-bought subscribers, a repeat buyer)

## Step structure

| Step | Timing | Channel | Purpose |
|---|---|---|---|
| 1 | Immediate (within 1 min of signup) | Email | Welcome + brand intro + the promised offer |
| 2 | 3 hours later | SMS | Mobile reminder of the offer |
| 3 | 24 hours later | Email | Brand story — why this brand exists |
| 4 | 3 days later | Email | Bestsellers / categories — what to shop |
| 5 | 5 days later | Email | Social proof — featured customer / press / reviews |
| 6 | 7 days later | SMS | Last-chance reminder if signup discount expires |
| 7 | 10 days later | Email | Re-engagement — offer alternative if no purchase yet |

Total: 5 emails (steps 1, 3, 4, 5, 7) + 2 SMS (steps 2, 6).

If the buyer hasn't promised a signup offer (e.g., 10% off), shift the structure:
- Step 1: Welcome + brand intro (no offer to deliver)
- Step 2 (SMS): brand-personality intro, short
- Other steps: same

---

## Per-step copy patterns

### Step 1: Welcome email (immediate)

**Subject line patterns:**
- "Welcome to [brand]. Here's your [offer]."
- "We've been waiting for you."
- "[Subscriber's name (if known)], your code is ready."
- "Hi, this is [founder name]."

**Preview text patterns:**
- "Your 10% off code is inside, plus what to know about us."
- "The thing we're known for, and a discount."
- "What we make, why we make it, and your welcome code."

**Body structure:**
1. Personal opener (founder voice when possible — "Hi, I'm [name]" reads warmer than "Welcome to [brand]")
2. The offer delivered (clearly visible: "Your code: WELCOME10 · 10% off your first order · expires in 7 days")
3. One paragraph on what the brand does and why
4. One CTA — shop the bestsellers
5. Sign-off in brand voice

**Length target:** 150-300 words. Welcome emails should be readable in under 30 seconds.

### Step 2: SMS reminder (3 hours later)

**Pattern:**
```
Hey [first name if known], your welcome code is WELCOME10 for 10% off. Use
it in the next 7 days: [shortlink]. Reply STOP to opt out.
```

**Length target:** 140-160 characters (under SMS standard limit, leaves room for the link expansion).

### Step 3: Brand story email (day 1)

**Subject line patterns:**
- "Why we started making [product category]"
- "The thing we kept getting wrong"
- "Made by [N people]. Here's how."

**Body:** the brand story — origin, what motivated the founder, what makes the brand different. 300-500 words. No CTA at the top; soft CTA at the bottom ("Shop the collection" / "Read more on our About page").

This email is for trust-building. Don't try to sell hard here. The buyers who became long-term customers usually credit a brand-story email as the moment they "got" the brand.

### Step 4: Bestsellers email (day 3)

**Subject line patterns:**
- "Three things our customers can't stop buying"
- "What's selling out this week"
- "The bestsellers most new customers start with"

**Body:** 3-5 featured products (pulled from Shopify connector if available — top sellers by units sold over the past 30 days). Each product gets a tiny block: product image, 1-line description, price, "Shop this" link. Header explains why these are the recommended starting points.

Use this email to introduce category breadth without overwhelming the new subscriber.

### Step 5: Social proof email (day 5)

**Subject line patterns:**
- "[N] customers can't be wrong"
- "What people are saying about [hero product]"
- "Featured in [publication] — and now in your inbox"

**Body:** 3-4 customer reviews (real, attributed when permission given), 1 press mention if available, link to a customer-photo gallery if the buyer has a UGC page. Length 200-400 words.

This email handles the "is this brand real?" objection for subscribers who didn't buy on day 1.

### Step 6: SMS last-chance (day 7)

Only sent if the signup discount has an expiry (typical: 7 days). Skip if no expiring offer.

**Pattern:**
```
Last day to use WELCOME10 for 10% off. We'd hate for you to miss it:
[shortlink]. Reply STOP to opt out.
```

### Step 7: Re-engagement email (day 10)

For subscribers who haven't purchased by day 10. Different tone than the rest of the flow — acknowledges the subscriber hasn't bought yet without being pushy.

**Subject line patterns:**
- "Not the right time?"
- "Let us know what you'd want from us"
- "One more thing before we let you settle in"

**Body:** ask a question ("What category are you most curious about?"). Offer alternative actions (browse a specific collection, read the blog, follow on social). Optionally extend the discount one more time.

Subscribers who engage with this email convert at ~10-15% higher rates than the program average over the following 60 days.

---

## Segmentation considerations

The Welcome flow is mostly NOT segmented — every new subscriber gets it. But there are useful filter rules:

- **Skip step 1's offer email if** the subscriber's email matches an existing customer (avoid offering a new-customer discount to an existing customer — feels like a slap)
- **Skip step 6 SMS if** the subscriber hasn't opted into SMS (TCPA requires opt-in — never SMS-send without it)
- **Skip step 7 if** the subscriber has already made a purchase (they don't need re-engagement; they're converted)

Read `segmentation-logic.md` for the exact filter syntax in Klaviyo.

---

## A/B test plan

Recommended tests in priority order:

1. **Subject line A/B on step 1** — most leverage. Test brand-voice variant vs offer-led variant. Run 14 days, declare winner.
2. **Preview text A/B on step 1** — second priority. Often improves open rate by 5-15% on its own.
3. **CTA button copy on step 4** — "Shop the bestsellers" vs "See what's popular" vs "Browse the collection."
4. **Send delay on step 3** — 24 hours vs 36 hours vs 48 hours. Reveals when subscribers are most engaged.

Each test runs to statistical significance (typically 14 days minimum for low-volume programs, 5-7 days for higher-volume).

---

## Common pitfalls

- **Only 1-2 emails in the Welcome flow.** Underuses the warm window. Always at least 4 emails.
- **Repeating the same CTA in every email.** Variety wins. Different angle per step.
- **Trying to close the sale in every email.** The brand-story and social-proof emails should NOT push hard. Trust-building wins.
- **Generic subject lines.** "Welcome!" or "Thanks for subscribing!" underperform branded, specific subject lines.
- **No SMS leg.** Roughly half of mobile-first subscribers don't open emails reliably. SMS reaches them.
- **Sending step 1 minutes after signup, then nothing for a week.** The 24-hour and 3-day follow-ups are where most conversions happen.

---

## Performance benchmarks (for the buyer's expectations)

For a healthy Welcome flow:

- Step 1 open rate: 45-65%
- Step 1 click rate: 8-15%
- Step 1 conversion rate (purchase within 48 hours): 3-8%
- Overall Welcome flow conversion (purchase within 14 days): 8-15% of subscribers

These are higher than program averages because subscribers are warm. If the buyer's Welcome flow underperforms these, the most common causes are: subject lines, offer clarity (or absence), or sending only 1-2 emails total.
