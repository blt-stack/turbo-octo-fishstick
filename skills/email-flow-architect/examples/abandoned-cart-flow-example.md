# Abandoned Cart Flow — Reference Example

Fictional brand used to show structure. Never reproduce verbatim.

**Flow:** Abandoned Cart
**Channels:** Email + SMS
**Brand:** {{brand_name}} (handmade ceramic coffee gear)
**Output files:** 1 .docx brief section + 5 Klaviyo paste-ready .txt files

---

## .docx brief excerpt — Abandoned Cart flow section

```
FLOW 2: ABANDONED CART
Trigger: Started Checkout event fired in past hour AND no Placed Order event for that checkout
Total duration: ~72 hours
Total emails: 3
Total SMS: 2

Step 1 (1 hour after abandonment, email): Gentle reminder + cart contents
  Segment: All carts that triggered the flow

  Subject line (28/60): You left something behind
  Preview text (62/90): Your cart is still here. We saved it for the next 24 hours.

  Body summary: Friendly opener, dynamic cart block (Klaviyo pulls cart items
  from the checkout), single "Complete your order" CTA, soft reassurance about
  the brand's returns policy.

  Merge tags used: first_name, event.cart_items, event.checkout_url
  A/B test: Subject line A/B — "You left something behind" vs "Still thinking
  it over?" Run 14 days, declare winner by click rate.

Step 2 (4 hours after abandonment, sms): Mobile reminder
  Segment: SMS-opted-in subscribers in flow

  SMS body (134/160): Hey {{first_name}}, your cart at {{brand_name}} is
  still here: [shortlink]. We'll hold it for the next 24 hours. Reply STOP to opt out.

  Compliance:
    ✓ Reply STOP present
    ✓ Brand identifier in first 30 chars

Step 3 (24 hours after abandonment, email): Address the friction
  Segment: All carts that haven't converted

  Subject line (18/60): About shipping...
  Preview text (74/90): A few things we make easy that might be holding you back.

  Body summary: Friction-addressing — addresses shipping (free over $50), returns
  (30-day money-back, no questions), and brand-trust (1,247 reviews). Cart contents
  reminder, CTA to complete.

  Merge tags used: first_name, event.cart_items, event.checkout_url

Step 4 (48 hours after abandonment, sms): Last reminder + discount
  Segment: SMS-opted-in subscribers in flow whose cart value > $30

  SMS body (146/160): Last reminder — your {{brand_name}} cart, plus 10% off:
  SAVE10 (expires in 24 hrs). [shortlink]. Reply STOP to opt out.

  Compliance:
    ✓ Reply STOP present
    ✓ Brand identifier in first 30 chars

Step 5 (72 hours after abandonment, email): Final push
  Segment: All carts that haven't converted

  Subject line (28/60): Last chance — your cart
  Preview text (66/90): SAVE10 for 10% off · expires tonight · ships in 2 days.

  Body summary: Acknowledges it's the last email about this cart. Restates the
  offer, cart contents, one customer review (newly added social-proof element
  to differentiate from earlier emails), final CTA.

  Merge tags used: first_name, event.cart_items, event.checkout_url
  A/B test: Discount on step 4-5 (SAVE10) vs no discount. Run 21 days.
```

---

## Klaviyo paste-ready .txt files generated (5 files for this flow)

### `abandoned_cart_01_email.txt` (the highest-converting step)

```
=== KLAVIYO EMAIL BLOCK ===
Flow: Abandoned Cart
Step: 1 of 5
Send timing: 1 hour after Started Checkout
Segment: All carts that triggered the flow

=== SUBJECT LINE ===
You left something behind

=== PREVIEW TEXT ===
Your cart is still here. We saved it for the next 24 hours.

=== BODY (HTML) ===
<p>Hi {{ first_name|default:'there' }},</p>

<p>You added something to your cart but didn't quite finish. No worries — we
saved it for you:</p>

{% for item in event.cart_items %}
<table style="width:100%;border-collapse:collapse;margin:16px 0;">
<tr>
<td style="width:80px;padding:8px;">
<img src="{{ item.product_image }}" alt="{{ item.product_name }}" style="width:80px;height:80px;object-fit:cover;border-radius:4px;">
</td>
<td style="padding:8px;vertical-align:top;">
<strong>{{ item.product_name }}</strong><br>
<span style="color:#666;">${{ item.unit_price }}</span>
</td>
</tr>
</table>
{% endfor %}

<p style="text-align:center;margin:24px 0;">
<a href="{{ event.checkout_url }}" style="display:inline-block;padding:14px 32px;background:#1a1a1a;color:#ffffff;text-decoration:none;border-radius:6px;font-weight:600;">
Complete your order
</a>
</p>

<p>We'll hold it for the next 24 hours. Free shipping over $50 and 30-day
returns — if anything's holding you back, just reply.</p>

<p>— {{ company_name }}</p>

=== BODY (PLAIN TEXT FALLBACK) ===
Hi there,

You added something to your cart but didn't quite finish. No worries — we
saved it for you:

{% for item in event.cart_items %}
{{ item.product_name }} — ${{ item.unit_price }}
{% endfor %}

→ Complete your order: {{ event.checkout_url }}

We'll hold it for the next 24 hours. Free shipping over $50 and 30-day
returns — if anything's holding you back, just reply.

— {{ company_name }}

=== KLAVIYO MERGE TAGS USED ===
first_name, event.cart_items, event.checkout_url, company_name

=== A/B TEST RECOMMENDATIONS ===
Subject line A/B — variant A: "You left something behind" vs variant B:
"Still thinking it over?" Run 14 days, declare winner by click rate (not
open rate — the email's job is to drive cart return, not just opens).
```

### `abandoned_cart_sms_01.txt`

```
=== KLAVIYO SMS BLOCK ===
Flow: Abandoned Cart
Step: 2 of 5
Send timing: 4 hours after Started Checkout
Segment: SMS-opted-in subscribers in flow
Quiet hours: respected (8am-9pm recipient local time)

=== SMS BODY (134/160 chars) ===
Hey {{ first_name|default:'there' }}, your cart at {{ company_name }} is still
here: [shortlink]. We'll hold it for the next 24 hours. Reply STOP to opt out.

=== LINK ===
{{ event.checkout_url }}

=== KLAVIYO MERGE TAGS USED ===
first_name, company_name, event.checkout_url

=== COMPLIANCE NOTES ===
- Reply STOP language present: yes
- Brand identifier in first 30 chars: yes (via {{ company_name }} merge tag)
```

(Remaining 3 .txt files follow the same format for steps 3-5.)

---

## Notes on this exemplar

- **Step 1 is intentionally short** (~120 words) — most recovered carts come from this step, and the customer was likely just interrupted
- **No discount in step 1** — discount comes at step 4 only, after the friction-addressing email
- **Step 3 addresses likely friction directly** (shipping, returns, trust) rather than just nagging
- **Step 4's discount is segmented by cart value** ($30 minimum to qualify for the discount) — protects margin on small carts
- **Step 5 uses different social proof** (a customer review) than earlier steps — keeps the final email feeling fresh
- **A/B test recommendation focuses on click rate** for step 1 — the right metric for cart-recovery emails (not opens)
- **Dynamic cart block** uses Klaviyo's `{% for %}` template syntax to pull live cart items
- **SMS character count is well under limit** (134/160) — leaves room for the link expansion

Buyer pastes 5 files into Klaviyo and the flow is ready (~15 minutes total).
