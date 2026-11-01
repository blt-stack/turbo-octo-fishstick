# Narrative Craft — Brand-Voice-Aware Tone

The digest is read every morning. It should feel like a competent operations partner is briefing the founder — not a dashboard, not a data dump, not a corporate report.

## The narrative principles

### 1. Lead with the number, then the meaning

Bad:
> "When we examine yesterday's performance, we find that revenue was..."

Good:
> "Revenue: $4,500 yesterday. Down 18% DoD. Within normal variance."

The founder is scanning. They want the number, then the context, then the implication.

### 2. State anomalies plainly

Bad:
> "We observed certain metrics that may be worth investigating further..."

Good:
> "Anomaly: ROAS dropped to 1.8x from 3.2x baseline (2.9σ below). Investigation needed: the cold prospecting campaign appears creative-fatigued."

The word "anomaly" or "flagged" is fine. So is "investigation needed." Hedging words ("perhaps," "may be," "worth considering") get cut.

### 3. Offer hypotheses, never conclusions

Bad:
> "Yesterday's revenue drop was caused by the broken checkout flow."

Good:
> "Yesterday's revenue drop coincides with a checkout-funnel drop of 9 percentage points. Likely cause: checkout error or shipping rate change. First check: the most recent Shopify settings change in the audit log."

The digest never knows the cause with certainty. It surfaces correlations and suggests where to look. The buyer investigates.

### 4. Quantify with units

Every number gets units:

- "$4,500" not "4500"
- "47 orders" not "47"
- "2.58%" not "0.0258"
- "2.9σ below baseline" not "2.9 standard deviations"

### 5. Direction symbols

Use compact directional indicators where they aid scanning:

- `↑` / `↓` for direction
- `+/-X%` for magnitude
- `Nσ` for z-score (with `↑` or `↓`)

Don't use these when they make the text harder to read. Prose flows better in long sentences; symbols flow better in bullet lists.

### 6. Avoid corporate hedging language

Cut these phrases:
- "It appears that..."
- "It might be worth considering..."
- "One could argue..."
- "Generally speaking..."
- "At the end of the day..."
- "Moving forward..."
- "Synergy" / "leverage" / "pivot" / "circle back"

Replace with direct statements.

## Brand voice adaptation

The digest reads `config.brand_voice` and adjusts tone:

### Brand voice: "warm" / "conversational" (lifestyle brands, hobby-niche brands)

> "Yesterday was a quiet one — revenue tracked within normal range and no anomalies surfaced. The pour-over had a strong day (18 units, well above its 12-unit baseline) which is consistent with the Memorial Day email push. Today's main thread: the Shenzhen Stoneworks response is overdue, and the Slow Morning bundle is still sitting undeployed."

### Brand voice: "professional" / "business" (B2B, premium brands, corporate-feel)

> "Revenue: $4,500. Tracking within normal variance vs. 7-day baseline. ROAS held at 3.0x — within acceptable range. Two items require attention: Shenzhen Stoneworks response is 4 days overdue (MOQ reduction letter sent 2026-05-15), and the Coffee Brewing Set bundle remains undeployed despite a composite score of 84.3/100."

### Brand voice: "punchy" / "casual" (consumer brands targeting younger demos)

> "Quiet day. $4,500, basically normal. Pour-over had a strong day (good email pull). Two things on the docket: Shenzhen's been quiet on the MOQ ask (4 days overdue), and we still haven't pulled the trigger on the Coffee Bundle (it's a solid one — should ship it)."

### Brand voice: "formal" / "luxury"

> "Yesterday's sales totaled $4,500.50, within standard variance against the trailing seven-day baseline. The brand's flagship pour-over performed strongly, with 18 units sold — well above its typical 12-unit pattern. Two items merit immediate attention: the response from Shenzhen Stoneworks regarding the requested MOQ adjustment is overdue by four days, and the previously developed Coffee Brewing Set bundle remains undeployed."

The base structure is identical across voices. Only word choice and rhythm shift.

## Founder-style adaptation

In addition to brand voice, the digest can adjust to founder preference via `config.daily_store_digest.founder_style`:

| Style | Tone characteristics |
|---|---|
| `terse` | Cut all narrative; use bulleted facts only |
| `analytical` | Include hypothesis chains + cross-references |
| `narrative` | Connect numbers to story (what happened and why) |
| `coachly` | Frame as next-action recommendations |

Defaults to `narrative` if not specified.

## Length discipline

The whole digest should be readable in **5-10 minutes** by a founder over coffee. Section lengths:

- Header + verdict + summary: 3-5 sentences
- Revenue section: 3-5 short paragraphs
- Anomalies section: 1 sentence per anomaly + 1-2 sentence likely cause
- Channel breakdown: short table + 1-2 sentences
- Top SKUs: bulleted, ≤7 lines per group
- Email section: 2-4 short paragraphs
- Ads section: 3-6 short paragraphs
- Traffic section: 2-4 short paragraphs
- Cross-skill queue: bullet lists; never more than 5 items per source
- Suggested actions: ≤5 numbered items

If a section feels long, the rule is: **cut the explanatory sentences, keep the data and the action.**

## What the digest never does

- Never editorializes ("This is concerning," "This is great news")
- Never assigns blame ("Marketing dropped the ball")
- Never compares to vague benchmarks ("industry average is...")
- Never promises future ("If we keep going at this rate...")
- Never repeats data already shown in an earlier section
- Never offers wellness advice or motivational framing
- Never explains what a metric is mid-narrative ("CPM, which means cost per thousand impressions...")

## When the digest is uncertain

The digest is **uncertain by default** about causes and **certain** about numbers:

- Numbers: stated as facts (they ARE the data)
- Anomalies: stated as flags (the metric IS outside the baseline)
- Causes: stated as hypotheses ("Likely cause...", "First place to check...")
- Recommendations: stated as recommendations ("Recommend...", "First action...")

The founder makes the decision. The digest informs.
