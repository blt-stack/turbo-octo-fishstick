# Amazon Listing Format

Amazon strips formatting and rewards keyword-dense, scannable copy. Character limits are enforced — exceeding them gets the listing rejected or truncated.

## Structure

```
1. TITLE — Max 200 characters (some categories cap at 80-150; default to 200 unless category-specific limit known)
   - Formula: [Brand] [Product Type] [Key Feature 1] [Key Feature 2] [Size/Color/Quantity]
   - Use natural phrasing — Amazon's algorithm now penalizes keyword stuffing
   - First 80 chars matter most — they're what shows on mobile

2. BULLETS — 5 bullets, max 250 characters each
   - Open each bullet with a benefit in ALL CAPS or Title Case (~3-5 words)
   - Then a sentence or two explaining the feature behind it
   - Example: "ALL-DAY COMFORT — Memory foam insole molds to your foot within the first week, eliminating the break-in period most boots demand."

3. DESCRIPTION — Max 2000 characters (plain text, line breaks OK)
   - Lead with the elevator pitch
   - Cover materials, use cases, care, what's in the box
   - End with a soft brand statement, never a CTA (Amazon prohibits external CTAs)

4. BACKEND SEARCH TERMS — Max 250 BYTES (not characters — multi-byte chars count more)
   - Words, not phrases — Amazon tokenizes
   - No duplicates of words already in title/bullets
   - No competitor brand names (against TOS)
   - No promotional language ("best", "sale", "free shipping")
```

## Voice notes

- Voice gets compressed on Amazon. You have less room to be lyrical. Lean into the benefit-led angle and reserve story-led for the description section.
- Bullets are read, not skimmed. The first 3-5 words of each bullet should answer "what do I get?" — everything else supports it.
- Title voice is minimal — almost no room for personality. Focus on accuracy and keyword coverage.

## Pitfalls

- **Title over 200 chars** — listing gets suppressed.
- **Bullets that are pure features** — buyers scan for benefits. "100% Cotton" loses; "Breathable cotton you can wear from yoga class to dinner" wins.
- **CTAs in description** — "Buy now!", "Click here!", "Visit our website!" all violate Amazon TOS.
- **External URLs anywhere in copy** — also TOS violation.
- **Trademark symbols and ®, ™** — allowed only if you own the trademark. Don't add them by default.
- **Mentioning shipping speed, price, sales** — Amazon controls those, not your copy.
- **Backend search terms with phrases or quoted strings** — Amazon ignores them. Just space-separated unique words.

## Variant tactics

When generating two Amazon variants, lean on these pairs:
- Variant 1: Benefit-led title + feature-rich bullets
- Variant 2: Specification-led title (model number, size, count first) + benefit-led bullets

This gives the buyer two distinctly different listings to A/B test in Amazon Experiments.
