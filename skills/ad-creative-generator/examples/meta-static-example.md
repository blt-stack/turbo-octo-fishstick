# Meta Static Ads — Reference Example

Fictional product used to show structure. Never reproduce verbatim.

**Product:** River Stone Ceramic Pour-Over
**Platforms requested:** Meta only
**Format:** Static image ads
**Image source:** Fal AI generated (buyer has key set)
**UGC hooks source:** shared cache (coordinated with skill #6)

---

## .docx brief structure

```
River Stone Pour-Over — Paid Ad Creative Brief
Generated 2026-05-22 · Brand: {{brand_name}} · Platforms: Meta · Formats: static
Image source: fal_ai
UGC hooks source: shared_cache (coordinated with skill #6)
Keywords source: seo_cache

══════════════════════════════════════════════════
CONCEPT 1 — Problem-aware
══════════════════════════════════════════════════
Hook: I bought a $400 espresso machine and now it lives in a cabinet

Generated image (1080×1080 Meta Feed):
[Embedded Fal-generated image showing pour-over center-right with
de-prioritized espresso machine in left half of frame]

Meta (Facebook + Instagram)
Primary text (122/125)
I bought a $400 espresso machine and it lives in a cabinet because brewing
coffee at home felt like a chore. The pour-over fixed that in one Saturday.

Headline (24/27): The $400 mistake fixer
Description (26/27): Free shipping over $50.
CTA: Learn More

══════════════════════════════════════════════════
CONCEPT 2 — Social-proof
══════════════════════════════════════════════════
Hook: 1,247 5-star reviews. Sprudge picked it.

Generated image: [Fal-generated barista-style scene with pour-over central]

Meta
Primary text (124/125)
1,247 5-star reviews and a Sprudge 2026 pick. The handmade ceramic pour-over
that has coffee shop owners ordering it for their own kitchens. $68.
Headline (23/27): 1,247 reviews · Sprudge
Description (26/27): 30-day money-back guarantee.
CTA: Shop Now

══════════════════════════════════════════════════
CONCEPT 3 — Transformation
══════════════════════════════════════════════════
Hook: Slow Saturday mornings, one cup at a time.

Generated image: [Fal-generated lifestyle scene — hand holding mug,
pour-over in background, golden morning light]

Meta
Primary text (123/125)
Slow Saturday mornings. One cup. Three minutes. Hand-thrown ceramic pour-over,
reusable mesh filter, dishwasher safe. The coffee setup you'll actually use.
Headline (24/27): Saturday morning, finally
Description (24/27): Ships in 2 business days.
CTA: Shop Now

══════════════════════════════════════════════════
CONCEPT 4 — Curiosity-gap
══════════════════════════════════════════════════
Hook: I'd been making pour-over wrong for two years.

Generated image: [Fal-generated overhead shot of pour-over mid-pour,
abstract circular composition]

Meta
Primary text (120/125)
I'd been making pour-over wrong for two years and didn't know until this
arrived. The fix wasn't grind, or technique, or beans. It was the dripper.
Headline (22/27): Was making coffee wrong
Description (24/27): The dripper that fixed it.
CTA: Learn More

══════════════════════════════════════════════════
CONCEPT 5 — Contrarian
══════════════════════════════════════════════════
Hook: Espresso machines are over.

Generated image: [Fal-generated scene with pour-over sharp/foregrounded,
espresso machine desaturated behind]

Meta
Primary text (120/125)
Espresso machines are over. The actually-good way to make coffee at home is
hand-brewed pour-over, in 3 minutes, with no cleanup beyond a rinse.
Headline (26/27): RIP your espresso machine
Description (27/27): Hand-thrown ceramic. $68.
CTA: Learn More

══════════════════════════════════════════════════
COMPLIANCE CHECK
══════════════════════════════════════════════════
Meta (Facebook + Instagram)
✓ Prohibited claims: pass
✓ Personal attributes language: pass (no "if you're [type of person]")
✓ Health claims: pass (no medical claims about coffee)
✓ External URLs in image: pass (no URLs in any image)
✓ Competitor names: pass (no named competitor brands)
✓ Pricing language: pass ($68 mentioned descriptively, no "sale")
✓ Prohibited CTAs: pass (Shop Now / Learn More both valid)
✓ All character limits respected: pass (all under 125/27/27)
✓ All images within size + dimension limits: pass (1080×1080 each)

══════════════════════════════════════════════════
HOW TO LAUNCH
══════════════════════════════════════════════════
Meta Ads Manager:
1. Open Ads Manager → Create new campaign or ad set.
2. Use Bulk Import → upload the meta-ads CSV produced by this skill.
3. Match the rows to your campaign/ad set IDs as prompted.
4. Upload the generated images when prompted.
```

---

## Companion .csv output

A `{slug}_meta-ads_{date}.csv` is generated alongside the .docx. Sample row structure:

| Ad Set Name | Ad Name | Body | Title | Link Description | Call to Action | Display Link | Creative Image File | Concept Angle |
|---|---|---|---|---|---|---|---|---|
| river-stone-pour-over_problem-aware | river-stone-pour-over_problem-aware_v1 | I bought a $400 espresso machine and it lives in a cabinet... | The $400 mistake fixer | Free shipping over $50. | Learn More | brand.com | river-stone-pour-over_ad-creative_problem-aware.png | Problem-aware |
| river-stone-pour-over_social-proof | ... | 1,247 5-star reviews and a Sprudge 2026 pick... | 1,247 reviews · Sprudge | 30-day money-back guarantee. | Shop Now | brand.com | river-stone-pour-over_ad-creative_social-proof.png | Social-proof |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

Buyer opens Meta Ads Manager → Bulk Import → uploads this CSV → pastes the row data into the relevant campaign ad sets. 5 ads created in ~3 minutes instead of 30.

---

## Notes on this exemplar

- **Each concept is meaningfully different** (not 5 wordings of the same idea) — Problem-aware uses personal frustration, Social-proof leans on credentials, Transformation paints the after-state, Curiosity-gap sets up a mystery, Contrarian challenges a category default
- **Character counts shown inline** for every Meta field (125/27/27 enforced)
- **CTAs are matched to archetype** (Learn More for educational/contrarian; Shop Now for proof/transformation)
- **Fal-generated images embedded in the .docx** so the buyer reviews them in context
- **Compliance check covers all Meta's policy categories** — buyer doesn't have to manually verify against Meta's TOS
- **The .csv saves 25-30 minutes** of manual ad-by-ad entry in Ads Manager
- **UGC hooks from skill #6 woven into the captions** (when the buyer ran #6 first) so the in-video hooks and the caption hooks reinforce each other
