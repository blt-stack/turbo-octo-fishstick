# Platform: Facebook Page Reviews / Recommendations

Facebook restructured its review system to a binary "Recommendations" model (Yes/No instead of stars). Recommendations appear on the brand's Facebook Page and have moderate SEO + trust weight, though less than Google or Trustpilot.

## Reply visibility

- **Public:** Yes — replies appear nested under the recommendation
- **Indexed:** Limited — Facebook content is partially crawled by Google
- **Edit/delete:** Yes — replies can be edited freely
- **Reply quota:** One reply per recommendation (though the brand can reply multiple times in a thread)

## What "Recommendations" actually means

Each recommendation is binary:
- **"Recommends"** (positive) — equivalent to 4-5★
- **"Does not recommend"** (negative) — equivalent to 1-2★

There is no 3★ equivalent on Facebook. Treat any "Recommends" with mixed body content as a clarify-tier reply (recommend tier-clarify treatment), and "Does not recommend" as recovery.

## Character limit

8000 characters. Practically: target **40-100 words**. Facebook's audience skims; long replies get truncated by the "See more" expand.

## Tone register

**Conversational, personal.** Facebook's social context means slightly more informal than Shopify (and much more informal than Amazon or Trustpilot). Use a warm voice that matches the brand's Page voice.

## Reply structure (Facebook-specific)

For "Does not recommend" (1-2★ equivalent) recovery:

```
Hi [First name],

We're so sorry [specific issue]. I just sent you a DM through Messenger so we can take care of this directly.

Thank you for telling us.
— [First name]
```

For "Recommends" with mixed feedback (3★ equivalent clarify):

```
Hi [First name],

Thank you for the kind words about [positive] — and also for the honest feedback on [friction]. We'd love to know more — feel free to DM us or reply here.

— [First name]
```

For "Recommends" amplify (4-5★ equivalent):

```
Hi [First name],

Thank you so much! [Specific reflection of their praise.] This made our day.
— [First name]
```

## Facebook-specific allowances

- **DM/Messenger handoff** — almost always preferred over email handoff on Facebook
- **Tagging** — DON'T tag the customer in the reply (Facebook flags it as spam). Just reply directly.
- **Emojis** — more natural on Facebook than other platforms; use sparingly
- **Casual openers** — "Hey [Name]" works on Facebook where it might not on Trustpilot
- **Light brand humor** — only on amplify, only when on-brand

## Facebook-specific restrictions

- No external links (Facebook deprioritizes posts with links)
- No phone numbers or email addresses in the public reply (they look spammy)
- No images or videos in replies (they don't render properly)
- Don't paste the same reply across multiple recommendations (Facebook's spam filter flags this)

## Facebook removal disputes

Facebook will remove recommendations / replies that:
- Violate Community Standards (hate speech, threats, sexual content)
- Are spam (clear marketing for unrelated products)
- Are off-topic (recommendation clearly meant for a different page)
- Are coordinated inauthentic behavior

The dispute path is via the 3-dot menu on each recommendation. See `dispute-drafts.md`.

## Disabling Recommendations entirely

The page owner can turn off Recommendations entirely in Page Settings. This nuclear option removes all recommendations (good and bad) from view. The skill's report flags when the buyer's profile has 3+ "Does not recommend" entries in a short window — at that point, the buyer may want to consider disabling Recommendations temporarily while addressing root causes.

This is mentioned only in the report — never recommended in a reply.

## Messenger handoff workflow

The buyer's actual follow-through happens in Messenger:
1. Public reply says "I just sent you a DM" (or "I just messaged you")
2. Buyer opens the Page's Messenger inbox
3. Sends a message to the customer
4. Customer receives it as a Page-message (not a personal account message)

The skill drafts the Messenger message as the "private follow-up" — same structure as email but adjusted for chat format (shorter, more direct).

### Messenger follow-up structure

```
Hi [Name],

I saw your review and wanted to follow up directly. [Acknowledge.]

Here's what we're doing:
- [Concrete action 1]
- [Concrete action 2]

[Easy next step from customer.]

— [Name]
```

The Messenger message should be **shorter than an email follow-up** — chat tone, not letter tone. Skip the email signature.

## Common Facebook recommendation patterns

### "Does not recommend — terrible customer service"

Public reply:
```
Hi [Name],

I'm sorry our team didn't show up the way you needed. I just DM'd you personally so we can fix this.
— [Name]
```

Messenger follow-up:
```
Hi [Name], it's [name] from [brand]. I read your recommendation and want to make this right. Can you tell me when you originally reached out so I can find the thread on our end? I'm taking this over personally.
```

### "Recommends — beautiful packaging and shipped fast"

Public reply (amplify):
```
Hi [Name],

Thank you so much — and we love that you noticed the packaging. We obsess over the unboxing because it's the first 30 seconds of the product.
— [Name]
```

## Posting workflow

1. Buyer goes to Facebook Page → Reviews tab
2. Finds the recommendation
3. Clicks "Reply"
4. Pastes the public reply
5. (Separately) Opens the Page's Messenger inbox to send the private follow-up

For batches, Facebook's reply UI is one-at-a-time. Plan ~15 seconds per public reply + ~30 seconds per Messenger follow-up.

## Page-message restrictions

Facebook's Page Messaging policy restricts when a Page can message a user:
- **Within 24 hours of a message from the user**: Page can reply freely
- **After 24 hours**: Page can only send "approved message tags" (e.g., post-purchase update, account update) without paid promotion

If the customer's recommendation is older than 24 hours and they haven't messaged the Page, the Page may not be able to DM them directly. In that case, the public reply should offer email handoff instead:

```
Hi [Name],

We're sorry [specific]. Please send us a Messenger note or email hello@brand.com so we can fix this.
— [Name]
```

The skill detects the recommendation's age and adjusts the handoff offer accordingly.
