# Birthday Flow

A single annual touchpoint that lifts both engagement and revenue from existing subscribers. Birthday flows are simple to build and rarely a top revenue driver, but they're a brand-warmth play — customers feel remembered.

## Flow specs

- **Trigger:** subscriber's birthday (requires having collected birthday data at signup or via profile update)
- **Default:** 1 email + 1 SMS over 7 days
- **Total duration:** 7 days
- **Goal:** acknowledge the birthday, drive a celebratory purchase

## Prerequisite: collecting birthdays

The flow only works if the buyer has birthday data. Most stores don't collect it. The skill flags this and offers a side-recommendation: add a birthday field to the signup form OR send a one-off "share your birthday" email to the existing subscriber base.

## Step structure

| Step | Timing | Channel | Purpose |
|---|---|---|---|
| 1 | 7 days before birthday | Email | "Birthday week is coming" — primes the buyer + offer |
| 2 | On birthday | SMS | Same-day birthday wish + offer reminder |

Total: 1 email + 1 SMS. Some brands add a "1 day before expiry" reminder — skill includes it as an optional 3rd step.

---

## Per-step copy patterns

### Step 1: Birthday email (7 days before)

**Subject line patterns:**
- "Birthday week is coming, [first name]"
- "A gift for your birthday — from us"
- "Something nice for your week"

**Body:**
1. Warm acknowledgment of the upcoming birthday
2. The gift (typically a discount code "BIRTHDAY15" for 15-20% off, or a free gift with purchase, or free shipping)
3. The expiry date (typically 7-14 days from birthday)
4. Soft CTA: "Shop something for yourself"
5. Brand-warm sign-off

Length: 80-150 words. Birthday emails should feel personal, not promotional.

### Step 2: Birthday SMS (on the day)

```
Happy birthday, [first name]! Your gift from [brand]: BIRTHDAY15 for 15% off
your order this week. [shortlink] Reply STOP to opt out.
```

### Optional step 3: Expiry reminder (1-2 days before code expires)

If the buyer wants it. Skip by default.

```
Last call on your birthday gift, [first name] - BIRTHDAY15 expires tomorrow.
[shortlink] Reply STOP to opt out.
```

---

## Segmentation considerations

- **Always filter out unsubscribed contacts**
- **Only send to SMS-opt-in subscribers for step 2**
- **Skip if the buyer recently purchased** (within 7 days of birthday) — feels redundant
- **For VIP customers**, optionally use a higher discount (20-25%) or a free-gift instead of percent off

---

## A/B test plan

1. **Subject line A/B** — gift-led vs warm-led
2. **Offer type** — % discount vs free shipping vs free gift with purchase
3. **Offer size** — 10% vs 15% vs 20%

---

## Common pitfalls

- **No birthday data** — flow doesn't trigger; many programs build this flow and forget to set up the data collection
- **Generic "happy birthday" with no offer** — most birthday emails need to give something or they're forgettable
- **Sending only on the actual day** — many subscribers don't open email on their birthday. The 7-days-before email gets opened.

## Performance benchmarks

- Email open rate: 50-65% (birthdays feel personal)
- Conversion rate: 5-12% of recipients
- Revenue contribution: 1-3% of program revenue (small but high warmth)
