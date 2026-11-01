---
name: email-flow-architect
description: >
  Builds Klaviyo-ready email and SMS automation flows for e-commerce stores. Covers 8 flow types:
  Welcome, Abandoned Cart, Post-Purchase, Browse Abandonment, Win-back, Birthday, Replenishment, and
  Back-in-Stock. Each flow includes message variants, send-timing logic, segmentation filters, and A/B
  test plans. Outputs a polished .docx brief plus Klaviyo-paste-ready .txt blocks for each email and
  SMS. Use this skill when the user mentions email flow, automation flow, Klaviyo flow, welcome
  series, abandoned cart, post-purchase, winback, browse abandonment, replenishment, back in stock,
  birthday email, 'set up my flows,' 'build me a welcome series,' or 'I need email automation.' Reads
  shared keyword and UGC hook caches for subject-line coordination with other skills.
---

# Email Flow Architect

Builds Klaviyo-ready email + SMS automation flows. 8 flow types, per-flow email + SMS variants, Klaviyo-paste-ready output.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Detect which flows to build.** Default to the 3 essentials; respect buyer overrides.
3. **Confirm channels.** Email + SMS by default; respect overrides.
4. **Gather context.** Shopify products + brand voice + audience + any existing flows.
5. **Read shared caches.** Keywords cache (for subject-line SEO), UGC hooks cache (for coordinated subject-line angles).
6. **Generate each flow.** Per-flow structure → per-email + per-SMS copy → send-timing logic → segmentation filters → A/B test plan.
7. **Render outputs.** `.docx` brief covering everything + Klaviyo-paste-ready blocks per email/SMS.
8. **Report back.** File paths, flows built, channels covered, total emails/SMS produced, deliverability check summary, next step.

---

## Step 1: First-run check

Look for `<plugin-root>/.config/the-ecommerce-seller.config.json`. If missing, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

---

## Step 2: Detect which flows to build

Eight flow types are supported:

| Flow | Trigger | Default email count | Default SMS count |
|---|---|---|---|
| **Welcome** | Newsletter signup | 5 | 2 |
| **Abandoned Cart** | Cart abandonment | 3 | 2 |
| **Post-Purchase** | Order placed | 4 | 2 |
| **Browse Abandonment** | Product viewed, not added | 2 | 1 |
| **Win-back** | No purchase in 60-180 days | 3 | 1 |
| **Birthday** | Birthday date (annual) | 1 | 1 |
| **Replenishment** | Consumable products, 30-90 days post-purchase | 2 | 1 |
| **Back-in-Stock** | Product restocked + customer on waitlist | 1 | 1 |

Detect from user language:

| Buyer says | Build |
|---|---|
| "set up my email program," "build my email flows," "I'm new to Klaviyo" | The 3 essentials (Welcome + Abandoned Cart + Post-Purchase) — the default |
| "build everything," "the whole program," "all flows" | All 8 |
| Names specific flows ("just Welcome and Abandoned Cart") | Only the named flows |
| Vague ("write me some email automation") | Default to 3 essentials |

Confirm out loud: "Building 3 flows: Welcome (5 emails + 2 SMS), Abandoned Cart (3+2), Post-Purchase (4+2). Want to add Browse Abandonment or Win-back?"

Each flow template lives in `templates/{flow-name}-flow.md`. Read the file for the flow(s) being built.

---

## Step 3: Confirm channels

**Email + SMS is the default.** Both for every flow.

Buyer overrides:
- "Email only" → skip SMS for this run
- "Just SMS" → email only for the essential parts (the SMS-supplementary flows like Back-in-Stock get full SMS treatment)
- "SMS only for abandoned cart" → that specific flow gets SMS; others stay email-only

Read `templates/email-craft.md` and `templates/sms-craft.md` for per-channel writing conventions.

---

## Step 4: Gather context

Same flexible input pattern as other skills. For email flows the skill needs:

- **From Shopify connector (when present):** product catalog, customer-segment counts (so the skill can recommend realistic segmentation thresholds), past order data (informs Replenishment timing per category), recent reviews (gold for the Post-Purchase email's review-request line)
- **From Klaviyo connector (when present):** existing flows the buyer has set up (so the skill doesn't duplicate or conflict), existing segments, brand template if customized
- **From config:** brand voice, audience, output folder, store URL
- **From buyer paste (always available):** what they want each flow to do, any specific offers (discount codes), brand-tone guardrails

If Shopify is missing, ask the buyer for: top 3-5 product categories, typical order value, typical purchase frequency. These inform the segmentation and timing.

If Klaviyo is missing, output Klaviyo-paste-ready blocks anyway — buyer can paste them into Klaviyo's email builder manually.

---

## Step 5: Read shared caches

Two shared caches enrich the output:

### Cache A: Keywords (read-only, from skill #2)

**Path:** `<plugin-root>/.cache/keywords/{product-identifier}.json`

Use `scripts/keyword_cache_reader.py`. Keywords influence subject lines for email flows that mention specific products (Abandoned Cart, Browse Abandonment, Post-Purchase). Subject lines benefit from search-friendly phrasing — "Your [keyword] is waiting" outperforms "Your cart is waiting" for branded-search subscribers.

### Cache B: UGC hooks (read-only, from shared cache)

**Path:** `<plugin-root>/.cache/ugc_hooks/{product-identifier}.json`

Use `scripts/ugc_hook_cache.py`. Reads the same hook archetypes used by skills #5 (ads) and #6 (creator briefs). The Welcome flow's hero email and the Abandoned Cart's recovery email can reuse the brand's tested hook angles — coordinating the "problem-aware" or "transformation" angle across ads, creator content, AND email.

When the caches are empty for this product, the skill generates fresh subject lines without coordination. The cache is enrichment, not requirement.

---

## Step 6: Generate each flow

For each flow being built:

1. **Read the flow's template file** in `templates/` for the canonical structure (email count, timing, segmentation pattern, subject-line patterns)
2. **Determine the segmentation** per email/SMS step (read `templates/segmentation-logic.md` for the algorithm)
3. **Write subject lines** using `templates/email-craft.md` rules + brand voice + relevant cached hooks
4. **Write preview text** (the post-subject preview line) — this is critical for open rate and frequently neglected
5. **Write email body copy** using the brand voice + flow-specific patterns
6. **Write SMS variants** using `templates/sms-craft.md` (160-char limits, TCPA compliance, opt-in handling)
7. **Specify send-timing logic** per step (immediately, 3 hours, 24 hours, 3 days, etc. — per flow template)
8. **Define A/B test plan** per flow (which subject lines / preview text / CTA buttons to test against each other)

The skill applies the buyer's brand voice consistently across all flows. Voice is the constant; the flow type and channel are the variables.

---

## Step 7: Render outputs

### Output 1: `.docx` flow brief

Use `scripts/render_flow_docx.py` and the `docx` skill. Structure:

```
[Brand name] — Email Flow Program Brief
Generated [date] · Brand: [brand_name]
Flows built: [list with email + SMS counts]
Total assets: [N emails + M SMS messages]
Keywords source: seo_cache | none
UGC hooks source: shared_cache | none

══════════════════════════════════════════════════
DELIVERABILITY CHECK
══════════════════════════════════════════════════
- DKIM / SPF / DMARC setup (Klaviyo requires)
- Sender domain warming notes (for new senders)
- Subject-line spam-trigger words flagged
- SMS opt-in confirmation present

══════════════════════════════════════════════════
FLOW 1: WELCOME
══════════════════════════════════════════════════
Trigger: subscribed to newsletter via [form]
Total: 5 emails + 2 SMS
Total duration: 14 days

[Per-step breakdown — see template for structure]

Step 1 (immediate, email): Welcome
  Subject: [...]
  Preview text: [...]
  Body: [...]
  A/B test: [subject line variant + winner-selection criteria]
  Segmentation: all new subscribers

Step 2 (3 hours later, SMS): Welcome SMS
  Body (160 chars): [...]
  Segmentation: subscribers who opted into SMS

[...etc through all steps...]

[Repeat for each flow being built]

══════════════════════════════════════════════════
HOW TO BUILD IN KLAVIYO
══════════════════════════════════════════════════
Step-by-step: create the flow, paste each email's block, set the timing
and trigger conditions.
```

Save to `config.output_folder` with filename `{brand-slug}_email-flow-program_{date}.docx`.

### Output 2: Klaviyo-paste-ready blocks

Use `scripts/render_klaviyo_blocks.py`. Produces a directory of plain-text files, one per email or SMS, structured exactly the way Klaviyo's email builder expects:

```
{output_folder}/klaviyo_blocks/
├── welcome_01_email.txt
├── welcome_02_email.txt
├── welcome_03_email.txt
├── welcome_04_email.txt
├── welcome_05_email.txt
├── welcome_sms_01.txt
├── welcome_sms_02.txt
├── abandoned_cart_01_email.txt
├── ... etc
```

Each `.txt` file's content:

```
SUBJECT LINE: [subject line for the email]
PREVIEW TEXT: [preview text]
---
[HTML or plain-text body]
```

For SMS files:
```
SMS BODY (XX/160 chars):
[message text]
LINK: [optional shortened URL]
```

Buyer opens each file → copies the subject + preview + body into Klaviyo's email editor for that step. Read `templates/klaviyo-paste-conventions.md` for the exact field-mapping.

---

## Step 8: Report back

Tell the buyer:
1. Where both outputs are (`.docx` + Klaviyo blocks folder)
2. Flow count + email/SMS count summary
3. Whether subject lines used the keyword cache + UGC hook cache (coordination signals)
4. Deliverability check summary (pass/flag count)
5. One suggested next step:
   - If buyer didn't ask for the optional flows: "Want to add Browse Abandonment + Win-back next? They typically lift program revenue 20-30%."
   - If buyer hasn't run skill #5 / #6 yet: "Coordination tip — when you run the Ad Creative Generator and UGC Creator Brief Writer, subject lines in future runs will sync with your ad and creator hooks."
   - If Shopify isn't connected: "Connect Shopify and re-run to get segmentation that uses your actual customer data (cart values, purchase recency)."

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Shopify | Skill uses generic segmentation thresholds; flags that real customer-data thresholds would improve targeting |
| Klaviyo | Skill still produces all outputs (paste-ready, not API-uploaded); flags that direct API upload is available if connector added |
| Keywords cache | Skill generates subject lines without keyword integration |
| UGC hooks cache | Skill generates subject lines without ad/creator coordination |

The skill always produces complete output — connectors enrich; they're not required.

---

## Edge cases

- **Buyer has existing Klaviyo flows and wants a refresh, not a new build**: pull the existing flow names + step counts (via Klaviyo connector if available, or buyer paste). Audit which flows are working and which aren't (based on send/open/click rates if buyer shares them). Recommend replacements per email. Note in the brief that the buyer should pause old emails before activating new ones — running two versions simultaneously hurts deliverability.
- **Buyer is in a regulated category** (supplements, financial, CBD): tighter compliance. Email needs CAN-SPAM compliance (already standard) + category-specific health-claim restrictions in the body. SMS needs TCPA compliance with explicit opt-in language.
- **Buyer wants flows in a non-English language**: write the copy in the target language. Subject lines and previews especially benefit from native-speaker authoring (literal translation often kills open rates).
- **Buyer has fewer than 100 subscribers**: flag that flow performance is noisy below 100. Some flows (Win-back, Birthday, Replenishment) shouldn't be activated until the buyer has at least 6 months of customer data. Default to the 3 essentials only and flag the rest as "build later when your list reaches 1,000+."
- **Buyer specifies a discount/promo code**: include it in the relevant flow emails (typically Welcome step 1 + Abandoned Cart step 2 + Win-back step 1). Don't recycle the same code across flows — different codes per flow let the buyer measure each flow's revenue contribution.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema
- **8 per-flow templates** (one per flow type):
  - `templates/welcome-flow.md`
  - `templates/abandoned-cart-flow.md`
  - `templates/post-purchase-flow.md`
  - `templates/browse-abandonment-flow.md`
  - `templates/winback-flow.md`
  - `templates/birthday-flow.md`
  - `templates/replenishment-flow.md`
  - `templates/back-in-stock-flow.md`
- **Craft + conventions templates:**
  - `templates/email-craft.md` — subject lines, preview text, body structure, deliverability
  - `templates/sms-craft.md` — 160-char limits, TCPA, opt-in, link handling
  - `templates/klaviyo-paste-conventions.md` — field-mapping for Klaviyo's builder
  - `templates/segmentation-logic.md` — audience filters per flow
- **Scripts:**
  - `scripts/config_loader.py` — shared
  - `scripts/keyword_cache_reader.py` — shared from skills #3/#4/#5
  - `scripts/ugc_hook_cache.py` — read-only shared from skills #5/#6
  - `scripts/render_flow_docx.py` — .docx flow brief renderer
  - `scripts/render_klaviyo_blocks.py` — per-email/per-SMS paste-ready file renderer
- **Examples:**
  - `examples/welcome-flow-example.md`
  - `examples/abandoned-cart-flow-example.md`
  - `examples/full-program-example.md`
