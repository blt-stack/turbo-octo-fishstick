# Send Cadence Patterns

How sends within a single campaign are spaced over time. Different campaign types use different cadence shapes. This file defines the standard patterns; per-playbook overrides are in `campaign-playbooks.md`.

---

## Pattern 1: Standard 7-day campaign

For most non-tentpole campaigns (Mother's Day, Father's Day, mid-size product launches, Memorial Day, etc.).

| Day relative to launch | Channel | Send type |
|---|---|---|
| -3 | Email | Pre-launch tease ("coming Tuesday") |
| -1 | Email + organic | Day-before reminder |
| 0 (launch day) | Email + SMS + paid ads + organic + site banner | Launch push |
| +2 | Email + organic | Mid-campaign + featured content |
| +4 | Email + paid ads | Reminder + scarcity if relevant |
| +6 | Email + SMS + paid ads + site popup | Last-day urgency |
| +7 | Email | Wrap-up / thank-you |

Total: 6 emails + 2 SMS + 3-4 paid ad concepts + 4-5 organic posts + 2 site updates.

---

## Pattern 2: Compressed 3-day campaign (flash sale, restock)

For high-urgency short campaigns.

| Day | Channel | Send type |
|---|---|---|
| 0 | Email + SMS + paid ads + site popup | Surprise launch |
| +1 | Email + organic | Mid-sale reminder |
| +2 (final day, AM) | Email | Morning reminder |
| +2 (final day, evening) | Email + SMS | Last few hours |
| +3 | Email | Wrap-up |

Total: 4 emails + 2 SMS + 2 paid ads + site popup live during.

---

## Pattern 3: Extended 14-day campaign (BFCM, big holiday window)

For tentpole campaigns with multiple peak days.

| Day | Channel | Send type |
|---|---|---|
| -7 to -3 | Email + organic | Pre-event content (3 sends) |
| -1 | Email + organic | Eve-of-event reminder |
| 0 (BF day) | Email + SMS + paid ads (peak budget) + site updates | Peak day push |
| +1 (Saturday) | Email + paid ads | Continuation |
| +2 (Sunday) | Email | Mid-event lull email |
| +3 (Cyber Monday) | Email + SMS + paid ads (peak budget) + site | Peak day push |
| +4 to +6 | Email (3 sends) + paid ads | Cyber Week sustain |
| +7 (wrap-up) | Email | Thank-you |

Total: 10-12 emails + 4-5 SMS + 5-7 paid ad concepts + 12-18 organic posts + 5-6 site updates.

For BFCM specifically, see Playbook 1 in `campaign-playbooks.md` for the full BFCM-tuned cadence.

---

## Pattern 4: Single-day campaign (Birthday, anniversary day, Black Friday day)

A campaign that's really just one day of activity.

| Day | Channel | Send type |
|---|---|---|
| -3 | Email | Pre-event tease |
| -1 | Email | Day-before reminder |
| 0 (the day) | Email + SMS + paid ads + organic + site updates | Full day push |
| +1 | Email | Wrap-up / thank-you |

Total: 4 emails + 1 SMS + 1-2 paid ads + 2-3 organic + site updates.

---

## Pattern 5: Sustained-content campaign (seasonal tentpole, brand anniversary)

A multi-week brand campaign without a single peak day.

| Week | Channel | Send type |
|---|---|---|
| Week 1 launch | Email + paid ads + organic + site update | Concept reveal |
| Week 1 sustain | Email + organic (3-5 posts) | Story development |
| Week 2 | Email + organic (3-5 posts) | Mid-arc content |
| Week 3 | Email + organic (3-5 posts) | Customer features |
| Week 4 wrap | Email + organic | Closing chapter |

Total: 4-6 emails + 12-20 organic posts + ongoing paid ads + 1-2 site updates.

These campaigns work for brand-content moments more than promotional ones.

---

## Cadence by campaign type (quick reference)

| Campaign type | Cadence pattern |
|---|---|
| Mother's Day, Father's Day | Pattern 1 (7-day) extended to 14 days |
| Valentine's Day | Pattern 1 (7-day) extended to 10 days |
| Memorial Day, Labor Day, July 4th | Pattern 1 (long-weekend variant) |
| BFCM + Cyber Week | Pattern 3 (14-day extended) |
| Easter | Pattern 1 (7-day) |
| Halloween | Pattern 1 (7-day) |
| Christmas + Boxing Day | Pattern 3 (14-day extended through Dec 31) |
| Product launch (small) | Pattern 1 (7-day) |
| Product launch (major) | Pattern 5 (sustained, 21-30 days) |
| Restock push | Pattern 2 (compressed 3-day) |
| Flash sale | Pattern 2 (compressed 3-day) |
| Brand anniversary | Pattern 5 (sustained 7-14 days) |
| Subscriber-growth campaign | Pattern 5 (sustained 14 days) |
| Seasonal tentpole (Slow Mornings of Summer, etc.) | Pattern 5 (sustained 30-45 days) |

---

## Cross-campaign cadence rules

Beyond the per-campaign cadence, the calendar enforces program-level rules:

### Send frequency limits per audience per week

| Audience tier | Max emails per week | Max SMS per week |
|---|---|---|
| Highly engaged (opened/clicked in past 30 days) | 4-5 | 2-3 |
| Standard engaged (active in past 90 days) | 2-3 | 1 |
| Light engagement (active in past 180 days) | 1-2 | 0-1 |
| Dormant (no activity in 180+ days) | 0 (exclude from broadcasts) | 0 |

When two campaigns overlap, the calendar checks per-audience send counts and either staggers or merges sends to stay within these limits.

### Conflict avoidance

The calendar's conflict check flags:

- Two campaigns sending on the same day to the same audience tier (over-send risk)
- A flash sale scheduled during a major holiday week (the audience is already in promo mode)
- A product launch scheduled during BFCM (the launch gets buried)
- A subscriber-growth campaign scheduled when the welcome flow is already at peak volume

When conflicts are detected, the calendar either re-times one campaign or merges them (e.g., a flash sale during Mother's Day week becomes "Mother's Day flash sale" — one campaign instead of two).

### Sub-segment opportunities

For larger lists (>10,000 subscribers), the calendar can recommend per-segment send variation:

- Highly engaged subscribers get ALL sends in a campaign
- Standard engaged get a subset (the most-converting 2-3 emails)
- Light engagement get only the launch + final-day reminder

This protects the dormant-tail of the list while maximizing engagement on the active tail.

---

## Time-of-day defaults

For sends within a campaign, the calendar defaults to these send times (recipient local time, when Klaviyo's smart-send is enabled):

| Send type | Default time |
|---|---|
| Email pre-launch tease | 10am |
| Email launch day | 9am |
| Email mid-campaign | 11am |
| Email last-day | 2pm (morning of the day; the 8pm/10pm send is for the SMS) |
| Email wrap-up | 9am day after |
| SMS launch | 11am |
| SMS last-day | 6pm |
| Paid ads | Continuous (set in the ad campaign settings) |
| Organic posts | Per platform optimal — typically 12pm and 6pm for Instagram; 7am and 7pm for TikTok |
| Site updates | Live by 8am day of the campaign |

Buyer can override per-campaign in the brief. The calendar uses these as starting points.
