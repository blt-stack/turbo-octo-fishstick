# Meta Ads Conventions (Facebook + Instagram)

Meta's ad system covers Facebook Feed, Instagram Feed, Instagram Reels, Stories (both), Marketplace, and a few smaller placements. Most DTC ad spend goes to Feed + Reels. The skill defaults to those two unless the buyer specifies otherwise.

The most important constraint: **Meta's recommended character limits.** Over-limit copy gets truncated in the feed with a "...more" expansion that most users don't click. Truncation kills conversion.

---

## Recommended character limits (Meta's official guidance)

| Field | Recommended limit | Hard cap |
|---|---|---|
| Primary text (caption above the image/video) | **125 characters** | 2,200 |
| Headline (bold text below the image/video) | **27 characters** | 40 |
| Description / link description (small grey text) | **27 characters** | 30 |

The 125/27/27 numbers are Meta's "recommended" — they're the limits below which the copy displays in full on mobile feed (which is 80%+ of impressions). Above those limits, the copy truncates.

**The skill enforces these strictly.** If a draft goes over 125 / 27 / 27, the skill rewrites until it fits — even at the cost of a slightly less punchy line. A truncated punchy line beats a complete punchy line nobody finishes reading.

For long-form story-style ads (where the audience is warmer and willing to read), the buyer can override to use the 2,200-char cap. Default is the 125-cap.

---

## Placement-specific copy adjustments

Meta ads serve across placements. The same ad set can run on Feed, Reels, and Stories with different copy treatments. The skill generates per-placement copy when the buyer asks for it.

### Facebook Feed + Instagram Feed

- Primary text 125 chars
- Headline 27 chars
- Description 27 chars (mostly visible on desktop; truncated on mobile)
- Image or video, square (1080×1080) or vertical (1080×1350) — vertical wins for mobile
- Link preview card with the headline + description below the image

### Instagram Reels (Reels Ads)

- Primary text 125 chars (shows as caption below the Reel)
- No headline / description fields — Reels ads don't use them
- Video must be 9:16 vertical, 5-60 seconds
- The hook overlay text in the video itself does most of the conversion work (not the caption)
- CTA button (sticky at the bottom of the Reel)

### Stories Ads (both platforms)

- Primary text 125 chars (rarely shown — Stories are full-bleed)
- The image or video IS the ad (vertical 9:16, full-screen)
- Text overlay in the image/video does the conversion lifting
- "Swipe up" CTA (still called this internally even though the gesture changed to "tap")

### Marketplace

- More functional placement (less brand-driven)
- Image-led
- Copy should match the marketplace shopping mindset (price-conscious, comparison-driven)

---

## Compliance categories Meta auto-rejects

Auto-rejection happens at upload OR within 24 hours. Rejected ads burn spend and can flag the ad account.

### Personal attributes

Meta's policy bans implying the viewer has a body type, condition, or attribute — even when framed positively.

- ❌ "Are you overweight and tired of it?"
- ❌ "If you have [skin condition]..."
- ❌ "For people with anxiety..."
- ✅ Reframe: "If you want X..." / "Anyone who's looking for..."

### Health claims (especially supplements, beauty, fitness)

- ❌ "Cures," "treats," "prevents," "eliminates"
- ❌ "FDA approved" (unless verifiable with specific FDA approval)
- ❌ "Doctor recommended" (unless cited)
- ❌ "Lose 30 pounds in 30 days"
- ✅ Reframe: "Designed for," "may support," "made with [ingredient]"

### Before-and-after imagery

- Heavily restricted for body / weight categories
- Allowed only with subtle transformations + typical disclaimer
- The skill flags these and recommends alternative angles (process shots, lifestyle shots, third-party endorsement)

### Misleading claims / fake urgency

- ❌ "Only 3 left in stock!" (when there are 300)
- ❌ "Sale ends today!" (when the sale runs all year)
- ❌ "Limited edition" (when it's not)
- ✅ Real scarcity + real urgency is fine; manufactured scarcity gets flagged

### Politically charged or sensitive content

- Even tangential references to politics, crisis, war, addiction get flagged
- The skill avoids these entirely unless the buyer's product is genuinely in that category and they've gone through Meta's special ad authorization

### Other common rejection triggers

- Mentions of competitor brands by name (TOS violation)
- External URLs in the image/video itself (URLs go in the destination link, not the creative)
- Currency or financial promise language
- Profanity, even bleeped (Meta is less strict than TikTok on this, but still flags it)

---

## CTA button options (Meta's allowed list)

Pick one from this list — Meta enforces these as a hard list:

- Shop Now
- Learn More
- Sign Up
- Get Offer
- Download
- Book Now
- Apply Now
- Subscribe
- Contact Us
- See Menu
- Get Quote
- Watch More

For DTC e-commerce, "Shop Now" and "Learn More" cover 90% of cases. "Get Offer" works well for promo-led ads. The skill picks based on the archetype:

- Problem-aware → "Learn More" (the ad teaches; the click learns more)
- Social-proof → "Shop Now" (the proof has happened; convert now)
- Transformation → "Shop Now" or "Learn More" depending on price band
- Curiosity gap → "Learn More" (the ad sets up a question; the click answers it)
- Contrarian → "Learn More" (the ad makes a claim; the click investigates)

---

## Format adjustments per ad type

### Static image ads
- Copy structure: hook in primary text → benefit in headline → support in description
- Hook should also appear as text overlay on the image when the image is photographic enough to carry text
- Image dimensions: 1080×1080 sq or 1080×1350 vertical (vertical wins for Reels overlap)

### Video ads (when wrapping copy around UGC or produced video)
- Primary text is the caption; hook from the in-video opening line gets restated here (slightly remixed so they're not identical)
- Headline carries the value prop punchline
- Captions on the video itself are mandatory (most Meta viewers watch muted)
- Hook in the first 1-2 seconds of the video is the single highest-leverage element

### Carousel ads (2-10 cards)
- One overall caption (primary text 125 chars)
- One overall headline (used as the first card's headline; subsequent cards have per-card headlines)
- Per-card headline (27 chars each — yes, the 27-char limit applies per card)
- Per-card description (27 chars)
- Cards should tell a story or showcase a sequence (problem → solution → results → CTA), not just 10 product photos
- Last card is usually a CTA-driven recap

### Collection ads (Dynamic Product Ads / Catalog ads)
- Uses the buyer's product feed (Shopify connector or Meta Catalog)
- Wrapper copy: primary text + headline + cover image OR cover video
- The product cards beneath the cover come from the feed automatically
- The cover sells the brand / promo; the products do the variety

---

## What works in Meta DTC ads (current best practice)

- **UGC > polished studio** for cold-traffic Meta ads. Polished studio works better for retargeting.
- **First-second hook in video** is critical (Meta's algorithm measures stop-rate in seconds 1-2)
- **Captions on video** (muted-viewing default) — should be auto-generated AND manually edited for accuracy
- **Multiple creative variants per ad set** — Meta's algorithm picks the best one and serves it most. 3-5 variants per ad set is the sweet spot.
- **Refresh creative every 7-14 days** — Meta's algorithm picks creative fatigue fast; aggressive testing keeps CPMs down

These are buyer-side recommendations more than skill-side — the skill produces the creative; the buyer manages the campaign mechanics.

---

## Buyer override behaviors

The skill defaults to:
- 125/27/27 char limits enforced
- Feed + Reels placement copy generated
- Default CTA per archetype

The buyer can override:
- "Write me long-form copy (use the 2,200-char cap)" → skill uses up to 2,200 in primary text
- "Just Reels copy, skip Feed" → skill produces only the Reels treatment
- "Use Sign Up instead of Shop Now" → skill respects the override

Note all overrides in the brief so the buyer remembers what was generated.
