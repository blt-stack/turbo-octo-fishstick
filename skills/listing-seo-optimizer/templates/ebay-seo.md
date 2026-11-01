# eBay SEO (Cassini algorithm)

eBay's Cassini algorithm weights item specifics very heavily — more than most sellers realize. Title carries the next biggest weight, then description (only moderately). Selling history, return policy, and free shipping toggle also affect ranking — out of scope for this skill.

## Ranking factors (in rough order of impact)

1. **Item specifics completion** — fields like Brand, MPN, Model, Color, Size, Material. The single highest-leverage SEO lever on eBay.
2. **Title keyword match** — 80 chars to work with.
3. **Listing condition accuracy** — wrong condition flags can suppress.
4. **Free shipping toggle** — boosts ranking.
5. **Return policy length** — 30-day returns boost ranking.
6. **Sell-through rate** — out of scope for copy.
7. **Description keyword presence** — moderate weight.

## What this skill optimizes

### Title — hard cap 80 chars, target 75-80 chars
- Use all 80 chars if possible — eBay specifically gives a small ranking boost to listings using the full title length.
- Formula: `[Brand] [Model/Item Type] [Key Spec] [Condition] [Size/Color] [Generation/Year]`
- No symbols, no ALL CAPS, no "L@@K", no "WOW", no emoji.
- Skip filler words ("the", "a", "for", "from", "with").
- For used items: include condition word ("Used", "Refurbished") in the title.

### Item specifics — fill every category-specific field eBay offers
- This is where most ranking gains live. eBay categories often offer 15-30 specific fields; many sellers fill 3.
- Required fields (denoted with a red asterisk in Seller Center) must be filled — eBay suppresses listings missing required specifics.
- Recommended fields (no asterisk) are not required but heavily ranked. Fill them.
- Brand, MPN (manufacturer part number), Model, Type, Color, Size, Material, Style, Country/Region of Manufacture, Features — fill them all if they apply.

This skill should output a recommended item-specifics list as part of every eBay rewrite, even though the buyer enters the specifics in Seller Center's structured form (not in the description).

### Description — no hard limit, but mobile strips HTML
- Plain text or very simple HTML — most eBay traffic is mobile.
- Open with the condition statement (critical for trust).
- Bullets for key features.
- Be specific about condition: "Like new, used twice, one tiny scuff on bottom rim from storage" beats "very good condition."
- Mention return policy and shipping in plain text.
- For used items: cover any wear, missing pieces, repairs, modifications.
- For new items: cover what's in the box, original packaging condition, manuals/accessories.

### Condition notes (used/refurbished)
- Granular detail wins. Cassini boosts listings with thorough condition descriptions because they have lower return rates.

## Bullet-equivalent for eBay

eBay descriptions sometimes use bullets, but the *item specifics* are the real "structured field" surface. Score item specifics completion as the bullet-equivalent.

## Completeness checks (eBay-specific)

- Title uses ≥75/80 chars
- All required item specifics filled
- At least 80% of recommended item specifics filled
- Condition correctly assigned and elaborated in description
- At least 5 photos uploaded (eBay allows up to 24)
- Free shipping toggle on (if economically viable for the buyer)
- ≥30 day return policy (if buyer offers returns)

## Common pitfalls

- **Title under 70 chars.** Wasted opportunity.
- **Skipping non-required item specifics.** These are exactly where ranking gains live.
- **Over-promising condition.** "Mint" sets up returns. Be precise.
- **Decorative HTML in descriptions.** Stripped on mobile, looks broken.
- **Linking offsite.** TOS violation, can suppress listing.
- **ALL CAPS in title.** eBay flags as spammy, downranks.

## Rewrite output structure for eBay

```
EBAY — Rewrite

Title (XX/80): [...]

Item specifics (enter in eBay Seller Center → Item specifics):
Required:
- Brand: [...]
- MPN: [...]
- Model: [...]
- [other required for this category]
Recommended:
- Color: [...]
- Size: [...]
- Material: [...]
- Style: [...]
- Country/Region of Manufacture: [...]
- Features: [...]
- [other recommended for this category]

Condition: [New | Used | Refurbished | etc.]
Condition note: [granular description]

Description:
[plain prose]

[Bulleted features]

[Care/use notes if applicable]

Return policy: [if relevant]
Shipping: [if relevant]
```
