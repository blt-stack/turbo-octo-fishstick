# TikTok Ads Conventions

TikTok's ad system is video-first by design. Static image ads exist but are rarely the strongest format. The skill defaults to video-wrapper ads for TikTok unless the buyer specifies otherwise.

The defining trait of TikTok ads: they should not look like ads. The platform's algorithm and audience both punish ad-shaped content. The best-performing TikTok ads look like organic TikToks the algorithm happens to be promoting.

---

## Ad formats supported

### In-Feed Ads (standard)
- Lives in the For You feed alongside organic content
- 5-60 seconds vertical video
- 9:16 aspect ratio
- Caption + CTA button
- Spark format option (see below)

### Spark Ads
- Promotes an existing organic TikTok post (creator's or brand's)
- Performance is typically 2-3x better than non-Spark in-feed because the content is native
- Requires the creator's authorization (handled by skill #6's brief workflow)
- This is where most DTC TikTok ad spend goes

### TopView Ads
- Premium full-screen takeover format
- Auto-plays at app open
- Expensive (typically $50K+ minimum), used by large brands
- The skill generates copy for these but flags that the format requires significant ad-account spend tier

### Branded Effects, Branded Hashtag Challenges
- Out of skill scope (these require TikTok's creator team to set up)

---

## Character limits

| Field | Limit |
|---|---|
| Ad caption / display text | 100 characters (recommended; 2,200 max) |
| Display name (showed below the video) | 24 characters |
| CTA button text | Use TikTok's predefined list (see below) |

TikTok's display caption shows under the video and gets truncated past ~80 characters on mobile. Default to 80-100 chars.

---

## CTA button options (TikTok's allowed list)

- Shop Now
- Learn More
- Sign Up
- Download
- Watch More
- Book Now
- Order Now
- Contact Us
- Subscribe
- Apply Now

For DTC e-commerce: "Shop Now" is the default. "Learn More" works for higher-consideration products.

---

## Hook timing and structure (TikTok-specific)

TikTok's algorithm measures stop-rate aggressively in the first 1-2 seconds. The hook IS the ad's lever.

- **Spoken hook lands in second 1** (not second 2)
- **Visual hook** (the opening shot composition) sells before any spoken word
- **Text overlay** appears at frame 1
- **3-second rule:** if the viewer hasn't engaged by second 3, they've scrolled

TikTok-native hook patterns:

- POV setups: "POV: you finally find the pour-over that..."
- Direct address: "Stop scrolling if you've ever..."
- Curiosity gap: "I'd been making coffee wrong for years"
- Reaction: "They didn't tell me [X] when I bought this"
- Contrarian setup: "Espresso machines are over"

---

## What kills TikTok ads (rejection or downrank triggers)

### Auto-rejection categories

- **Same as Meta's prohibitions**, plus:
- **Profanity (even bleeped)** — TikTok is stricter than Meta
- **Stock-image-style visuals** — TikTok's algorithm downranks visually-polished-looking-like-an-ad content
- **External platform mentions** — "Follow me on Instagram" in a TikTok ad gets flagged
- **Watermarks from other platforms** — TikTok strips/penalizes Reels watermarks visible on uploaded content
- **Music rights violations** — paid TikTok ads MUST use TikTok's Commercial Music Library or licensed audio. Trending sounds = rights issue = rejection.

### Downrank (not outright rejection, but lower delivery)

- High-production-value content (looks like a commercial)
- Horizontal aspect ratio with black bars
- Direct response copy that's too salesy ("Buy now, today only!")
- Overly polished voiceovers (sound like radio ads)
- No native audio track (silent videos with text-only)

---

## What TikTok ads should look like (current best practice)

- **Native-feeling production**: phone-shot, slightly imperfect, real
- **Trending format adaptation**: the ad borrows a recognizable TikTok format (story-time, POV, day-in-the-life) but uses it for the product
- **Audio-on by default**: TikTok viewers expect sound; design accordingly
- **Captions visible**: many viewers still watch muted; captions on-screen
- **Hook in first 1-2 seconds**: visual + text + audio together
- **First-person creator voice**: "I bought this and..." outperforms third-person brand voice

---

## Spark Ads (most important DTC use case)

Spark Ads run an existing organic post (from the brand or a partnered creator) as paid. This is the highest-performing TikTok ad format for DTC because:

1. The content is already designed for TikTok's organic audience (native by definition)
2. Engagement metrics from the organic post (likes, comments, shares) get carried into the ad
3. Comments on the ad stay live and visible (social proof in real time)

### Brief structure for Spark Ads

When the buyer is wrapping copy around a creator's existing video (Spark from skill #6's UGC output), the ad copy structure is:

- **Caption (100 chars):** restated hook or value proposition (don't repeat the in-video hook verbatim)
- **CTA button:** typically "Shop Now"
- **Linked product URL** in the ad CTA destination

The skill generates the wrapper copy assuming the video itself is the heart of the ad.

---

## Whitelisted / Allowlisted Ads

Buyer runs ads through the creator's handle (more authentic, costs more in usage rights).

Same copy structure as Spark, but:
- Usage rights must be explicit (handled by skill #6's brief for the creator side; this skill just generates the wrapper copy)
- Comments come from the creator's audience, which can be a feature or a risk depending on the product

---

## Format adjustments per ad concept

### Static image ad on TikTok
- 9:16 vertical recommended (1080×1920)
- TikTok auto-pans/zooms static images to fake motion — design with that in mind (leave room top and bottom)
- Text overlay is critical (image-only ads underperform)
- Caption still 100 chars

### Video wrapper (most common)
- Caption (100 chars) wraps around the video
- Display name (24 chars) appears below — usually the brand name
- Caption can reference what the video shows ("watch how she pours it in 3 minutes")

### Carousel ads (TikTok's catalog-driven format)
- 2-10 images in a swipeable carousel
- Single caption (100 chars)
- Each card has its own image; no per-card text fields (different from Meta)

### Collection / Catalog ads
- Cover video + product feed below
- Caption (100 chars) + CTA button
- Products auto-pulled from the buyer's TikTok Catalog (set up in Business Center)

---

## Hashtags (caption)

TikTok hashtags work but should be minimal in paid:

- 2-3 hashtags max
- Mix: one product/category hashtag, one audience hashtag, optionally one branded hashtag
- Don't stuff or use unrelated trending tags — TikTok's algorithm flags this

The skill includes 2-3 suggested hashtags per concept in the brief.

---

## Buyer override behaviors

The skill defaults to:
- Spark-friendly copy (video-wrapper format)
- 100-char caption
- 2-3 hashtags
- Shop Now CTA

Buyer can override:
- "Static image ads on TikTok" → skill produces image ads with text-overlay design
- "Higher production value, brand-aware" → skill writes copy assuming polished production (still flags the algorithm downside)
- "No hashtags" → skill removes them
- "Different CTA" → skill respects the override (must pick from TikTok's list)
