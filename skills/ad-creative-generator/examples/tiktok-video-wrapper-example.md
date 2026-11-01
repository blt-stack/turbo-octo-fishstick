# TikTok Video Wrapper Ads — Reference Example

Fictional product used to show structure. Never reproduce verbatim.

**Product:** River Stone Ceramic Pour-Over
**Platforms requested:** TikTok only
**Format:** Video wrapper (buyer has 5 creator videos from skill #6)
**Use case:** Buyer is running Spark Ads on TikTok, boosting the 5 creator-shot videos

---

## How this differs from the static example

- No image generation — the videos are shot separately (by creators briefed via skill #6)
- The skill writes the WRAPPER copy that lives around each video: caption, display name, hashtags, CTA
- One ad concept per creator-shot video, with archetype angle matched to each
- Shared UGC hooks cache means the caption's hook echoes (but doesn't repeat) the in-video hook

---

## .docx brief structure

```
River Stone Pour-Over — Paid Ad Creative Brief
Generated 2026-05-22 · Brand: {{brand_name}} · Platforms: TikTok · Formats: video_wrapper
Image source: n/a (videos provided by creators)
UGC hooks source: shared_cache (coordinated with skill #6)
Keywords source: seo_cache

══════════════════════════════════════════════════
CONCEPT 1 — Problem-aware (paired with @amyhouse's video)
══════════════════════════════════════════════════
In-video hook (from skill #6's brief, delivered by Amy):
"I bought a $400 espresso machine and now it lives in a cabinet because of this."

Wrapper copy:
TikTok Ads
Caption (95/100)
my $400 espresso machine lives in a cabinet now & i'm not even mad about it
Display name (24/24): handmade coffee studio
Hashtags: #pourover #coffee #morningroutine
CTA: Shop Now

Reference video: @amyhouse upload (delivered May 28, Spark-Ad authorized
through her account)

══════════════════════════════════════════════════
CONCEPT 2 — Social-proof (paired with @threecutekids's video)
══════════════════════════════════════════════════
In-video hook: "1,247 reviews said this is the pour-over that converted them"

Caption (86/100)
12k people switched. the pour-over they all ended up with is hand-thrown ceramic.
Display name (24/24): handmade coffee studio
Hashtags: #coffeeoftiktok #pourover #kitchenfinds
CTA: Shop Now

Reference video: @threecutekids upload

══════════════════════════════════════════════════
CONCEPT 3 — Transformation (paired with @lifestylebymeg's video)
══════════════════════════════════════════════════
In-video hook: "Slow Saturday mornings start exactly like this"

Caption (58/100)
mornings hit different when you actually want to make coffee
Display name (24/24): handmade coffee studio
Hashtags: #slowmorning #coffeeoftiktok #pourover
CTA: Shop Now

Reference video: @lifestylebymeg upload

══════════════════════════════════════════════════
CONCEPT 4 — Curiosity-gap (paired with @coffeebysamantha's video)
══════════════════════════════════════════════════
In-video hook: "I've been making pour-over wrong for two years"

Caption (72/100)
turns out i'd been making pour-over wrong for years. it was the dripper.
Display name (24/24): handmade coffee studio
Hashtags: #coffeehacks #pourover #morningcoffee
CTA: Learn More

Reference video: @coffeebysamantha upload

══════════════════════════════════════════════════
CONCEPT 5 — Contrarian (paired with @nightowlbarista's video)
══════════════════════════════════════════════════
In-video hook: "Espresso machines are over. Hand-brewed coffee is the actually-good way."

Caption (45/100)
unpopular opinion: espresso machines are over
Display name (24/24): handmade coffee studio
Hashtags: #unpopularopinion #coffee #pourover
CTA: Learn More

Reference video: @nightowlbarista upload

══════════════════════════════════════════════════
COMPLIANCE CHECK
══════════════════════════════════════════════════
TikTok Ads
✓ Profanity (even bleeped): pass
✓ Prohibited claims: pass
✓ External platform mentions: pass (no "follow me on Instagram")
✓ Music rights (videos use Commercial Music Library per skill #6's brief): pass
✓ Personal attributes: pass
✓ All character limits respected: pass

══════════════════════════════════════════════════
HOW TO LAUNCH
══════════════════════════════════════════════════
TikTok Ads Manager:
1. TikTok Business Center → Ads Manager → Bulk Tools.
2. Upload the tiktok-ads CSV produced by this skill.
3. For each ad, link the corresponding creator's authorized video (Spark Ad authorization should already be set up per skill #6's brief workflow).
4. Set targeting + budget at the ad group level.
5. Launch.
```

---

## Companion .csv output

A `{slug}_tiktok-ads_{date}.csv` is generated. Sample structure:

| Campaign Name | Ad Group Name | Ad Name | Ad Text | Display Name | CTA Button | Hashtags | Video File | Landing Page URL | Concept Angle |
|---|---|---|---|---|---|---|---|---|---|
| river-stone-pour-over_campaign | river-stone-pour-over_problem-aware_group | river-stone-pour-over_problem-aware_v1 | my $400 espresso machine lives in a cabinet now... | handmade coffee studio | Shop Now | #pourover #coffee #morningroutine | REPLACE_WITH_VIDEO_PATH | brand.com/pour-over | Problem-aware |
| river-stone-pour-over_campaign | river-stone-pour-over_social-proof_group | ... | 12k people switched... | handmade coffee studio | Shop Now | #coffeeoftiktok #pourover #kitchenfinds | REPLACE_WITH_VIDEO_PATH | brand.com/pour-over | Social-proof |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

Buyer replaces the `REPLACE_WITH_VIDEO_PATH` column with paths to each creator's authorized Spark Ad video, then bulk-uploads to TikTok Ads Manager.

---

## Notes on this exemplar

- **Each caption echoes — but doesn't repeat — the in-video hook**. Repeating would feel redundant; echoing reinforces the angle
- **TikTok-native voice**: lowercase, casual punctuation, sentence fragments — feels like organic TikTok, not corporate ads
- **Hashtags kept to 3 per ad** (TikTok algorithm penalizes hashtag stuffing)
- **Display name kept consistent across ads** (24-char limit, "handmade coffee studio")
- **CTAs picked by archetype**: Shop Now for Problem-aware/Social-proof/Transformation; Learn More for Curiosity-gap/Contrarian
- **No music rights notes needed in this brief** — skill #6's brief already specified Commercial Music Library, so creators delivered Spark-Ad-safe videos
- **The .csv saves 20+ minutes** of TikTok Ads Manager entry
