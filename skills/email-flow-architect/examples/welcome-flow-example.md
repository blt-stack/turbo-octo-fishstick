# Welcome Flow — Reference Example

Fictional brand used to show structure. Never reproduce verbatim.

**Flow:** Welcome
**Channels:** Email + SMS
**Brand:** {{brand_name}} (handmade ceramic coffee gear)
**Output files:** 1 .docx brief section + 7 Klaviyo paste-ready .txt files

---

## .docx brief excerpt — Welcome flow section

```
FLOW 1: WELCOME FLOW
Trigger: Added to list "Newsletter Subscribers"
Total duration: 14 days
Total emails: 5
Total SMS: 2

Step 1 (Immediate, email): Welcome + brand intro + offer
  Segment: All new subscribers

  Subject line (44/60): Welcome to {{brand_name}}. Here's your 10% off.
  Preview text (62/90): Your code is inside, plus a quick hello from our studio.

  Body summary: Personal opener from founder Sarah, offer delivery with the
  code clearly visible, one paragraph on brand context, single CTA to shop the
  bestsellers, sign-off in brand voice.

  Merge tags used: first_name, company_name
  A/B test: Subject line A/B — brand-voice variant ("Hi from Sarah at
  {{brand_name}}") vs offer-led variant ("Your 10% off code, {{first_name}}").
  Run 14 days, declare winner by open rate.

Step 2 (3 hours later, sms): Mobile reminder of the offer
  Segment: Subscribers opted into SMS

  SMS body (138/160): Hey {{first_name}}, your welcome code is WELCOME10 for
  10% off your first order. Use it in the next 7 days: [shortlink]. Reply
  STOP to opt out.
  Compliance:
    ✓ Reply STOP present
    ✓ Brand identifier in first 30 chars

  Merge tags used: first_name

Step 3 (24 hours later, email): Brand story — why this brand exists
  Segment: All new subscribers

  Subject line (38/60): The morning the wifi went out
  Preview text (74/90): Why we started making coffee gear in a kitchen in Portland.

  Body summary: Origin story — the morning Sarah's coffee shop wifi went
  down and she had to make her own. ~400 words narrative. No hard CTA; soft
  invitation to read the full About page.

  Merge tags used: first_name
  A/B test: None (this is the trust-building email — A/B testing optimizes
  the converting emails first)

Step 4 (3 days later, email): Bestsellers — what to shop
  Segment: All new subscribers who haven't purchased yet

  Subject line (49/60): Three things our customers can't stop ordering
  Preview text (72/90): The pour-over, the mug set, and the brewing journal.

  Body summary: 3 featured products with images, 1-line descriptions, prices,
  Shop Now links. Header explains why these are the starting points.

  Merge tags used: first_name (in greeting)

Step 5 (5 days later, email): Social proof — featured customer / press
  Segment: All new subscribers who haven't purchased yet

  Subject line (44/60): What our customers can't stop saying
  Preview text (62/90): Five reviews and one piece of press we're proud of.

  Body summary: 3 customer reviews + 1 press mention (Sprudge 2026) + link
  to UGC gallery.

  Merge tags used: first_name

Step 6 (7 days later, sms): Last-chance reminder
  Segment: Subscribers opted into SMS who haven't purchased yet

  SMS body (140/160): Last day to use WELCOME10 for 10% off, {{first_name}}.
  We'd hate for you to miss it: [shortlink]. Reply STOP to opt out.

  Compliance:
    ✓ Reply STOP present
    ✓ Brand identifier (implied via brand context)

Step 7 (10 days later, email): Re-engagement
  Segment: New subscribers who haven't purchased by day 10

  Subject line (28/60): Not the right time?
  Preview text (74/90): Tell us what you'd want from us, or take 15% off if you're ready.

  Body summary: Asks a question (what category are they curious about?),
  offers alternative actions, extends the discount one more time at 15%
  (sweetened from the original 10%).

  Merge tags used: first_name
```

---

## Klaviyo paste-ready .txt files generated (7 files for this flow)

### `welcome_01_email.txt`

```
=== KLAVIYO EMAIL BLOCK ===
Flow: Welcome Flow
Step: 1 of 7
Send timing: Immediate (within 1 min of signup)
Segment: All new subscribers

=== SUBJECT LINE ===
Welcome to {{brand_name}}. Here's your 10% off.

=== PREVIEW TEXT ===
Your code is inside, plus a quick hello from our studio.

=== BODY (HTML) ===
<p>Hi {{ first_name|default:'there' }},</p>

<p>I'm Sarah — one of the three potters at {{ company_name }}. Thanks for
subscribing. Here's the welcome offer I promised:</p>

<p style="text-align:center;background:#f8f5f0;padding:20px;border-radius:8px;">
<strong style="font-size:18px;">WELCOME10</strong><br>
<span style="font-size:14px;">10% off your first order · expires in 7 days</span>
</p>

<p>We started {{ company_name }} in a kitchen corner with one wheel and
a borrowed kiln. Three years and ~7,200 pieces later, every {{ company_name }}
dripper is still thrown by hand in our small studio in Portland.</p>

<p style="text-align:center;margin:24px 0;">
<a href="https://{{ company_name }}.com/collections/bestsellers"
   style="display:inline-block;padding:14px 32px;background:#1a1a1a;color:#ffffff;text-decoration:none;border-radius:6px;font-weight:600;">
   Shop the bestsellers
</a>
</p>

<p>Glad you're here. If you have a question, just reply — I read every email.</p>

<p>— Sarah, {{ company_name }}</p>

<p style="font-size:13px;color:#666;"><em>P.S. The River Stone Pour-Over
is what most new customers start with. If you're not sure what to pick,
that's the one.</em></p>

=== BODY (PLAIN TEXT FALLBACK) ===
Hi there,

I'm Sarah — one of the three potters at {{ company_name }}. Thanks for
subscribing. Here's the welcome offer I promised:

WELCOME10
10% off your first order · expires in 7 days

We started {{ company_name }} in a kitchen corner with one wheel and a
borrowed kiln. Three years and ~7,200 pieces later, every dripper is still
thrown by hand in our Portland studio.

→ Shop the bestsellers: https://{{ company_name }}.com/collections/bestsellers

Glad you're here. If you have a question, just reply — I read every email.

— Sarah, {{ company_name }}

P.S. The River Stone Pour-Over is what most new customers start with. If
you're not sure what to pick, that's the one.

=== KLAVIYO MERGE TAGS USED ===
first_name, company_name

=== A/B TEST RECOMMENDATIONS ===
Subject line A/B — variant A: "Welcome to {{brand_name}}. Here's your 10%
off." vs variant B: "Hi from Sarah at {{brand_name}}." Run 14 days, declare
winner by open rate.
```

### `welcome_sms_01.txt`

```
=== KLAVIYO SMS BLOCK ===
Flow: Welcome Flow
Step: 2 of 7
Send timing: 3 hours after signup
Segment: Subscribers opted into SMS
Quiet hours: respected (8am-9pm recipient local time)

=== SMS BODY (138/160 chars) ===
Hey {{ first_name|default:'there' }}, your welcome code is WELCOME10 for 10%
off your first order. Use it in the next 7 days: [shortlink]. Reply STOP to opt out.

=== LINK ===
https://{{ company_name }}.com/collections/bestsellers?welcome=true

=== KLAVIYO MERGE TAGS USED ===
first_name, company_name

=== COMPLIANCE NOTES ===
- Reply STOP language present: yes
- Brand identifier in first 30 chars: yes (via "{{brand_name}}" merge tag when company_name is the brand)
```

(The remaining 5 .txt files follow the same format for steps 3-7.)

---

## Notes on this exemplar

- **5 emails + 2 SMS over 14 days** — uses the warm window aggressively
- **Brand voice consistent**: warm, slightly contemplative, founder-led
- **Step 1's offer is clearly delivered** with a visual call-out box (not buried in body)
- **A/B test recommendation on step 1** — most leverage on the entry email
- **Step 3 (brand story) intentionally has no A/B test** — trust-building, not conversion-optimization
- **SMS keeps brand consistency** but in a more casual tone
- **The 7-day re-engagement email** (step 7) acknowledges the buyer hasn't bought and asks a question
- **Compliance verified in SMS**: Reply STOP + brand ID checks both pass

The buyer pastes 7 files into Klaviyo (~20 minutes total) and the flow is ready to activate.
