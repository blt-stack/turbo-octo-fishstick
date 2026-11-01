# Klaviyo Paste Conventions

The Klaviyo-paste-ready blocks are the second output deliverable. They're plain-text `.txt` files structured exactly as Klaviyo's email + SMS builders expect, so the buyer copies one file's contents into one Klaviyo email and is done — no rebuilding, no reformatting.

This file defines the exact field-mapping the renderer follows.

---

## Email block format

One `.txt` file per email step in a flow. File naming pattern:

```
{flow-name}_{step-number}_email.txt
```

Examples:
- `welcome_01_email.txt`
- `abandoned_cart_03_email.txt`
- `post_purchase_04_email.txt`

### Email file structure

Each `.txt` file contains exactly four labeled sections:

```
=== KLAVIYO EMAIL BLOCK ===
Flow: [flow name]
Step: [step number] of [total steps]
Send timing: [when this step fires after the trigger]
Segment: [audience filter description, if applicable]

=== SUBJECT LINE ===
[The subject line copy — paste this into Klaviyo's Subject field]

=== PREVIEW TEXT ===
[The preview text copy — paste this into Klaviyo's Preview Text field]

=== BODY (HTML) ===
[The body copy with basic HTML — paste this into Klaviyo's email body editor]

=== BODY (PLAIN TEXT FALLBACK) ===
[The body copy in plain text — Klaviyo auto-generates this from HTML but
the buyer can paste this version for explicit control]

=== KLAVIYO MERGE TAGS USED ===
[Comma-separated list of merge tags used in body and subject so the buyer
can verify they're set up — e.g., first_name, product_name, checkout_url]

=== A/B TEST RECOMMENDATIONS ===
[What to test on this email and how — see per-flow template]
```

The renderer writes this exact structure for every email.

### Body HTML format

The HTML body uses Klaviyo-friendly markup:

```html
<p>Hi {{ first_name|default:'there' }},</p>

<p>You left something behind. We saved it for you:</p>

<p><strong>{{ event.cart_items.0.product_name }}</strong><br>
${{ event.cart_items.0.unit_price }}</p>

<p style="text-align:center;margin:24px 0;">
  <a href="{{ event.checkout_url }}" style="display:inline-block;padding:14px 32px;background:#1a1a1a;color:#ffffff;text-decoration:none;border-radius:6px;font-weight:600;">Complete your order</a>
</p>

<p>We'll hold it for the next 24 hours. If you have questions, just reply
to this email.</p>

<p>— {{ company_name }}</p>
```

Conventions:
- Inline styles only (no `<style>` blocks — many email clients strip them)
- `<p>` tags for paragraphs (not `<div>` — better client compatibility)
- Buttons use `<a>` styled as buttons (not actual `<button>` — better client support)
- Image references use absolute URLs (`<img src="https://...">`, not relative paths)
- Klaviyo merge tags use the `{{ }}` syntax with default filters where helpful

### Plain-text fallback

Klaviyo auto-generates a plain-text version of every email but the auto-version can be ugly. The renderer provides an explicit plain-text version that mirrors the HTML's structure:

```
Hi there,

You left something behind. We saved it for you:

[Product name]
$[price]

→ Complete your order: [checkout URL]

We'll hold it for the next 24 hours. If you have questions, just reply
to this email.

— [Brand name]
```

Buyer pastes this into Klaviyo's "Plain Text" tab if they want explicit control.

---

## SMS block format

One `.txt` file per SMS step. File naming:

```
{flow-name}_sms_{step-number}.txt
```

Examples:
- `welcome_sms_01.txt`
- `abandoned_cart_sms_02.txt`

### SMS file structure

```
=== KLAVIYO SMS BLOCK ===
Flow: [flow name]
Step: [step number] of [total steps]
Send timing: [when this step fires after the trigger]
Segment: [audience filter — usually "subscribers opted in to SMS"]
Quiet hours: respected (8am-9pm recipient local time)

=== SMS BODY (XX/160 chars) ===
[The full SMS message text — paste into Klaviyo's SMS field]

=== LINK ===
[The destination URL — Klaviyo auto-shortens this when sending]

=== KLAVIYO MERGE TAGS USED ===
[Comma-separated list]

=== COMPLIANCE NOTES ===
- Reply STOP language present: yes/no
- Brand identifier in first 30 chars: yes/no
- Quiet hours setting required in flow config: yes
```

The compliance section explicitly verifies the TCPA-required elements for the buyer's records.

---

## How the buyer uses these files

For each flow:

1. In Klaviyo, navigate to Flows → Create Flow → name it after the flow (e.g., "Welcome — Newsletter Signup")
2. Set the trigger per the flow brief (e.g., "Added to list: Newsletter Subscribers")
3. For each step in the flow:
   - In Klaviyo, add a flow action (Email or SMS) with the timing specified in the `.txt` file
   - Open the matching `.txt` file from the output folder
   - Copy the Subject Line section → paste into Klaviyo's Subject field
   - Copy the Preview Text section → paste into Klaviyo's Preview Text field
   - Copy the Body (HTML) section → paste into Klaviyo's email body editor (choose Source HTML mode)
   - Verify merge tags are recognized (Klaviyo shows them as colored chips)
   - Optionally paste the Plain Text Fallback into the Plain Text tab
   - Set the A/B test if recommended
4. Repeat per step
5. Activate the flow when all steps are configured

Time per flow: ~15-30 minutes once the buyer has the .txt files. Without the .txt files, building from scratch takes 90+ minutes per flow.

---

## Klaviyo-specific gotchas

### Merge tag syntax

Klaviyo uses Django-style template tags: `{{ variable }}`. The skill always uses this exact syntax.

For default values: `{{ first_name|default:'there' }}` — note the single quotes inside default.

For nested attributes: `{{ event.cart_items.0.product_name }}` — note the period separator.

### Event variables

For Abandoned Cart / Browse Abandonment / Post-Purchase, Klaviyo uses different variable names depending on whether the trigger is a metric (event) or a profile attribute. The skill uses the most common:

- Abandoned Cart trigger: `event.cart_items`, `event.cart_total`, `event.checkout_url`
- Browse Abandonment trigger: `event.product_id`, `event.product_name`, `event.product_url`
- Placed Order trigger: `event.items`, `event.order_id`, `event.total`

If the buyer's Klaviyo account uses custom event names (e.g., custom integrations), the skill flags this in the brief and asks the buyer to substitute their own variable names.

### Image hosting

Klaviyo can host images uploaded to the email editor, OR images can be hosted at the buyer's own URL. The skill uses placeholder image references (`https://YOUR-IMAGE-CDN.com/path-to-image.jpg`) and notes in each email's section that the buyer needs to upload product images or use their CDN.

For Shopify-integrated accounts, Klaviyo's product blocks auto-fetch the product image from the Shopify catalog. The skill uses these blocks for Abandoned Cart / Browse Abandonment / Post-Purchase order-recap emails to avoid manual image work.

### Sender configuration

Each email needs a sender name + reply-to email. The skill defaults to:

- Sender name: `[brand_name]` (e.g., "{{brand_name}}")
- Reply-to: a real, monitored email (NOT no-reply@... — that hurts deliverability and brand)

The buyer configures sender info once per Klaviyo account; the skill doesn't re-specify per-email.

---

## What's not in the paste blocks

The .txt files don't include:

- **Visual design** (colors, fonts beyond inline styles, branded headers/footers) — buyer applies their Klaviyo template
- **Triggering logic** (when the flow fires) — buyer configures the trigger in Klaviyo's flow builder per the brief's "Trigger" specification
- **Segmentation filters** (audience conditions) — buyer applies these in the flow's segment settings per the brief's segmentation notes
- **A/B test configuration** (variant percentages, winner-selection criteria) — buyer sets these in Klaviyo's A/B test panel per the brief's recommendations

These are all in the .docx brief but not duplicated in the .txt paste blocks. The .txt is just the content.
