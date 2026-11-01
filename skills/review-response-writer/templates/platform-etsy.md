# Platform: Etsy

Etsy's review culture is more community-flavored than other platforms. Buyers expect a personal-ish voice; sellers expect a relatively forgiving moderation environment. Etsy is also the most likely platform to remove off-topic and shipping-related negative reviews when properly reported.

## Reply visibility

- **Public:** Yes — appears under the review on the listing
- **Indexed:** Yes — Etsy reviews show in Google search and Etsy's own search
- **Edit/delete:** Yes, but limited — sellers can edit their reply once, then it locks
- **Reply quota:** One reply per review

## Character limit

Etsy doesn't publish an explicit limit, but the practical ceiling is ~500 characters. Replies over 500 characters get truncated in the buyer's mobile view, which is where ~70% of Etsy traffic happens.

Target: **40-90 words for recovery + clarify, 25-50 for amplify.**

## Tone register

**Personal, warm, slightly informal.** Etsy's shopper expects to be talking with a maker, not a corporation. First-person ("I" not "we") works well for solo Etsy sellers.

Match the brand's Etsy shop About page voice. If the About page says "Hi, I'm Maya and I throw every mug by hand," the reply should sound like Maya, not like a CS team.

## Reply structure (Etsy-specific)

For 1-2★ recovery:

```
Hi [First name],

I'm so sorry [specific issue]. Please send me a message through the conversation and I'll [send a replacement / refund / make it right].

Thank you for letting me know.
— [Seller name]
```

For 3★ clarify:

```
Hi [First name],

Thank you for the honest review. Would you mind sending me a message about [the friction]? I'd love to learn how to make it 5 stars next time.

— [Seller name]
```

For 4-5★ amplify:

```
Hi [First name],

Thank you so much! Knowing [specific praise] means a lot. So glad it found a good home.
— [Seller name]
```

## What's allowed on Etsy

- First-person language (most natural)
- Asking the customer to "message me" through Etsy's conversation tool
- Mentioning the handmade nature of the product
- Light personal storytelling ("This was one of the last in the indigo dye batch")
- Naming the maker (very common; expected for solo sellers)

## What's prohibited / risky

- External links (Etsy strips them out anyway)
- Asking for the review to be updated (TOS violation, similar to Amazon)
- Discount codes (TOS-allowed but considered cheap on Etsy)
- Mentioning other sellers / competitors
- Sharing customer's order details publicly
- Anything that reads like enterprise customer service

## Etsy-specific removal opportunities

Etsy removes negative reviews more readily than most platforms when they're:
- About shipping issues (Etsy considers shipping reviews off-topic by policy)
- About communication outside the product
- About a delay before the customer ever received the product
- Extortion-style ("Refund or 1 star")

The skill flags 1-2★ reviews that meet these criteria with a high-confidence dispute draft. See `dispute-drafts.md`.

## Etsy "private" feedback (between shop and Etsy)

Etsy has a separate path: the buyer can leave **private feedback** that only the seller sees. This isn't public; the skill doesn't draft replies to private feedback. If the buyer wants help responding to private feedback, recommend the Customer Service Reply Bot skill (#9) instead.

## Common Etsy review patterns

### "Took a long time to arrive" (Etsy removes these)

Public reply:
```
Hi [Name],

Sorry the shipping took longer than estimated — that's on the carrier, not on you. I've messaged you directly.
— [Seller]
```

Dispute draft: Etsy will remove on the grounds that shipping isn't covered under product reviews.

### "Didn't match the listing photo" (handle, don't dispute)

Public reply (recovery):
```
Hi [Name],

I'm sorry the [item] didn't match what you saw in the listing — the lighting can make [color/finish] read differently in photos. I'd love to send a different [size/color] or process a refund. Just message me.
— [Seller]
```

### "Item arrived broken" (handle + might be disputable if it's clearly carrier damage)

Public reply (recovery):
```
Hi [Name],

I'm so sorry it arrived damaged. I'm sending a replacement out this week at no charge — please message me to confirm the address.
— [Seller]
```

Dispute draft: Possible if the damage is clearly carrier-caused and the buyer can show packing photos; usually not worth pursuing.

### "Excellent quality and shop owner was lovely!" (5★ amplify)

Public reply (amplify):
```
Hi [Name],

You just made my morning. Thank you for choosing this piece — I hope it brings you years of joy.
— [Seller]
```

## Posting workflow

1. Buyer goes to Shop Manager → Listings → review section
2. Finds the review on the relevant listing
3. Clicks "Post a Public Response"
4. Pastes the drafted reply
5. Submits

For batches, Etsy doesn't support bulk reply — each is manual. Plan ~15 sec per reply.

## Posting cadence

Etsy review buyers tend to post in clusters around weekends and after promotional pushes. The skill's bulk mode is designed for these clusters. A typical Etsy seller might run a bulk batch once a week on Mondays.
