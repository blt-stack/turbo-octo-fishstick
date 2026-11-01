# Single Nano Instagram Outreach — Reference Example

Shows what gets produced when the buyer says "Draft outreach to @maya_brews on Instagram (4.2K followers), gifted only. Here are three of her recent captions: [pasted]."

**Brand:** {{brand_name}} (Brooklyn ceramics + coffee accessories — placeholder for buyer's brand)
**Creator:** @maya_brews
**Platform:** Instagram
**Tier:** Nano (1K-10K)
**Framework:** Gifted only
**Output:** Single `.docx`

---

## Input the buyer provided

```
Handle: @maya_brews
Platform: Instagram
Follower count: 4,200
Recent post 1 (caption):
  "Camping pour-over update — three failed mornings, one perfect one.
  Lessons: bloom matters. Grind matters. Water temperature matters
  but you can't really fix it on a backpacking stove. Worth it. 🏕️☕"

Recent post 2 (caption):
  "POV: you spend 6 hours researching beans and then drink instant
  coffee anyway because you forgot the filter. Why is this hobby
  like this."

Recent post 3 (caption):
  "small slow morning moment — first quiet hour before the kids wake up.
  Highly recommend."
```

---

## Step 1: Context extraction

The skill extracts six dimensions:

| Dimension | Extracted |
|---|---|
| Content themes | pour-over coffee, slow mornings, camping coffee, ironic-relatable hobby framing |
| Specific reference | The "three failed mornings, one perfect one" camping pour-over post |
| Products featured | None visible in 3 posts (clean) — no competitor partnership detected |
| Campaign signals | None — appears organic / hobbyist account |
| Voice signals | Casual, ironic-warm, lowercase ok, single-emoji accents, self-deprecating |
| Audience signals | 20-30s coffee enthusiasts, hobbyists with disposable income, possibly parents |

**Alignment score:** 9.2/10 — strong fit. Creator's content themes (pour-over + slow morning) directly align with the bundle being pitched.

---

## Step 2: Pitch selection

Bundle cache (skill #13) has a matching entry: `the-slow-morning-bundle.json` (Pour-Over + Filter Pack + Glass Carafe — $92 total individual).

Decision: pitch the bundle, not the single SKU. Bundle gives creator full kit to film with; aligns with creator's "complete setup" content style.

---

## Step 3: Framework selection

- Tier: nano (4.2K)
- Buyer specified: gifted only
- Cooling check: no prior cache entry; OK to outreach
- Confirmed: Gifted only, value $92

---

## .docx output structure

```
Outreach: @maya_brews
Platform: Instagram  ·  Tier: Nano (1K-10K)  ·  Followers: 4,200  ·  Generated: 2026-05-22
Relationship stage: new
```

### CREATOR CONTEXT

- Display name: Maya
- Niche: pour-over coffee + slow mornings
- Content themes: pour_over_coffee, camping_coffee, slow_mornings, ironic_relatable
- Voice register: warm_ironic_lowercase
- Brand alignment score: 9.2/10
- Alignment notes: Strong fit — content themes align with bundle composition; no competitor partnership detected in last 3 posts

### PITCH RECOMMENDATION

- Pitch type: bundle
- Product/Bundle: The Slow Morning Bundle (Pour-Over + Filter Pack + Glass Carafe)
- Pitch value (product cost): $92.00
- Why this fits: Bundle includes the three pieces needed for the "complete morning setup" content style the creator already makes — sending the bundle gives her everything she needs to film without asking for what to pair it with
- Payment framework: Gifted Only
- Rate offered: $0
- Tier rate range: $0 (nano gifted standard; product value $92)
- Expected reach: 2,500-5,000 impressions (15-20% engagement at 4.2K)

### INITIAL OUTREACH (paste-ready)

- Word count: 96 words

> hey maya — your camping pour-over update made me laugh in solidarity (the "bloom matters, grind matters, water temp impossible to fix on a backpacking stove" sequence felt extremely true). also the 6-hour research → instant coffee post was the most-me thing I've read all week.
>
> we make a small line of pour-over gear in Brooklyn and I'd love to send you our morning kit — the pour-over, our filters, and a carafe that fits 1L. no obligation to post; only if you actually love it after a few mornings.
>
> if open to it, drop me an address (or DM here) and I'll send it out. either way, keep making the slow morning content. 🙏
>
> — [signer first name]

### FOLLOW-UP VARIANTS (use if no reply)

**Follow-up A — send 7 days after initial**
> hey maya — bumping this in case it got buried. no pressure either way; just thought the kit would fit your style. let me know if you want me to send it. ✌️

**Follow-up B — send 14 days after initial**
> hey — figured i'd switch tactics. instead of just sending the kit, would you want to try our limited edition mug (just released) AND the brewing setup? same gifted basis, no asks attached. happy to ship either way.

**Follow-up C — send 28 days after initial**
> last one from me — if it's not your thing or the timing isn't right, totally fine. if it's a maybe-later, just say so and I'll circle back in a couple months. either way, your camping content is killing it.

### SUGGESTED DELIVERABLES STRUCTURE

- 1 organic post if creator chooses to post (no obligation under gifted framework)
- Standard timing: within 30-60 days of receiving product
- Usage rights: organic only; brand may repost to Story with credit
- Exclusivity: none

### DISCLOSURE REQUIREMENTS

- #gift or "gifted by [brand]" in caption — FTC material connection disclosure
- Branded Content toggle optional but recommended for nano gifted (not required by Instagram for gifted-only)
- Brand should NOT request "honest review" framing (FTC-fraught + signals unsophisticated)

Note: Standard for Gifted + Instagram

### NEXT STEPS

1. Send the initial outreach via instagram_dm.
2. Update influencer memory cache when reply arrives.
3. If no reply by 2026-05-29, deploy Variant A.
4. Track deliverables via the cache after the partnership confirms.

---

## Influencer memory cache write

Path: `~/.the-ecommerce-seller/cache/influencers/maya-brews.json`

```json
{
  "influencer_id": "maya-brews",
  "handle": "@maya_brews",
  "platforms": {
    "instagram": {
      "handle": "@maya_brews",
      "follower_count": 4200,
      "tier": "nano",
      "primary": true
    }
  },
  "content_themes": ["pour_over_coffee", "camping_coffee", "slow_mornings", "ironic_relatable"],
  "voice_register": "warm_ironic_lowercase",
  "niche": "pour-over coffee + slow mornings",
  "first_contact_date": "2026-05-22",
  "relationship_stage": "outreached",
  "outreach_history": [
    {
      "date": "2026-05-22",
      "channel": "instagram_dm",
      "outreach_type": "initial",
      "framework_offered": "gifted_only",
      "rate_offered_usd": 0,
      "product_offered": "The Slow Morning Bundle",
      "response_status": "no_reply"
    }
  ],
  "pending_responses": [
    {"outreach_date": "2026-05-22", "expected_response_by": "2026-05-29", "follow_up_due": "2026-05-30"}
  ],
  "post_context_history": [
    {
      "date_pasted": "2026-05-22",
      "post_excerpts": ["Camping pour-over update — three failed mornings...", "..."],
      "themes_extracted": ["pour_over_coffee", "camping_coffee", "slow_mornings"]
    }
  ],
  "alignment_score": 9.2
}
```

---

## Time savings

Manually drafting this outreach with the same level of personalization:
- Read + extract themes from 3 posts: 10-15 min
- Pick which bundle/SKU to pitch: 5-10 min
- Draft initial outreach with specific references: 15-25 min
- Draft 3 follow-up variants: 15-25 min
- Note disclosure requirements: 5 min
- Track in spreadsheet or memory file: 5-10 min
- **Total: 55-90 min per creator**

With this skill:
- Skill runs: ~3 seconds
- Buyer reviews + adjusts personal references: ~5 min
- **Total: ~5 min per creator**

Compounded across 20-30 nano outreach in a launch campaign, this is 20+ hours saved per launch with consistent personalization quality and cache continuity for follow-ups.
