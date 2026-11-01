# Google Ads (Search RSA + PMax) — Reference Example

Fictional product used to show structure. Never reproduce verbatim.

**Product:** River Stone Ceramic Pour-Over
**Platforms requested:** Google Ads (Search RSAs + Shopping titles + Performance Max)
**Image source:** Fal AI generated (for PMax image assets)
**Keywords source:** Listing SEO Optimizer cache (skill #2)

---

## How Google output differs from Meta/TikTok

- **Keyword-driven**: heavy integration with skill #2's keyword cache
- **Structured fields**: 15 headlines + 4 descriptions per RSA (Google's algorithm assembles combinations)
- **Multi-surface**: RSAs (Search), Shopping titles (Merchant Center feed), PMax asset groups (everything else)
- **No "concepts per archetype" the same way** — Google ads are keyword-targeted, so archetypes inform variety within the 15 headlines rather than producing 5 separate ad concepts

---

## .docx brief structure

```
River Stone Pour-Over — Paid Ad Creative Brief
Generated 2026-05-22 · Brand: {{brand_name}} · Platforms: Google · Formats: search_rsa, shopping_title, pmax_asset_group
Image source: fal_ai
UGC hooks source: shared_cache (not used for Google — kept independent)
Keywords source: seo_cache (15 keywords pulled from skill #2's cache for this product)

══════════════════════════════════════════════════
RESPONSIVE SEARCH AD (RSA) — Master ad for "ceramic pour over" keyword group
══════════════════════════════════════════════════

Campaign: river-stone-pour-over_search_campaign
Ad group: river-stone-pour-over_ceramic_pour_over_adgroup
Final URL: brand.com/pour-over
Path 1: Pour-Over   (12/15)
Path 2: Handmade    (8/15)

Headlines (15 total — Google's algorithm picks combinations per query):

  H1 (pinned to position 1): Ceramic Pour Over Coffee Dripper (32 — over by 2, will trim)
  H1 (pinned to position 1, revised): Ceramic Pour Over Coffee     (27/30)
  H2: Handmade Pour Over - One Cup        (27/30)
  H3: Hand-Thrown in Portland             (24/30)
  H4: Reusable Filter Included            (26/30)
  H5: 1,247 5-Star Reviews                (21/30)
  H6: Free Shipping Over $50              (24/30)
  H7: Brews One Cup in 3 Minutes          (28/30)
  H8: Dishwasher Safe Pour Over           (26/30)
  H9: No Paper Filter Ever Again          (28/30)
  H10: Stoneware Holds Heat Longer        (28/30)
  H11: Made by Three People               (21/30)
  H12: The Pour Over We Make Daily        (28/30)
  H13: 30-Day Money-Back Guarantee        (28/30)
  H14: Single-Cup Pour Over Setup         (28/30)
  H15: Slow Coffee, Done Right            (24/30)

Descriptions (4 total):

  D1 (88/90): Hand-thrown ceramic pour-over with a reusable mesh filter. Brews one cup in 3 min. Shop now.
  D2 (86/90): Made in our Portland studio. Dishwasher safe stoneware that lasts. Free shipping over $50.
  D3 (89/90): Stop buying paper filters. Stainless mesh included with every pour-over. 30-day returns.
  D4 (87/90): Slow-craft coffee gear for the morning when you want one good cup, not five fast ones.

══════════════════════════════════════════════════
SHOPPING AD TITLE — for Google Merchant Center feed
══════════════════════════════════════════════════

{{brand_name}} Ceramic Pour Over Coffee Dripper Handmade Stoneware
Single Cup Reusable Filter
(97 characters)

Notes:
- Front-loads brand + product (Google Shopping algorithm weights early
  words higher)
- Includes 3 high-priority keywords: ceramic pour over, handmade, reusable
  filter
- No promotional language (would cause Google to reject)
- No symbols / ALL CAPS

When to update: when a new keyword surfaces in skill #2's cache that ranks
higher than the current 3 — rebuild this title.

══════════════════════════════════════════════════
PERFORMANCE MAX (PMAX) ASSET GROUP
══════════════════════════════════════════════════

Asset group name: river-stone-pour-over_pmax_asset_group

Final URL: brand.com/pour-over

Headlines (15 total — same as RSA above, slightly tuned for PMax broader audience):
[15 headlines listed]

Long headlines (3 of 5 max):
LH1 (88/90): Hand-thrown ceramic pour-over coffee dripper with reusable mesh filter included
LH2 (78/90): The handmade pour-over for slow mornings — one perfect cup in 3 minutes
LH3 (84/90): 1,247 5-star reviews. Made in Portland. Dishwasher safe ceramic stoneware.

Descriptions (4 of 5 max):
[same 4 as RSA]

Business name (22/25): handmade coffee studio

Image assets (4 aspect ratios — generated via Fal AI):
[Embedded image: river-stone-pmax_1200x628.png — 1.91:1 horizontal hero]
[Embedded image: river-stone-pmax_1200x1200.png — 1:1 square]
[Embedded image: river-stone-pmax_720x1280.png — 9:16 vertical]
[Embedded image: river-stone-pmax_960x1200.png — 4:5 portrait]

Logo assets (uses buyer's logo — not generated):
- 1:1 logo at 1200×1200 (buyer to provide)
- 4:1 wide logo at 1200×300 (buyer to provide)

Audience signals (configured in Google Ads, not via this brief):
- Keyword themes: ceramic pour over, handmade coffee, slow coffee ritual, single cup brewer (4 themes from skill #2's top 10)
- Remarketing lists: site visitors past 30 days
- Custom intent audiences: searched "pour over coffee" past 7 days

══════════════════════════════════════════════════
COMPLIANCE CHECK
══════════════════════════════════════════════════
Google Ads
✓ Misrepresentation: pass
✓ Competitor brand keywords in copy: pass (no named brands mentioned)
✓ Trademark violations: pass (no trademarked terms used)
✓ Phone numbers in copy: pass (none)
✓ Excessive capitalization / symbols: pass
✓ Repeated punctuation: pass
✓ Health / medical claims: pass (no coffee health claims)
✓ All character limits: pass

══════════════════════════════════════════════════
HOW TO LAUNCH
══════════════════════════════════════════════════
Google Ads Editor:
1. Open Google Ads Editor (desktop app).
2. Account → Import → CSV → upload the google-ads CSV produced by this skill.
3. Review imported entries → Post Changes.

Google Merchant Center (Shopping ad):
1. Open Merchant Center → Products → Edit the SKU for River Stone Pour-Over.
2. Replace the existing title with the optimized title from this brief.
3. Save. The new title propagates to Shopping ads within ~24 hours.

Performance Max:
1. Open Google Ads → Campaigns → New Campaign → Performance Max.
2. Create asset group with the headlines, long headlines, descriptions,
   business name, and uploaded image assets from this brief.
3. Configure audience signals as listed above.
4. Set budget and launch.
```

---

## Companion .csv output

A `{slug}_google-ads_{date}.csv` is generated for Google Ads Editor bulk import. Sample row structure (one row per ad, with all 15 headlines and 4 descriptions inline):

| Campaign | Ad group | Ad type | Headline 1 | Headline 2 | ... | Headline 15 | Description 1 | ... | Description 4 | Path 1 | Path 2 | Final URL | Concept Angle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| river-stone-pour-over_search_campaign | river-stone-pour-over_ceramic_pour_over_adgroup | Responsive search ad | Ceramic Pour Over Coffee | Handmade Pour Over - One Cup | ... | Slow Coffee, Done Right | Hand-thrown ceramic pour-over... | ... | Slow-craft coffee gear... | Pour-Over | Handmade | brand.com/pour-over | Multi-archetype |

For Google's RSA format, the 5-archetype concept count condenses into a single RSA ad with the archetype variety expressed across the 15 headlines (rather than 5 separate ads).

---

## Notes on this exemplar

- **15 headlines cover 5 archetypes**: 3 headlines per archetype on average (with the first 3 pinned to the primary keyword)
- **Headlines come from skill #2's keyword cache** (when present) — that's the integration win
- **Shopping title is a single optimized title**, not 5 variants (Google Shopping doesn't A/B test titles the way Meta tests creative)
- **PMax requires 4 image aspect ratios** — Fal generates the primary 1.91:1 and 1:1; the brief flags the 9:16 and 4:5 as Canva-crop briefs from the source images
- **Audience signals are documented but configured in Google Ads UI** (not in the CSV) — Google's PMax doesn't accept audience signals via CSV import
- **Compliance check passes Google's standard policy categories** — keyword stuffing, prohibited claims, formatting violations all auto-verified
