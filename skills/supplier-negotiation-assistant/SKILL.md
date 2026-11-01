---
name: supplier-negotiation-assistant
description: >
  Drafts supplier outreach emails to Chinese, Indian, Vietnamese, North American, and EU manufacturers
  across five letter types — MOQ reduction, pricing tier request, payment terms, sample request, and
  dispute letters. Region-aware — each region has its own playbook for opening conventions, pacing of
  asks, indirect vs. direct framing, and holiday windows. Per-supplier relationship memory tracks
  contact info, stage (new / established / strained), prior asks, MOQs, payment history, and response
  patterns so each new letter reads like a continuing relationship. Single mode (one letter, one
  supplier) outputs .docx. Bulk RFQ mode (one request to N suppliers) outputs .xlsx with auto-ranked
  landed-cost comparison. Use this skill when the user mentions supplier email, supplier negotiation,
  MOQ reduction, RFQ, payment terms, dispute letter, Alibaba supplier, 'email my supplier,' or
  'negotiate with [supplier].'
---

# Supplier Negotiation Assistant

Drafts MOQ, pricing-tier, payment-term, sample-request, and dispute letters to manufacturers across five regions. Per-supplier relationship memory. Single or comparison bulk (RFQ to N suppliers + quote comparison).

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Detect mode.** Single letter (default) or comparison bulk.
3. **Identify the supplier(s).** Pull from supplier memory if known; collect basic info if new.
4. **Pick the letter type.** One of five — MOQ, pricing tier, payment term, sample request, dispute.
5. **Apply the regional playbook.** China / India / Vietnam / North America / EU.
6. **Compose the letter.** Universal 5-part skeleton, shaped by relationship stage + region + letter type.
7. **Update supplier memory.** Log the ask, the stage transition (if any), and any new info captured.
8. **Render output.** Single → `.docx`. Comparison bulk → `.xlsx` with one row per supplier + comparison sheet.
9. **Report back.** File path, supplier(s) addressed, relationship state changes, suggested next step (with follow-up timing per region).

---

## Step 1: First-run check

Look for `~/.the-ecommerce-seller/config/the-ecommerce-seller.config.json`. If missing, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

---

## Step 2: Detect mode

**Single letter mode is the default.** Switch to comparison bulk when any of these are true:

- The user attaches a list of supplier emails / Alibaba contacts
- The user says "send the same ask to multiple suppliers," "RFQ to N suppliers," "compare suppliers," "get quotes from a few factories"
- The user provides 2+ supplier names with the same negotiation goal
- The user says a count: "ask 5 suppliers for a quote on..."

Confirm out loud before proceeding.

---

## Step 3: Identify the supplier(s)

For each supplier, two paths:

### Path A: Known supplier (from memory cache)

Look up `~/.the-ecommerce-seller/cache/suppliers/{supplier-id}.json` via `scripts/supplier_memory.py`. The cache holds:

- Company name, contact name, contact role
- Region (china / india / vietnam / north_america / eu)
- Language preference
- Relationship stage (new / established / strained)
- Product categories sourced from them
- Known MOQs + pricing tiers
- Payment history
- Prior letters sent + outcomes
- Response time patterns
- Notes (preferred communication channel, time zone, holidays observed)

If known, pull all of this into the draft.

### Path B: New supplier

Collect minimum: company name, contact name (if known), region, language preference, what product is at stake, and any prior context (where the buyer found them, prior conversations).

Create a new supplier file in memory cache.

---

## Step 4: Pick the letter type

Read the matching template:

| Type | Template | When to use |
|---|---|---|
| MOQ reduction | `templates/letter-moq-reduction.md` | Supplier's MOQ is too high; you want a lower starting commit |
| Pricing tier request | `templates/letter-pricing-tier.md` | Ask for a better unit price, often by requesting volume-tier breakdowns or matching a competitor quote |
| Payment terms | `templates/letter-payment-terms.md` | Move from 100% upfront to deposit + balance, or from TT to LC, or ask for NET terms after established relationship |
| Sample request | `templates/letter-sample-request.md` | Request samples — paid, free, or sample-credit-against-first-order |
| Dispute letter | `templates/letter-dispute.md` | Defects, short shipment, wrong specs, late shipment, quality regression |

When the situation spans multiple types (e.g., "I want a lower MOQ AND better payment terms"), draft a combined letter that leads with one ask and adds the second as a softer follow-on. Read `templates/letter-craft.md` for the combined-ask rules.

---

## Step 5: Apply the regional playbook

Read the matching regional template:

| Region | Template | Key conventions |
|---|---|---|
| China | `templates/region-china.md` | Relationship-first, formal opening with honorific, indirect asks, patience with reply timing, attention to lunar holidays |
| India | `templates/region-india.md` | English-fluent, slightly more direct than China, may use formal honorifics, faster reply pace |
| Vietnam | `templates/region-vietnam.md` | Semi-formal, relationship-aware but more direct than China, English varies — keep sentences clean and unambiguous |
| North America (US / CA / MX) | `templates/region-north-america.md` | Direct, contract-forward, specific numeric asks, faster turnaround, MX may add Spanish-bilingual considerations |
| EU | `templates/region-eu.md` | Formal, compliance-aware, regulation references when relevant (CE marking, REACH, GDPR for B2B), structured paragraphs |

The regional playbook shapes:
- Opening line conventions
- Pacing of asks (lead with relationship vs. lead with ask)
- Numeric specificity (very specific in NA, slightly softer in China)
- Use of honorifics
- Reply expectations + follow-up timing

---

## Step 6: Compose the letter

Read `templates/letter-craft.md` for the universal 5-part skeleton:

1. **Open** — greeting + relationship acknowledgment (longer in China, shorter in NA)
2. **Bridge** — connect to the ongoing context (referencing prior order, recent conversation, or the situation triggering this letter)
3. **Ask** — the specific request, framed per the regional playbook
4. **Mutual benefit framing** — why this works for the supplier too (very important in Asia, less so in NA)
5. **Close** — clear next step + sign-off

Apply the relationship stage adjustments:

- **New supplier**: warmer intro, more relationship-building, smaller asks
- **Established supplier**: leaner, references prior orders, can ask bigger
- **Strained supplier**: extra care, may need a relationship-mend paragraph before the ask, often skip combined asks

Length targets vary by letter type and region — see `templates/letter-craft.md` for the table.

---

## Step 7: Update supplier memory

After each letter is composed, the skill writes to `~/.the-ecommerce-seller/cache/suppliers/{supplier-id}.json` via `scripts/supplier_memory.py`:

- Add the letter to `letters_sent` (date, type, summary of the ask)
- Update `current_relationship_stage` if the ask is significant enough to shift it (e.g., a dispute letter may push from "established" to "strained" pending response)
- Update `known_moqs`, `known_pricing_tiers`, `payment_history` if the letter references new numbers
- Update `last_contact_at` timestamp
- Add to `pending_responses` list with expected reply window per region's pacing norms

When the buyer comes back next week with "draft a follow-up to the Shenzhen supplier about the MOQ ask," the skill knows what was asked, when, and what response is expected.

---

## Step 8: Render output

### Single mode

Use `scripts/render_letter_docx.py` and the `docx` skill. Structure:

```
Letter: [Letter type] to [Supplier company]
Drafted: [date]
Region: [region — playbook applied]
Relationship stage: [new / established / strained]
Contact: [contact name] ([role])
Product context: [what's at stake — product line, current order, situation]

══════════════════════════════════════════════════
SUPPLIER MEMORY SNAPSHOT
══════════════════════════════════════════════════
- Known since: [date]
- Orders to date: [N orders]
- Prior asks: [list]
- Current MOQ on file: [N units]
- Current unit price: [$X]
- Payment terms in force: [terms]

══════════════════════════════════════════════════
DRAFTED LETTER
══════════════════════════════════════════════════
Subject: [subject line]

[Full letter body, ready to copy-paste into email / Alibaba TradeMessenger]

══════════════════════════════════════════════════
WHY THIS LETTER WORKS
══════════════════════════════════════════════════
- Regional cues applied: [list]
- Stage-appropriate tone: [explanation]
- The mutual-benefit framing: [explanation]
- Expected response window: [per region's playbook]

══════════════════════════════════════════════════
ALTERNATE PHRASINGS
══════════════════════════════════════════════════
[2-3 alternate phrasings for the key ask sentence so the buyer can pick what fits their voice]

══════════════════════════════════════════════════
SUGGESTED FOLLOW-UP TIMING
══════════════════════════════════════════════════
[Days to wait before nudging; what to do if no reply within window]
```

Save to `config.output_folder` with filename `supplier_letter_{supplier-slug}_{letter-type}_{date}.docx`.

### Comparison bulk mode

Use `scripts/render_rfq_comparison_xlsx.py`. Four-sheet workbook:

**Sheet 1: Outreach Queue** — one row per supplier with:
- Supplier name, region, contact name, contact channel
- Tailored letter draft (the same ask, but regionally + relationship-stage adjusted per supplier)
- Subject line
- Suggested send time per supplier's time zone
- Suggested follow-up date
- Quote Response (empty — buyer fills in as replies arrive)
- Quote Date (empty — when reply received)
- Status column (Drafted / Sent / Replied / No-reply / Awarded / Declined)

**Sheet 2: Quote Comparison** — auto-populates from Sheet 1 as the buyer fills in quotes:
- Supplier, MOQ offered, unit price, payment terms offered, lead time, shipping terms (FOB/EXW/DDP), sample policy
- Total landed cost calc (unit price × quantity + shipping + duties est.)
- Rank by total landed cost
- Comments column for the buyer's notes

**Sheet 3: Supplier Memory Updates** — one row per supplier showing what got written to the memory cache (new supplier file created, existing file updated, relationship stage transitions).

**Sheet 4: Negotiation Tactics Reference** — a quick-reference card on regional tactics, recommended counter-offers if first quotes are unfavorable, and "soft tells" to watch for in supplier replies (e.g., "supplier didn't address X" usually means X is non-negotiable).

Save to `config.output_folder` with filename `supplier_rfq_comparison_{rfq-name}_{date}.xlsx`.

---

## Step 9: Report back

Tell the buyer:
1. Where the file is (`computer://` link)
2. Supplier(s) addressed + region breakdown
3. Letter type + relationship stage applied
4. Supplier memory write summary (what was updated)
5. Expected reply window per region:
   - China: 24-72 hours during business hours (Beijing time); add a day if approaching Lunar New Year / Golden Week
   - India: 24-48 hours (Mumbai/Delhi business hours)
   - Vietnam: 24-72 hours (Ho Chi Minh / Hanoi business hours)
   - North America: 24-48 hours (business days)
   - EU: 48-96 hours (especially August / late December)
6. One suggested next step:
   - If single mode: "Send the letter via [recommended channel — Alibaba TradeMessenger / Gmail / direct email]. Set a follow-up reminder for [date per region]. The supplier memory has been updated."
   - If comparison bulk: "Send all N letters today; track responses in the .xlsx as they come in; the Quote Comparison sheet will auto-rank suppliers by total landed cost once you've filled in 2+ quotes."

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Gmail | Skill drafts copy-paste-ready letters; flags Gmail-direct-send as an upgrade |
| Alibaba MCP (if/when available) | Skill drafts letters formatted for TradeMessenger paste; flags direct send as upgrade |

The skill always produces a complete letter — connectors are nice-to-have.

---

## Edge cases

- **Combined-ask letters** (MOQ + payment terms in one letter): allowed for established relationships, discouraged for new + strained. Lead with the smaller ask.
- **Multilingual letters**: when the supplier's language preference is non-English and the brand voice config supports the language, draft in the supplier's language with English in parentheses for key numbers. When buyer's brand voice doesn't support, draft in English using simpler vocabulary and shorter sentences.
- **Dispute letters that may end the relationship**: skill flags "consider the relationship cost" in the .docx and offers a softer alternative version. The buyer chooses.
- **Sample-request asks from a competitor's supplier**: skill warns the buyer about reputational risk and recommends transparent framing rather than trying to hide the connection.
- **Cultural holidays affecting reply timing**: skill checks `templates/region-*.md` holiday tables and warns the buyer if the letter is sent during a known holiday window (Lunar New Year, Golden Week, Diwali, EU summer holidays).
- **Supplier's first language is unclear**: skill defaults to the region's primary language convention and writes the letter in English with English-second-language considerations (shorter sentences, no idioms, no sarcasm).
- **Strained-relationship sample request**: when a supplier delivered a bad shipment and now the buyer wants samples of a new product, the skill flags that the sample ask should wait until the prior dispute is resolved. Or, recommends rolling the sample ask into the dispute resolution as a make-good gesture.
- **New supplier with unverified credentials**: skill doesn't draft payment-term-flexible letters (e.g., asking for NET 30) until the supplier has at least one completed order in the memory cache. New suppliers always start at 100% upfront or deposit-and-balance — the skill flags this.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema (extended with supplier_negotiation section)
- `templates/letter-moq-reduction.md` — MOQ reduction patterns + leverage points
- `templates/letter-pricing-tier.md` — pricing tier / volume-discount request patterns
- `templates/letter-payment-terms.md` — payment term negotiation patterns (deposit %, NET terms, TT vs. LC)
- `templates/letter-sample-request.md` — sample request patterns (free, paid, credit-against-first-order)
- `templates/letter-dispute.md` — dispute patterns (defects, short shipment, wrong specs, late shipment)
- `templates/letter-craft.md` — universal 5-part skeleton + relationship stage adjustments + combined-ask rules
- `templates/region-china.md` — Chinese supplier conventions, opening, pacing, holidays
- `templates/region-india.md` — Indian supplier conventions
- `templates/region-vietnam.md` — Vietnamese supplier conventions
- `templates/region-north-america.md` — US / CA / MX conventions
- `templates/region-eu.md` — EU conventions
- `templates/supplier-memory.md` — per-supplier relationship state file schema + tracking rules
- `templates/rfq-quote-comparison.md` — comparison bulk methodology + total landed cost calc
- `scripts/config_loader.py` — shared config loader
- `scripts/supplier_memory.py` — per-supplier relationship cache writer/reader
- `scripts/render_letter_docx.py` — single-letter .docx renderer
- `scripts/render_rfq_comparison_xlsx.py` — comparison bulk .xlsx renderer (4-sheet)
- `examples/single-moq-reduction-example.md`
- `examples/single-dispute-letter-example.md`
- `examples/bulk-rfq-comparison-example.md`
