---
name: customer-service-reply-bot
description: >
  Drafts on-brand, empathetic replies to customer service tickets across four categories: shipping
  issues, returns/refunds/exchanges, defects/damages, and pre-purchase questions. Each reply pairs
  with a recommended business action (refund, reship, partial credit, escalate) and one-line
  rationale. Sentiment-aware — angry tickets get an apologetic tone, pre-purchase questions get a
  sales-aware tone. Two modes: single ticket (paste or auto-fetch from Gmail) outputs .docx; bulk (CSV
  upload or fetch N unread from Gmail) outputs .xlsx with one row per ticket. Pulls order context from
  Shopify when available. Use this skill when the user mentions customer service, support tickets,
  support inbox, customer email, 'reply to this customer,' 'draft a response,' refund request,
  shipping complaint, return request, defect complaint, sizing question, or 'drowning in tickets.'
---

# Customer Service Reply Bot

Drafts replies + recommended actions for support tickets across 4 categories. Single ticket or batch mode. Sentiment-aware tone. Pulls order context from Shopify when available.

## How this skill works at a glance

1. **First-run check.** Load shared plugin config; trigger onboarding if missing.
2. **Detect mode.** Single ticket (default) or batch.
3. **Ingest ticket(s).** Paste, Gmail auto-fetch, or CSV upload.
4. **Categorize each ticket.** Match to 1 of 4 categories + sub-type. Detect sentiment.
5. **Pull order context.** If ticket references an order, fetch details from Shopify.
6. **Draft reply.** Apply brand voice + category-specific reply pattern + order context.
7. **Recommend action.** Reply + action go together — refund / reship / credit / escalate / no action.
8. **Render output.** Single mode → `.docx`. Batch mode → `.xlsx`.
9. **Report back.** File path, ticket(s) processed, sentiment breakdown, suggested next step.

---

## Step 1: First-run check

Look for `<plugin-root>/.config/the-ecommerce-seller.config.json`. If missing, run onboarding from `../product-description-writer/templates/onboarding.md`. Use `scripts/config_loader.py`.

---

## Step 2: Detect mode

**Single ticket mode is the default.** Switch to batch when any of these are true:

- The user attaches a CSV of tickets
- The user says "batch," "go through my inbox," "process all unread," "do my whole queue"
- The user provides 3+ tickets pasted in one message
- The user says a count: "process the next 10," "do 25 unread tickets"

Confirm out loud before proceeding.

---

## Step 3: Ingest tickets

Four ingestion paths:

### Path A: Buyer pastes the ticket (default for single mode)

Most universal. Buyer copies the customer's message and pastes. Skill parses the customer's name, email if visible, the message itself, any order references.

### Path B: Gmail auto-fetch (when connector available)

If Gmail is connected and the buyer says "process the next unread" or "go through my inbox," use the Gmail connector to fetch unread messages from the customer-service folder/label. Read `templates/gmail-handling.md` for the workflow:

1. Detect which folder/label holds customer-service emails (ask buyer if unclear — common labels: "Support," "Customer Service," "Hello," or just "Inbox" filtered by sender domain)
2. Fetch the N most recent unread messages
3. For each, parse the customer's name, email, subject line, body
4. Strip signature blocks / quoted prior thread / promotional footers
5. Continue with categorization

### Path C: CSV upload (for batch mode without Gmail)

Buyer uploads a CSV exported from their ticketing tool (Gorgias, Help Scout, Shopify Inbox, Outlook export, etc.). Expected columns (case-insensitive, any subset):

- `customer_name`, `customer_email`, `subject`, `message_body`, `order_id` (optional), `received_at` (optional)

Parse, then categorize each row.

### Path D: Direct Shopify integration (when ticket references an order)

When a ticket includes a Shopify order ID (e.g., `#1024`) or the customer email matches a Shopify customer record, pull additional context:
- Order date, fulfillment status, shipping carrier + tracking
- Products in the order (names, variants, prices)
- Customer's lifetime order count + lifetime value
- Whether they're a first-time or repeat buyer

This order context dramatically improves reply quality — generic "we're so sorry your order is delayed" becomes "we're so sorry order #1024 is delayed — UPS shows it left the facility Tuesday and is currently sitting in [city]. Here's what we'll do..."

---

## Step 4: Categorize the ticket

Match each ticket to one of 4 categories + a sub-type. Read the matching template:

| Category | Template | Common sub-types |
|---|---|---|
| Shipping issues | `templates/shipping-issues.md` | Delay, lost, wrong address, tracking question, missing item |
| Returns / refunds / exchanges | `templates/returns-refunds.md` | Doesn't fit, changed mind, arrived damaged, want different color/size, late return |
| Defects / damages / quality | `templates/defects-damages.md` | Broken on arrival, broke after N days, manufacturing defect, color/material mismatch |
| Pre-purchase questions | `templates/pre-purchase-questions.md` | Sizing, materials, fit, use-case, shipping speed, compatibility |

When categorization is ambiguous (a single ticket spans multiple categories), pick the primary category but note the secondary in the brief.

### Detect sentiment

Read `templates/sentiment-routing.md` for the framework. Three sentiment tiers:

- **Angry / frustrated:** all-caps, exclamation marks, "this is unacceptable," "I want a refund NOW," "I'm so disappointed." → More apologetic tone, faster action, often escalate to founder
- **Neutral / matter-of-fact:** professional or transactional tone. → Warm but not over-apologetic
- **Friendly / patient:** thanks the buyer in advance, says "no rush," uses please/thank you. → Match their warmth, often gets a small upgrade (free shipping next time, etc.)

Sentiment shapes the reply tone but not the underlying business action — refunds owed should still be refunded regardless of how the customer asked.

---

## Step 5: Pull order context (when applicable)

If the ticket references an order ID or customer email matching a Shopify record, fetch:

- Order details (date, products, totals)
- Fulfillment status (unshipped, shipped, delivered, exception)
- Shipping carrier + tracking number + last known location
- Customer lifetime metrics (orders, total spent, first purchase date)

Use the Shopify connector. When unavailable, ask the buyer for the order details before drafting.

---

## Step 6: Draft the reply

Read `templates/reply-craft.md` for the universal reply structure. The 4-part skeleton:

1. **Acknowledge** — name the issue back to the customer in their own words ("I'm sorry your order arrived broken")
2. **Apologize / take ownership** (when warranted) — never weasel-word the apology when the brand is at fault
3. **Resolve** — state specifically what you're going to do (refund, reship, ship a replacement, etc.) with a timeline
4. **Close warmly** — brief, brand-voice sign-off

Apply the brand voice from `config.brand_voice`. Apply the category-specific reply patterns from the matching template. Apply the order context to make the reply specific (not generic).

**Length target:** 80-180 words for most tickets. Longer for defects/damages (more reassurance). Shorter for pre-purchase (helpful + fast).

**Never:**
- Use form-letter language ("Thank you for contacting us...")
- Hide behind policy ("Per our return policy...") when the policy itself caused the problem
- Sound robotic
- Make promises the buyer can't keep (overpromising on shipping resolution leads to a second angry ticket)
- Use ALL CAPS or excessive exclamation marks
- Sign off as "the team" when a real person should sign

---

## Step 7: Recommend an action

Read `templates/action-recommendations.md` for the decision framework. The skill recommends one of these actions per ticket:

| Action | When |
|---|---|
| **No action needed** | Pre-purchase Q&A, simple info request, customer satisfied |
| **Resend tracking / status update** | Customer just wants info |
| **Reship the product** | Lost in transit, wrong item shipped, defect within return window |
| **Issue partial refund** | Minor defect customer wants to keep, late shipping |
| **Issue full refund** | Defective + doesn't want replacement, fundamental brand-fault |
| **Issue full refund + store credit** | Full refund + relationship-saver (extra credit for the hassle) |
| **Issue full refund + free reship** | When the situation warrants both ("our error twice") |
| **Honor return / process exchange** | Standard return request within window |
| **Decline gracefully (with reason)** | Outside return window, customer error not brand error |
| **Escalate to founder / owner** | High-LTV customer, public complaint risk, unusual situation, customer named the founder |

For each action, the skill includes a one-line rationale:

> Recommended action: Full refund + $10 store credit
> Rationale: Customer's order delayed 8 days because the buyer's fulfillment partner dropped the ball. The customer is reasonable so far (no public complaint yet). Make it right + give them a reason to stay.

The buyer decides whether to take the recommended action or pick a different one. The reply text doesn't need to change — it's written generally enough to match the action the buyer ultimately takes.

---

## Step 8: Render output

### Single mode

Use `scripts/render_reply_docx.py` and the `docx` skill. Structure:

```
Reply to: [Customer name] (received [date])
Category: [shipping issues — delay]
Sentiment: [neutral]
Order: #1024 (placed [date], shipped [date], status: delayed in transit)

══════════════════════════════════════════════════
DRAFTED REPLY
══════════════════════════════════════════════════
Subject: Re: [original subject]

[Full reply text, ready to copy-paste into Gmail / helpdesk]

══════════════════════════════════════════════════
RECOMMENDED ACTION
══════════════════════════════════════════════════
Action: [Issue $10 store credit + escalate to founder if no movement in 48 hours]
Rationale: [One-line explanation]
Estimated cost to brand: [$10 + ~3 minutes of buyer's time]

══════════════════════════════════════════════════
CUSTOMER CONTEXT
══════════════════════════════════════════════════
- LTV: $340 across 4 orders
- First purchase: [date]
- Past CS interactions: none
- Risk of public complaint: low (customer has been measured so far)

══════════════════════════════════════════════════
ORIGINAL TICKET (for reference)
══════════════════════════════════════════════════
[Customer's original message, formatted cleanly]
```

Save to `config.output_folder` with filename `cs_reply_{customer-last-name}_{date}.docx`.

### Batch mode

Use `scripts/render_replies_xlsx.py`. Three-sheet workbook:

**Sheet 1: Reply Queue** — one row per ticket with:
- Received date, Customer name, Customer email, Category, Sub-type, Sentiment
- Original ticket (cell-text, wrapped)
- Drafted reply (cell-text, wrapped)
- Recommended action, Rationale, Estimated cost
- Status column (Pending review / Approved / Sent / Held / Escalated — buyer fills in)

**Sheet 2: Category Breakdown** — counts per category, sentiment distribution, action frequency. Helps the buyer spot patterns ("8 of 23 tickets this week are shipping delays — root-cause investigation?").

**Sheet 3: Recommended Process Changes** — if the skill detects recurring patterns (5+ tickets about the same product defect, 3+ shipping complaints about the same carrier), it surfaces those as systemic issues worth fixing once rather than reactively replying forever.

Save to `config.output_folder` with filename `cs_reply_batch_{date}.xlsx`.

---

## Step 9: Report back

Tell the buyer:
1. Where the file is (`computer://` link)
2. Ticket(s) processed + category breakdown
3. Sentiment summary (e.g., "12 neutral, 4 friendly, 2 angry")
4. Total recommended cost to brand across all actions (e.g., "$87 in refunds + 2 reships")
5. Any systemic-issue flags from Sheet 3
6. One suggested next step:
   - If batch mode: "Review the .xlsx, mark each ticket's status, and send the approved replies. The systemic-issue sheet flags patterns worth investigating."
   - If single mode: "Review the reply and recommended action. Adjust the action if the customer's relationship merits something different."
   - If Gmail isn't connected: "Connect Gmail to enable auto-fetch — pasting tickets one at a time scales poorly past 5/day."

---

## Connector availability and graceful degradation

| Connector | Behavior when missing |
|---|---|
| Shopify | Skill drafts replies from ticket text alone; flags that order context would make replies more specific |
| Gmail | Skill works on pasted tickets only; flags auto-fetch as an upgrade |
| Helpdesk MCP (Gorgias, Help Scout, Zendesk) | Skill works on CSV exports; flags as upgrade |

The skill always produces a complete reply — connectors enrich.

---

## Edge cases

- **Multiple tickets from the same customer in a thread:** treat the full thread as context. Reply to the latest message but acknowledge the prior context ("I see we've been emailing about this — I'm sorry it's taken multiple touchpoints").
- **Customer language not English:** if the original ticket is in a non-English language, draft the reply in the same language (if buyer's brand voice supports it) or flag for translation handoff. Don't reply in English to a French customer.
- **Customer threatens public complaint** ("I'm posting this on Trustpilot"): tag the ticket as high-risk in the action recommendation. Recommend founder escalation. Add an extra apology line in the reply.
- **Customer is a known repeat-issue customer** (filed CS tickets on 50% of past orders): note in the customer context but don't change tone. Some customers are high-need; that's not the brand's problem to solve via tone, only via process.
- **Customer asks for something the brand can't legally do** (refund of a non-refundable digital product, exchange of a final-sale item): draft a decline reply that's warm + explains the policy without hiding behind it. Offer an alternative (a discount on a future order, store credit) when possible.
- **Ticket is actually spam / phishing / random** (selling SEO services, etc.): flag as "no reply needed — likely spam" in batch mode. Skip in single mode.
- **Pre-purchase question from an existing customer**: treat slightly differently — they're warmer than a cold prospect. Reference past orders if relevant.

---

## Files in this skill

- `SKILL.md` — this file
- `config.example.json` — shared config schema
- `templates/shipping-issues.md` — shipping ticket sub-types + reply patterns + action recommendations
- `templates/returns-refunds.md` — returns/refunds/exchanges sub-types + patterns
- `templates/defects-damages.md` — defect/damage sub-types + patterns
- `templates/pre-purchase-questions.md` — pre-purchase sub-types + sales-aware patterns
- `templates/reply-craft.md` — universal 4-part reply structure + tone framework
- `templates/action-recommendations.md` — decision framework for refund/reship/credit/escalate
- `templates/sentiment-routing.md` — angry / neutral / friendly detection + tone adjustments
- `templates/gmail-handling.md` — Gmail auto-fetch workflow + label detection
- `scripts/config_loader.py` — shared config loader
- `scripts/render_reply_docx.py` — single-reply .docx renderer
- `scripts/render_replies_xlsx.py` — batch .xlsx renderer with category breakdown + systemic-issue detection
- `examples/single-shipping-issue-example.md`
- `examples/single-defect-example.md`
- `examples/bulk-batch-example.md`
