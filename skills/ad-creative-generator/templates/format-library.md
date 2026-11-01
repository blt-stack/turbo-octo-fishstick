# Ad Format Library

Four creative formats supported. Each has its own structural conventions, image requirements, and copy distribution.

The buyer can request any combination of formats per run. The skill default is static image (simplest, most common) unless the buyer specifies otherwise.

---

## Format 1: Static image ad

The simplest paid format. One image + copy. Most common for cold-traffic Meta and Pinterest. Less common on TikTok (where video dominates).

### Image specs per platform

| Platform | Recommended dimensions | Aspect ratio |
|---|---|---|
| Meta Feed (FB+IG) | 1080×1080 (square) or 1080×1350 (vertical) | 1:1 or 4:5 |
| Meta Stories / Reels | 1080×1920 (vertical) | 9:16 |
| TikTok (rare) | 1080×1920 (vertical) | 9:16 |
| Google Display (PMax) | 1200×628 (horizontal), plus square + vertical | 1.91:1, 1:1, 4:5, 9:16 |
| Pinterest | 1000×1500 (vertical) | 2:3 |

The skill generates Meta's 1080×1080 + 1080×1350 by default, plus 1080×1920 for Reels/Stories. For Google PMax, all four aspect ratios. For Pinterest, the 2:3 vertical.

### Composition rules

- **Subject occupies 50-60% of frame** (any less and it gets lost in mobile feeds)
- **High contrast** between subject and background (mobile screens, sunlight readability)
- **Text overlay supports the visual** (it doesn't have to do all the selling — the image and the caption do most of it)
- **Brand colors used sparingly** (over-branding signals "ad"; under-branding loses recognition)
- **One clear focal point** (no busy layouts)

### Copy distribution for static image ads

- **Primary text (caption above image):** hook + value prop. Carries most of the conversion lift.
- **Headline (below image, bold):** the punchline. 27 chars on Meta, similar across.
- **Description (small grey text):** support / context. Often missed by readers.
- **Text overlay on image:** the hook re-stated visually. Should match the primary text's hook but not be identical word-for-word.

### When to use static image

- Cold-traffic Meta ads where production budget is limited
- A/B testing copy with the same image
- Retargeting (warm audience doesn't need video)
- Pinterest (still image-led)
- Google Display + PMax

### When NOT to use static image

- TikTok (algorithm punishes static-feeling content)
- High-consideration products where the buyer needs to see the product in motion
- Demo-heavy products (a video shows in 10 seconds what a static image can't in any number of words)

---

## Format 2: Video wrapper

The skill writes the copy that wraps around a video the buyer is providing (typically from skill #6's UGC creator brief or from in-house production). The skill does NOT generate the video itself.

### What the skill produces

- **Caption / primary text:** what appears above the video (Meta) or as the display caption (TikTok)
- **Headline:** appears below the video on Meta Feed
- **Description:** small grey text on Meta Feed
- **CTA button:** platform's allowed list
- **Thumbnail / cover-frame text overlay:** the first-frame text that appears before the viewer taps play
- **Recommended end-card text:** if the video ends with a CTA frame, what it should say

### Video specs (per platform — for the buyer to brief the shooter)

| Platform | Duration | Aspect ratio | Audio | Captions |
|---|---|---|---|---|
| Meta Feed | 5-90s, sweet spot 15-30s | 1:1 or 4:5 | Yes | Mandatory (auto + edit) |
| Meta Reels | 5-60s, sweet spot 15-30s | 9:16 | Yes | Mandatory |
| Meta Stories | 5-15s per clip | 9:16 | Yes | Mandatory |
| TikTok | 5-60s, sweet spot 15-30s | 9:16 | Yes (sound-on platform) | Yes |
| YouTube Shorts | 5-60s | 9:16 | Yes | Recommended |
| Google PMax video asset | 6-30s | 16:9, 9:16, 1:1 | Yes | Yes |

### Coordination with skill #6

When skill #6 has been run for this product, the skill reads the in-video hooks from the shared UGC cache and writes wrapper copy that:

- Doesn't repeat the in-video hook verbatim in the caption (would feel redundant)
- Echoes the hook's archetype but in a different sentence
- Adds a value-prop point not made in the video
- Carries the CTA the video implies

When skill #6 hasn't been run, the skill writes the wrapper copy as if the video is generic UGC and the caption needs to do more of the lifting.

### When to use video wrapper

- The buyer has UGC footage from creator briefs
- The buyer has produced video content (commercial, demo, founder talking head)
- For TikTok (almost always)
- For Reels / Shorts (almost always)

### When NOT to use video wrapper

- The buyer doesn't have video and won't have it before the ad needs to launch (use static image)

---

## Format 3: Carousel ads (2-10 cards)

Multiple images / videos in a swipeable sequence. Each card has its own visual + headline + (usually) description.

### Card count guidance

- **2-3 cards:** quick A/B comparison or product variant showcase
- **4-6 cards:** feature-by-feature breakdown OR before/after sequence OR multi-product upsell
- **7-10 cards:** rare — usually catalog showcases. Most carousel attention drops after card 4.

The skill defaults to 5 cards: one per archetype angle as 5 mini-ads in the carousel sequence. Buyer can override.

### Card structure

Each card has:
- **Image or short video** (per-card visual)
- **Headline** (27 chars on Meta; per-card)
- **Description** (27 chars on Meta; per-card)
- **Destination URL** (per-card — can deep-link to different product pages)

Plus an overall:
- **Primary text / caption** (125 chars on Meta; for the carousel as a whole)
- **Display URL**

### Composition rules for carousel

- **Cards should form a sequence**, not random product photos
- **First card sets up the story; last card delivers the CTA**
- **Visual consistency across cards** (same lighting, same style — like a magazine spread, not a thrift-store shelf)
- **Each card answers a different question**

### When to use carousel

- Multi-product showcases (5 SKUs in one ad)
- Before/after sequences
- Feature-by-feature breakdowns
- Category-spanning brand ads (showing brand range)
- When testing multiple visual angles for the same product

### When NOT to use carousel

- Single-product ads with one clear hero shot (static beats carousel)
- TikTok-native ads (carousel is a Meta/Pinterest format)
- High-consideration where each card needs its own substantial story (video beats carousel)

---

## Format 4: Collection / Catalog ads (Dynamic Product Ads)

Catalog-driven format. The buyer's product feed (Shopify Catalog → Meta Catalog or TikTok Catalog) populates the products beneath a cover image or video.

### What the skill produces

- **Cover creative:** the image or video that sits at the top of the ad
- **Primary text / caption** (125 chars)
- **Headline** (27 chars on Meta)
- **CTA button**

The products beneath the cover are dynamically populated from the buyer's catalog. The skill doesn't write per-product copy for these — the catalog has its own field structure for that.

### When the skill is most useful for Collection ads

- The buyer has a catalog of 10+ SKUs
- The buyer wants to advertise "the collection" or "the brand" rather than one specific SKU
- The buyer is running retargeting based on catalog browsing

### What the skill flags to the buyer

- Catalog ads require a working product feed (Shopify-to-Meta sync, TikTok Business Center catalog upload). If the buyer hasn't set this up, the skill flags it as a prerequisite.
- The product feed's own field copy (product titles, descriptions, prices) determines per-product appearance. Skill #1 (Product Description Writer) is the right place to optimize per-product copy.

### When NOT to use Collection / Catalog ads

- Buyer has fewer than 5 SKUs (use static image or video instead)
- Buyer doesn't have a connected product feed
- Buyer is launching a single new product (use static or video wrapper for the launch)

---

## Format combinations per run

Buyer can pick multiple formats. The skill produces a section in the brief per format, with copy per archetype within each format.

### Common combinations

- **Static image + video wrapper** (test which format works for the same archetype angle)
- **Static image only** (lowest production cost; most common for testing)
- **Video wrapper only** (buyer already has video and just needs the ad copy)
- **All four** (rare — typically only when the buyer is launching a major campaign with significant budget)

### When the buyer asks for all four

The .docx brief gets long (5 concepts × 4 formats × per-platform copy = 60+ copy variants). The skill organizes the brief by archetype first, then by format within each archetype, then by platform within each format. This keeps a single archetype's full ad treatment in one section so the buyer can review one concept at a time.

---

## Default behavior when format isn't specified

The skill defaults to **static image** for Meta and Google, and **video wrapper** for TikTok (since TikTok rarely uses static).

If the buyer's brand voice is video-heavy (per `config.brand_voice`), the skill suggests video wrapper as the default and asks if buyer has video footage available. If not, falls back to static image.
