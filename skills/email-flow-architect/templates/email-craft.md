# Email Craft — Subject Lines, Preview Text, Body, Deliverability

The mechanics of writing emails that get opened, read, and converted. Per-flow templates handle the strategic copy; this file handles the craft fundamentals every email needs.

---

## Subject lines

The single most important element. Subject lines determine open rate (which gates click rate, which gates conversion). A 5% improvement in subject line performance compounds across every other metric.

### Length

Optimal: **30-50 characters**. Mobile email clients (where 60-70% of opens happen) typically show 30-40 characters in the inbox preview before truncating.

Hard cap: 60 characters. Past 60, mobile shows "..." mid-word.

### What works

- **Specificity over vagueness**: "Your $400 mistake fixer" beats "Special offer inside"
- **Curiosity over urgency**: "Three things we learned about brewing" beats "Last chance — 24 hours!"
- **Personal feel over corporate**: "Hi from Sarah at [brand]" beats "Welcome to [brand]"
- **Punctuation, sparingly**: one em-dash or colon works; multiple punctuation marks read as spammy
- **Sentence-case capitalization**: "Your cart is still here" beats "YOUR CART IS STILL HERE" (caps trigger spam filters)
- **Real questions (occasionally)**: "Need to talk through sizing?" gets opens by inviting reply
- **Emoji, very sparingly**: 1 emoji at the beginning or end can lift open rates 5-10%; 2+ emojis read as promotional

### What kills subject lines (spam-trigger words to avoid)

These words reduce inbox placement OR reduce opens even when delivered:

| Category | Words to minimize |
|---|---|
| Urgency | "Hurry," "Now," "Limited time," "Don't miss" |
| Money | "Cash," "Earn $," "Make money," "Save big" |
| Spam classics | "Free!!", "100% off," "Click here," "Act now" |
| ALL CAPS | Any word ALL CAPS in subject line |
| Multiple punctuation | "Sale!!!", "WOW!!!" |
| Misleading | "RE:", "FWD:" when the email isn't actually a reply or forward |

The skill auto-flags subject lines containing these patterns and rewrites.

### Subject-line patterns per flow archetype

| Archetype | Pattern |
|---|---|
| Welcome (step 1) | "Welcome to [brand]. Here's your [thing]." OR "Hi from [founder name]." |
| Welcome (later steps) | Brand-story or category-focused |
| Abandoned Cart (early) | "You left something behind" OR "Still thinking it over?" |
| Abandoned Cart (late) | "Last chance: your cart + [discount]" |
| Post-Purchase (order confirm) | "Order confirmed — thanks, [first name]" |
| Post-Purchase (engagement) | "How's the [product] treating you?" |
| Post-Purchase (review request) | "Two weeks with your [product]. Quick review?" |
| Browse Abandonment | "Still thinking about [product]?" |
| Win-back (early) | "It's been a while — here's what's new" |
| Win-back (late) | "Last call — and we'll let you settle" |
| Birthday | "Birthday week is coming, [first name]" |
| Back-in-stock | "[Product] is back in stock — yours if you want it" |

---

## Preview text

The post-subject text that shows in the inbox. Most senders neglect this — it gets auto-populated by the email's first line, which is usually "View this email in your browser" or "Hi [first name]," (forgettable).

### Length

Optimal: **35-90 characters**. Most clients show 50-75 chars.

### What it does

The preview text continues the subject line's argument. A subject + preview combo is essentially a two-line ad in the inbox. Strong combos lift open rates 20-30% over subject-line-only optimization.

### Patterns

- **Subject sets up; preview pays off**: subject = "Your cart is still here" / preview = "We'll hold it for 24 more hours — and your [discount] is inside."
- **Preview adds the offer**: subject = "Welcome to [brand]" / preview = "Your 10% off code is in here."
- **Preview asks a question**: subject = "Three things about brewing" / preview = "Which one are you doing wrong?"
- **Preview foreshadows specificity**: subject = "[Product] reviews" / preview = "12,000+ five-star reviews, plus one customer story you should hear."

### Common pitfall

Forgetting to set preview text manually. Klaviyo defaults to the first line of the email body, which is rarely what the buyer would choose. The skill always specifies preview text explicitly in the brief and the Klaviyo-paste block.

---

## Body copy structure

### Length per email type

- Welcome step 1: 150-300 words
- Welcome story: 300-500 words
- Welcome bestsellers: 100-200 words + product blocks
- Abandoned Cart step 1: 100-200 words
- Abandoned Cart step 3 (friction): 150-250 words
- Post-Purchase order confirm: 150-300 words + dynamic order block
- Post-Purchase engagement check-in: 100-200 words
- Post-Purchase review request: 100-200 words
- Browse Abandonment: 100-200 words
- Win-back step 1: 100-200 words
- Birthday: 80-150 words
- Replenishment: 100-150 words
- Back-in-stock: 80-150 words

Longer emails are NOT better. Most subscribers skim. Long emails (500+ words) work for brand-story content and Win-back step 1 only.

### Structure pattern

```
1. Hook / personal opener (1-2 sentences)
2. The main content (2-4 short paragraphs OR a structured block)
3. The CTA (one clear button or link, plus optional secondary link)
4. Sign-off (brand voice, founder name when appropriate)
5. Postscript / P.S. (often the second-most-read line — use it for the most important benefit not yet mentioned)
```

### What works

- **Short paragraphs** (1-3 sentences each)
- **One clear CTA per email** — too many CTAs paralyze
- **Founder voice when possible** — "Hi, I'm Sarah" outperforms anonymous brand voice for small brands
- **Specific over vague** — "10-12 oz cup, ready in 3 minutes" beats "perfect cup of coffee"
- **The P.S. line** — historically high engagement; use it for a key benefit or a soft second CTA

### What kills body copy

- Walls of text (one giant paragraph)
- Multiple competing CTAs in one email
- Generic openers ("We hope this email finds you well")
- Branded image headers larger than the content (mobile readers see the header and scroll past)
- All-image emails (high spam risk, inaccessible)

---

## CTA design

### Button copy

Action-led, specific to the offer:

| Generic (avoid) | Specific (better) |
|---|---|
| Click here | Shop the pour-over |
| Learn more | See the brewing guide |
| Buy now | Get yours |
| Submit | Save my spot |
| Sign up | Join the waitlist |

### Button styling guidance

(For the Klaviyo paste-ready blocks — buyer applies in the editor)

- Full-width on mobile (`width: 100%` for sub-600px viewports)
- Minimum tappable area 44x44 pixels
- High color contrast (button background vs surrounding white)
- Single button per primary section; secondary actions as small text links

---

## Personalization

Klaviyo's merge tags let the skill personalize emails. Common useful tags:

- `{{ first_name|default:'there' }}` — greets by first name when known
- `{{ product_name }}` — for Abandoned Cart / Browse Abandonment
- `{{ event.checkout_url }}` — for cart-recovery CTAs
- `{{ order.items|each }}` — for Post-Purchase order recap
- `{{ subscriber_signup_form_name }}` — for context-aware Welcome

The skill always uses the `|default:'there'` filter on `first_name` so a missing name doesn't render as "Hi ," (which signals "this is automated").

---

## Deliverability checklist

Before each flow goes live, verify:

### Domain authentication
- **DKIM** record set up at the buyer's domain DNS
- **SPF** record updated to include Klaviyo's sending IP
- **DMARC** record set with at least p=none (or stricter)
- **Custom sender domain** configured in Klaviyo (instead of klaviyo-shared)

Without proper authentication, emails go to spam at higher rates and the buyer's domain reputation tanks.

### Content checks
- No spam-trigger words in subject lines
- Image-to-text ratio below 50% (heavy image emails get filtered)
- All images have alt text (accessibility + image-blocker fallback)
- Unsubscribe link visible in footer (CAN-SPAM requirement)
- Sender name and reply-to address set correctly
- Physical mailing address in footer (CAN-SPAM requirement)

The skill's compliance check flags any of these that are missing or misconfigured.

### Sender reputation
- Warm new sending domains gradually (start with the most-engaged segments, expand outward over 14-30 days)
- Don't blast a cold list — opening rate signals to Gmail/Outlook tell the inbox provider whether to send the brand to spam
- Re-engage or remove inactive subscribers periodically

These are program-level recommendations, not per-flow — but the skill flags them in the .docx brief so the buyer knows.

---

## Mobile considerations

- 60-70% of opens happen on mobile
- Subject + preview combo show on mobile inbox listings
- Single column layout (don't try to be desktop-only fancy)
- Tap targets at least 44x44 pixels
- Body font size at least 14px
- Avoid horizontal scrolling at all costs
- Test the email on iPhone and Android before activating any flow
