# Full Email Program — Reference Example

Shows what gets produced when the buyer asks "build my whole email program" — all 8 flows in one run.

**Brand:** {{brand_name}}
**Buyer request:** "Build my whole email program for Klaviyo — email + SMS"

---

## Output summary

```
{{brand_name}} — Email Flow Program Brief
Generated 2026-05-22 · Flows: welcome, abandoned_cart, post_purchase, browse_abandonment, winback, birthday, replenishment, back_in_stock · Channels: email, sms
Total assets: 21 emails + 11 SMS = 32 paste-ready files
Keywords source: seo_cache (River Stone Pour-Over keywords integrated into product-specific subject lines)
UGC hooks source: shared_cache (hooks from skills #5/#6 coordinated into Welcome step 1 and Win-back step 1)
```

## All 8 flows at a glance

| Flow | Trigger | Duration | Emails | SMS | Klaviyo files |
|---|---|---|---|---|---|
| Welcome | Newsletter signup | 14 days | 5 | 2 | 7 |
| Abandoned Cart | Started Checkout, no Placed Order | 72 hours | 3 | 2 | 5 |
| Post-Purchase | Placed Order | 30 days | 4 | 2 | 6 |
| Browse Abandonment | Viewed Product, no Add to Cart | 48 hours | 2 | 1 | 3 |
| Win-back | No order in 90 days (category default) | 21 days | 3 | 1 | 4 |
| Birthday | 7 days before birthday | 7 days | 1 | 1 | 2 |
| Replenishment | 25 days after Order with replenishable product | 14 days | 2 | 1 | 3 |
| Back-in-Stock | Product restocked + waitlist member | 24 hours | 1 | 1 | 2 |
| **TOTAL** | | | **21** | **11** | **32** |

---

## Deliverability checklist (program-wide)

The .docx brief includes a deliverability checklist that applies across all flows:

```
DELIVERABILITY CHECK

☐ DKIM record at sending domain
☐ SPF record updated for Klaviyo
☐ DMARC record set (p=none or stricter)
☐ Custom sender domain configured in Klaviyo
☐ SMS opt-in collection mechanism in place
☐ Master Suppression segment configured (unsubscribed, bounced, spam, disengaged)
☐ Sender name + reply-to set per flow (not no-reply@...)
☐ Physical mailing address in email footers (CAN-SPAM)
☐ Unsubscribe link visible in all email footers (CAN-SPAM)
☐ Quiet hours configured per flow for SMS (8am-9pm recipient local)
```

The buyer checks each box as they verify the underlying setup.

---

## File output structure

```
{output_folder}/
├── {{brand_name}}_email-flow-program_2026-05-22.docx      ← the brief
└── klaviyo_blocks/
    ├── welcome_01_email.txt
    ├── welcome_02_email.txt
    ├── welcome_03_email.txt
    ├── welcome_04_email.txt
    ├── welcome_05_email.txt
    ├── welcome_sms_01.txt
    ├── welcome_sms_02.txt
    ├── abandoned_cart_01_email.txt
    ├── abandoned_cart_02_email.txt
    ├── abandoned_cart_03_email.txt
    ├── abandoned_cart_sms_01.txt
    ├── abandoned_cart_sms_02.txt
    ├── post_purchase_01_email.txt
    ├── post_purchase_02_email.txt
    ├── post_purchase_03_email.txt
    ├── post_purchase_04_email.txt
    ├── post_purchase_sms_01.txt
    ├── post_purchase_sms_02.txt
    ├── browse_abandonment_01_email.txt
    ├── browse_abandonment_02_email.txt
    ├── browse_abandonment_sms_01.txt
    ├── winback_01_email.txt
    ├── winback_02_email.txt
    ├── winback_03_email.txt
    ├── winback_sms_01.txt
    ├── birthday_01_email.txt
    ├── birthday_sms_01.txt
    ├── replenishment_01_email.txt
    ├── replenishment_02_email.txt
    ├── replenishment_sms_01.txt
    ├── back_in_stock_01_email.txt
    └── back_in_stock_sms_01.txt
```

---

## Time-to-build estimate

The buyer's time to build the entire program in Klaviyo:

- **Without this skill:** 8-15 hours (or ~$2,500-$5,000 outsourced to a Klaviyo agency)
- **With this skill:** ~3-4 hours of pasting + flow configuration

Roughly an 80% time savings. The skill's value compounds across the rest of the buyer's roadmap — as new products launch, the buyer reruns the skill with new product context and the new product-specific copy is ready in minutes.

---

## How to build all 8 flows

The .docx brief's "How to Build in Klaviyo" section provides a recommended order:

1. **Set up Master Suppression segment first** (10 min)
2. **Configure sender domain + DKIM/SPF/DMARC if not already done** (varies — 30 min to 2 hours)
3. **Set up SMS opt-in mechanism if not already done** (30 min)
4. **Build the 3 essentials first** — Welcome, Abandoned Cart, Post-Purchase (90 min × 3 = 4.5 hours)
5. **Activate the 3 essentials** before building the rest. Let them run for 2-4 weeks to validate setup.
6. **Build the 5 supplementary flows** — Browse Abandonment, Win-back, Birthday, Replenishment, Back-in-Stock (60-90 min each × 5)
7. **Activate the supplementary flows** as data accumulates and prerequisites are met (Birthday requires birthday data; Replenishment requires Subscribe & Save consideration; Back-in-Stock requires waitlist setup)

---

## Coordination with other skills

When the buyer ran skill #2 (Listing SEO Optimizer) for their products before running this skill:

- The keywords from `keywords.json` get woven into product-specific subject lines (Abandoned Cart, Browse Abandonment, Post-Purchase, Back-in-Stock — all of which reference specific products in subject lines)
- Example: instead of "Your cart is still here," the subject becomes "Your ceramic pour over is still here" — better open rate AND better SEO visibility in search-mail apps

When the buyer ran skills #5 (Ad Creative) and #6 (UGC Creator Brief) before this skill:

- The UGC hook cache has archetype-specific hooks (problem-aware, social-proof, transformation, curiosity, contrarian)
- The Welcome flow's step 1 subject line and the Win-back flow's step 1 subject line both pull from the cache — the same brand argument runs across paid ads, creator content, and email
- This is the single biggest "brand coherence" win across the plugin

---

## Notes on this exemplar

- **The full program builds 32 paste-ready assets** in one run
- **Per-flow segmentation is documented in the .docx** so the buyer doesn't have to guess
- **A/B test plans are flow-specific** — only the highest-leverage tests recommended (not every email gets an A/B test)
- **Compliance is verified per email and per SMS** — buyer doesn't have to manually check Klaviyo against CAN-SPAM + TCPA
- **The Klaviyo paste-ready format saves 60-80% of build time** vs writing from scratch in Klaviyo's editor
