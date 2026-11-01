# Follow-up Cadence

Three follow-up variants per outreach, deployed at different intervals based on creator tier.

## The 3 follow-up variants

### Variant A: Soft nudge (first follow-up)

Light bump. References the original message. No pressure.

Structure:
- "Just wanted to bump this in case it got buried"
- Brief re-anchor of the offer
- No additional pressure or new info

Example (nano IG):
> "Hi Maya — just bumping this in case it got buried in your DMs. Still happy to send the brewing kit if it's a fit. No worries if not. Best, Jamie"

Length: 20-50 words.

### Variant B: Reframed offer (second follow-up)

Different angle on the same opportunity. Slightly different deliverables, timing, or framing.

Examples of reframing:
- Different deliverables ("if a Reel isn't your style, happy to discuss Story-only or a one-image post")
- Different timing ("if you're booked this month, no rush — we can plan for [later month]")
- Different framing ("if 'partnership' feels too commercial, we'd just send the product as a thank-you for your work and see what happens")
- Different product ("we have a couple of other things if the brewing kit isn't the right fit")

Example (micro IG):
> "Hi Maya — circling back on the brewing kit. If the Reel format isn't your usual style, happy to discuss Story-only or a single post. Also if timing's tight, we're flexible — could plan for Q3 instead. Just want to find what fits. Best, Jamie"

Length: 50-100 words.

### Variant C: Final ask (third follow-up)

Clear "if not a fit, no worries" close. Gives the creator an easy out + leaves the door open for future.

Structure:
- Acknowledge the silence
- Confirm not pressing further
- Leave the door open
- Brief and warm sign-off

Example:
> "Hi Maya — I'll stop bumping this thread now. If a partnership doesn't fit for you right now, totally understand. We'll be around if anything changes. Best, Jamie"

Length: 25-50 words.

## Cadence by tier

| Tier | First → Variant A | Variant A → B | B → C |
|---|---|---|---|
| Nano | 5-7 days | 10-12 days | 18-21 days |
| Micro | 7-10 days | 14-17 days | 25-30 days |
| Mid-tier | 10-14 days | 21-28 days | 35-45 days |
| Macro | 14-21 days | 30-45 days | 60-90 days |

The skill auto-schedules follow-up reminders based on these cadences. Buyer sees them in the .xlsx Follow-up Calendar (Sheet 4 in bulk mode) and the .docx Next Steps section in single mode.

## When to skip follow-ups entirely

- **Creator responded with "no thanks"**: don't follow up; respect the decline
- **Creator's recent content shifted away from brand category**: pitch a different angle later instead of bumping the original
- **Major news cycle, holiday, or platform outage**: pause follow-ups; resume after
- **Creator went on hiatus**: wait for their return
- **3rd outreach already sent with no reply**: stop; the answer is no

## Follow-up dos

- ✓ Reference the original message
- ✓ Keep follow-ups SHORTER than the original
- ✓ Offer alternative angles (Variant B)
- ✓ Give clear out (Variant C)
- ✓ Stay warm regardless of silence

## Follow-up don'ts

- ✗ Add new asks or pressure
- ✗ Repeat the entire original message (creator can scroll up)
- ✗ Send all 3 variants before each interval has passed
- ✗ Use guilt language ("I haven't heard back...")
- ✗ Threaten or invoke "we're moving on" with finality before Variant C
- ✗ Send follow-ups during obvious bad timing (creator's known hiatus, news cycle)

## The math of follow-up cadence

Industry-baseline conversion rates:

| Touchpoint | Conversion rate added |
|---|---|
| Initial outreach only | 2-10% (varies wildly by tier + quality) |
| + Variant A (soft nudge) | +1-4% |
| + Variant B (reframed) | +0.5-2% |
| + Variant C (final) | +0.2-1% |

A campaign that only sends the initial outreach captures roughly 60-70% of potential responses. A campaign that follows through with all 3 variants captures 90%+. The follow-ups are high-ROI relative to the time investment.

## Cadence example timeline

For a Micro creator outreached on May 1:

```
May 1   — Initial outreach sent
May 8   — Variant A (soft nudge) — buyer reminder set
May 22  — Variant B (reframed offer) — buyer reminder set
Jun 15  — Variant C (final ask) — buyer reminder set
Jun 30+ — Stop; no further contact for 90 days
```

The skill outputs these dates in the .docx and .xlsx.

## When the creator responds mid-cadence

If the creator responds at any point, the skill:
1. Pauses the remaining follow-ups
2. Updates `relationship_stage` to "responded" or "negotiating"
3. Generates a new reply draft based on what the creator said

The cadence resumes only if the conversation goes cold again — which is then re-counted from the latest response date.

## Special cadence for re-engagement

If a creator previously declined or went silent 6+ months ago and the buyer wants to re-engage:

- Skill flags the prior history
- Recommends a different angle (different product, different framework, different offer)
- Treats as a "warm cold" outreach — references prior interaction lightly without dwelling on it
- Slower cadence: 14 / 30 / 60 days

## Buyer override

The buyer can adjust cadence per-creator:

```json
"influencer_outreach": {
  "follow_up_cadence_overrides": {
    "@specific_creator": {"variant_a_days": 14, "variant_b_days": 30, "variant_c_days": 60}
  },
  "default_cadence_multiplier": 1.0
}
```

Useful when the buyer knows a specific creator's responsiveness pattern.

## Cadence audit in bulk mode

In bulk campaign mode, the skill outputs Sheet 4 (Follow-up Calendar) showing each creator's next-action date and which variant is due:

| Creator | Last Outreach | Next Variant Due | Variant | Status |
|---|---|---|---|---|
| @maya_brews | 2026-05-01 | 2026-05-08 | Variant A | Pending |
| @marcus_taste | 2026-05-01 | 2026-05-22 | Variant B | Pending |
| @sarah_kitchen | 2026-04-15 | 2026-05-10 | Variant C | Pending |
| ... | ... | ... | ... | ... |

The buyer scans by date to see what to send today/this week.
