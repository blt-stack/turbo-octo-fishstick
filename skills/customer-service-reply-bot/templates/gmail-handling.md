# Gmail Handling — Auto-Fetch + Categorize Workflow

When the buyer has Gmail connected and asks the skill to "process my inbox" or "do the next 10 unread tickets," the skill runs the Gmail auto-fetch workflow. This file documents that workflow.

## Prerequisites

- Gmail connector must be installed in the buyer's Claude / Cowork environment
- The buyer's customer-service emails should be reasonably labeled / filtered (in a "Support" or "Customer Service" label, or filterable by sender domain). If everything's in the main inbox mixed with personal email, the skill has to do more categorization work.

## Workflow

### Step A: Detect the customer-service inbox

The skill needs to know where the customer-service messages live. Options to check, in order:

1. **`config.cs_inbox.gmail_label`** — if the buyer set this during onboarding (e.g., "Support" or "INBOX"), use it directly
2. **Common labels** — if config doesn't have it, the skill checks for labels named one of: "Support," "Customer Service," "Help," "CS"
3. **Sender filtering** — if no dedicated label, the skill filters the inbox by sender (anyone NOT on the buyer's "personal contacts" list, plus emails to support@/hello@/info@/customerservice@ addresses)
4. **Ask the buyer** — last resort. "I don't see a customer-service label. Should I filter by sender to find CS tickets, or do you want to create a label first?"

Once detected, the skill caches the label/filter for future runs (no need to re-ask each time).

### Step B: Fetch the messages

Use the Gmail connector's search/list capability:

```
query: label:Support is:unread
max_results: [batch size, default 10]
```

For each message returned:

1. Get the message ID
2. Fetch the message details (subject, body, sender, received_at, thread context)
3. Parse the sender's email address — extract domain to check against known spam/promo senders
4. Strip any quoted prior conversation (if it's a reply in a thread, capture only the new content)
5. Strip signature blocks (heuristic: 3+ lines at the bottom after a `--` separator or after a known signature pattern)
6. Strip promotional footers ("This email was sent by..." auto-footers)

The cleaned message body is what gets fed to categorization.

### Step C: Filter out non-CS messages

Not everything in the CS inbox is actually a customer-service ticket. Filter out:

- **Spam / promotional email** — unsolicited sales pitches, SEO outreach, "I noticed your website" cold pitches. These are NOT CS tickets.
- **Internal team communications** — emails from co-workers using the CS inbox for internal forwarding
- **Auto-replies** — vacation auto-responses, shipping carrier auto-notifications, marketing platform receipts
- **Order confirmations or system notifications** — the customer's order confirmation isn't a CS ticket; the customer's reply to it might be

The skill flags these as "skip — not a CS ticket" in the batch and continues with the rest. In single mode, asks the buyer to paste a real ticket instead.

### Step D: Categorize each ticket

For each remaining ticket, run the standard categorization (4 categories + sub-type, as documented in the main SKILL.md).

### Step E: Handle threading

If a fetched message is part of an ongoing thread (the customer has already emailed multiple times about this issue):

1. Fetch the full thread, not just the latest message
2. Read the prior messages from the brand's side to know what's already been said
3. Read the prior customer messages for context
4. Draft a reply that acknowledges the ongoing context ("I see we've been emailing about this — sorry it's taken multiple touches")
5. Avoid contradicting prior brand replies (if the brand already offered a refund, don't switch to offering an exchange)

### Step F: Draft replies as usual

Once each ticket is parsed, categorized, sentiment-detected, and contextualized, the standard reply-drafting workflow runs. Output goes to .xlsx in batch mode, .docx in single mode.

### Step G: Don't auto-send

The skill draft replies; it doesn't send them. Sending requires buyer review for at least these reasons:

- Tone calibration (the buyer knows their voice better than the model)
- Action approval (refunds and credits cost real money)
- Customer-specific context the model doesn't have (e.g., "this customer is the founder's college friend")
- Legal / compliance (some regulated categories require human review on all CS responses)

If the buyer explicitly says "auto-send approved replies for low-risk categories" in their config, the skill can support that — but it defaults to draft-only.

### Step H: Mark tickets as handled (optional)

After drafting, the skill can optionally apply a Gmail label like "drafted-by-skill" to the fetched messages so they're not re-processed in the next batch. This is opt-in via `config.cs_inbox.auto_label_drafted` because some buyers prefer to manually handle their own ticket-flow tracking.

## Things the skill does NOT do via Gmail

- **Send replies** (drafts only)
- **Delete messages** (never)
- **Archive messages** (only if buyer opts in explicitly)
- **Forward to third parties** (escalation to a founder/team is done via the .docx/.xlsx, not by forwarding emails)
- **Reply to messages outside the customer-service inbox** (if a CS ticket landed in the main inbox by mistake, the buyer needs to forward it to the CS label first)

## Common Gmail-handling pitfalls

- **Treating an ongoing thread as a new ticket** — feels jarring to the customer who's been emailing for days
- **Missing the customer's order ID** in the email body — order IDs are often in the email signature or footer of the customer's reply
- **Stripping too aggressively** — the customer's email signature sometimes contains useful info (e.g., their delivery address); preserve identifiable context
- **Re-processing the same ticket multiple times** — without the auto-label, the same tickets show up in every "next 10 unread" batch

## Multi-mailbox or shared-inbox scenarios

For brands using shared inboxes (multiple team members handling tickets out of one Gmail account), the skill flags any ticket where a team member has already drafted/sent a reply within the past hour. This prevents the skill from re-replying to a ticket that's already been answered.

For brands using multiple inboxes (e.g., separate `support@` and `hello@`), the skill can be configured per-inbox in `config.cs_inbox.gmail_labels` (a list rather than a single label).

## When Gmail is not connected

The Gmail connector is optional. When unavailable:

- Single mode: buyer pastes one ticket per run. Works fine, just slower for high-volume inboxes.
- Batch mode: buyer uploads a CSV exported from their helpdesk/email tool. The skill processes it identically.

The skill never blocks on Gmail being missing — it just flags the auto-fetch capability as an upgrade.
