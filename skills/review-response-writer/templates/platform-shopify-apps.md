# Platform: Shopify Review Apps (Judge.me, Loox, Yotpo, Stamped, Reviews.io)

The most permissive review platform group. Reviews appear under products on the brand's own store; the merchant controls the surrounding context. Each app has slight differences but the constraints are similar enough to treat as a group.

## Reply visibility

- **Public:** Yes — the reply appears directly under the review on the product page.
- **Indexed:** Yes — Google indexes reviews + replies on Shopify product pages, so SEO weight is real.
- **Edit/delete:** Yes, the merchant can edit or delete their reply later. Customers cannot.

## Character limits

| App | Public reply limit | Notes |
|---|---|---|
| Judge.me | ~5000 chars | Practically unlimited. Use Markdown for line breaks (single newline = soft break, double newline = paragraph). |
| Loox | ~3000 chars | Plain text. Line breaks via newlines. |
| Yotpo | ~2500 chars | Plain text. Markdown not supported. |
| Stamped | ~2000 chars | Plain text. |
| Reviews.io | ~5000 chars | Plain text. |

For practical purposes: target **80-180 words** regardless of app. Long replies don't read as more caring; they read as overcompensating.

## Formatting

- Line breaks: yes (double newline = paragraph break)
- Markdown: only on Judge.me (and only basic — bold, italic, bullets). Don't rely on it for others.
- Emojis: allowed on all; use sparingly and only when on-brand. A warm brand voice can use one; a minimalist brand shouldn't.
- Hyperlinks: allowed on all but read as spam if used. Avoid linking out from a public reply. Use the private follow-up email for any links.
- Reviewer's name: first name only (last name shown in the review header is fine to use, but if the reviewer used only "M. Smith" or "Marcus T.", echo what they used)

## Tone register

Shopify review apps host reviews on the brand's own turf. The tone can be more brand-flavored than on third-party platforms (Trustpilot, Google) — but not so internal-jargon that new customers feel excluded.

Default register: **conversational, warm, real**. Match the brand's email and social voice.

## What's allowed (Judge.me / Loox / Yotpo specifically)

- Mentioning order numbers (when the reviewer mentioned theirs first)
- Naming employees by first name
- Mentioning sister products or product lines
- Offering remedies publicly (discounts, replacements, credit) — though best practice is to handle privately
- Asking the customer to email or DM
- Light brand storytelling ("This piece was thrown in our Brooklyn studio")

## What's prohibited / risky

- Posting the customer's email address publicly (privacy)
- Posting another customer's review or experience as a counterpoint (TOS violation on most apps)
- Bulk-pasting the same reply across multiple reviews (Yotpo and Judge.me flag this)
- Editing the reviewer's review text (you can't anyway; mentioning don't)

## Common pitfalls

1. **Form-letter syndrome** — Replies that start with "Thank you for your review!" on every review read like they came from a CS bot. The first sentence must reference the actual review's specific content.
2. **Discount-code reliance** — Sprinkling discount codes ("Use SORRY10 for 10% off") in public replies cheapens the brand and trains future negative reviewers to expect codes. Reserve codes for private follow-ups.
3. **Missing the SEO opportunity** — Replies are indexed. Including product names and key features naturally in 4-5★ amplify replies builds long-tail SEO. Don't keyword-stuff, but do mention the product by name and one or two features.

## Per-app quirks

### Judge.me
- Supports Markdown — use single newlines for soft breaks
- Has a "Q&A" reply mode separate from the review reply mode; make sure you're replying to the review, not the Q&A
- Allows photos in reviewer submissions — when the review has photos, refer to them ("I love the way you styled it")
- Reply editing is unlimited; mistakes are recoverable

### Loox
- Visual-forward — reviews often have photos
- Reply tone can lean more "Instagram caption" warm
- Auto-shows replies in the on-page carousel; truncates after ~3 lines for the preview
- **Front-load the key message** in the first 1-2 lines

### Yotpo
- More enterprise/legacy — replies look like email-style cards
- Less visual emphasis
- Yotpo's "Reviews" widget displays replies differently than "Q&A" widget; check which the brand has installed

### Stamped
- Smaller character window than the others
- More conservative tone register typically
- Often paired with Klaviyo for the brand's email flows; check if the review event triggers a follow-up email already (avoid duplicate reach-out)

### Reviews.io
- Hybrid third-party + on-site
- Reviews syndicate to Google Shopping
- Replies are indexed in Google rich results — treat them like Google Business Profile replies for SEO weight

## When Shopify connector is available

The skill can fetch reviews from product metafields for Judge.me, Loox, and Yotpo. The metafield paths differ — see `shopify-connector-fetch.md` for the exact paths.

For Stamped and Reviews.io, the data is stored off-Shopify and needs to come via CSV export from the app's own dashboard.

## Posting workflow

Buyer workflow once the .docx / .xlsx is generated:

1. Open the app's review management dashboard
2. Find the review by reviewer + date
3. Paste the drafted reply into the reply field
4. (Optional) Adjust opener/closer to vary across the batch
5. Post

For Judge.me + Loox, bulk reply isn't supported via UI — each reply is posted individually. Plan for ~10-20 seconds per reply at the posting step.
