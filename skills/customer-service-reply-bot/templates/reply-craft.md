# Reply Craft — Universal Structure + Tone Framework

The mechanics every reply follows, regardless of category. Category-specific patterns live in the per-category files; this file is the cross-cutting craft.

## The 4-part reply skeleton

Almost every CS reply follows this structure. Skipping a step makes the reply feel incomplete; adding extra paragraphs makes it bloat.

### 1. Acknowledge

Name the issue back to the customer in their own words. Don't paraphrase awkwardly. Don't repeat the entire ticket back at them — pick the core thing they're upset/asking about and reflect it.

**Good:**
> "I'm sorry your order arrived broken."

**Bad:**
> "Thank you for reaching out about your recent purchase from us. We understand that you have experienced an issue with the product you received and we sincerely apologize for any inconvenience..."

(Generic, slow, makes them wait two sentences to feel heard.)

### 2. Apologize / take ownership (when warranted)

Apologize when the brand is at fault. Don't apologize when it isn't — sounds insincere and trains customers that complaining works regardless.

**Good (brand at fault):**
> "That's our error, not yours."

**Good (brand not at fault — shipping carrier delay):**
> "We're sorry the wait has been frustrating — we'll do what we can to escalate with UPS."

(Empathy without taking blame for something the brand can't control.)

**Bad:**
> "We apologize for any inconvenience our product may have caused."

(Vague non-apology. Sounds defensive.)

### 3. Resolve specifically

State exactly what you're going to do, with a timeline. Customers fear ambiguity more than bad news.

**Good:**
> "Here's what I'm going to do: I'm shipping a replacement today via priority — should arrive by Tuesday. You don't need to send the broken one back; just dispose of it."

**Bad:**
> "We'll look into this and get back to you as soon as possible."

(Open-ended. Customer has to wait without knowing the outcome.)

### 4. Close warmly

Brief, brand-voice sign-off. Real name, not "the team." Reply-friendly ("just reply to this email").

**Good:**
> "Thanks for letting us know. If anything else comes up, just reply to this email — it comes straight to me.
>
> — Sarah, {{brand_name}}"

**Bad:**
> "We appreciate your continued patronage. The {{brand_name}} Customer Support Team."

(Corporate, depersonalized.)

---

## Universal tone principles

### Match the brand voice (from config)

The reply uses the same brand voice as the rest of the program — warm/slow brands have warm/slow replies; bold/direct brands have direct replies. The voice is consistent across marketing, product, and CS.

### Specificity over vagueness

Be specific about order numbers, dates, products, dollar amounts. Specific replies signal "we know who you are; we read your message." Vague replies signal "you're a ticket number."

### Concise over thorough

Most CS replies should be 80-180 words. Longer reads as defensive (when written) or as not-respecting-the-reader's-time (when read). Length expansion is justified for defects/damages (more reassurance needed) and rare for pre-purchase (too long signals over-selling).

### Real person, not "the team"

Sign with a real first name. For very small brands, the founder name. For larger, a real CS person's name. Never "the customer service team" — customers respond better to humans.

### Reply-friendly

Always close with something that invites continued conversation ("just reply to this email — it comes straight to me"). Even when the issue is resolved. This:
- Reduces escalation friction if the resolution doesn't hold
- Signals the brand is approachable
- Makes the customer feel heard even when they don't reply

---

## Tone-of-voice register selection

The brand voice profile in `config.brand_voice` provides a few adjectives. Map to register:

| Brand voice descriptor | CS reply register |
|---|---|
| Warm, slow, artisanal | Conversational, sensory details OK in close ("our studio is quiet today, we'll get on this"), founder-name sign-off |
| Modern, technical, clean | Direct, precise, no fluff, professional sign-off, less personality in the sign-off |
| Playful, bold, vibrant | Casual, allowed one tasteful joke if the situation supports it (NOT for serious complaints), playful sign-off |
| Premium, luxurious | More formal, controlled language, "please accept our apology" rather than "sorry about that," sign-off uses title (e.g., "Sarah, Customer Care, {{brand_name}}") |
| Outdoor, rugged, lived-in | Plainspoken, no over-apologizing, action-oriented language ("we'll fix it"), short |

Skill picks register based on `config.brand_voice` and adjusts each reply accordingly.

---

## What to NEVER do in CS replies

- **Use ALL CAPS** anywhere except for product names that are stylistically capitalized
- **Use excessive exclamation marks** — one per reply at most, and only for genuinely positive closes
- **Use "policy" as a defense** when the brand could be more generous and earn the customer
- **Say "unfortunately"** — softens via passive voice while making the customer wait for the bad news
- **Say "as a courtesy"** — passive-aggressive, signals "this is a one-time favor"
- **Say "thank you for your patience"** before the customer has demonstrated patience — preempting their reaction reads as condescending
- **Say "I understand you are frustrated"** — usually feels formulaic; show understanding via action instead
- **Quote the entire prior message** back to them — they wrote it; they remember
- **Use form-letter language** ("Thank you for contacting us about your recent inquiry")
- **Promise things the brand can't actually deliver** — over-promising on shipping speed, refund timing, etc. creates a second angry ticket

---

## What to ALWAYS do

- **Reply within 24 hours** for standard tickets, 4 hours for angry/high-risk ones
- **Use the customer's first name** when known
- **Reference specific order details** (number, products, dates) when available
- **State the action you're taking** with a timeline
- **Sign with a real name**
- **End with a reply-friendly close**
- **Match the brand voice** consistently

---

## Reply length by category (target)

| Category | Word count target |
|---|---|
| Shipping issues (info request) | 60-100 |
| Shipping issues (delay/loss) | 120-180 |
| Returns / refunds | 100-180 |
| Defects / damages | 140-220 (more reassurance) |
| Pre-purchase questions | 80-160 (varies with question depth) |

Replies over 250 words start to lose the reader. Replies under 60 feel curt for anything but quick info requests.

---

## Subject line for the reply

When the skill drafts a reply for an email-based ticket, it provides a subject line. Default pattern:

- For replies to existing thread: `Re: [original subject]`
- For escalated tickets: `Re: [original subject] — [Founder name]`
- For new outbound (rare; the customer rarely needs an unprompted new thread from CS): brand-voice subject with specific context

The subject line auto-includes "Re:" when the ticket is a reply to an existing message — Gmail and most clients thread off this prefix.

---

## Signature block (recommended)

Each reply should end with a clean signature. Default structure for a small brand:

```
— [Founder name]
{{brand_name}}
{{store.website_url}}
```

For larger brands with dedicated CS:

```
— [CS person's first name]
Customer Care, {{brand_name}}
{{store.website_url}}
```

Skill pulls the signature pieces from `config.store.brand_name` and `config.store.website_url`. Founder name is set during onboarding under `config.store.founder_name` (the skill asks once if not set).
