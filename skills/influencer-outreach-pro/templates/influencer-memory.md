# Influencer Memory — Per-Influencer Relationship State

Every outreach the skill drafts pulls from + writes to a per-influencer JSON file at:

```
~/.the-ecommerce-seller/cache/influencers/{handle-slug}.json
```

Where `{handle-slug}` is a filesystem-safe slug from the creator's handle (e.g., `@maya_brews` → `maya-brews`).

This makes each new outreach pick up where the last one left off — second and third outreach to the same creator read like continuing relationships, not cold contact.

## Schema

```json
{
  "influencer_id": "maya-brews",
  "handle": "@maya_brews",
  "display_name": "Maya Lin",
  "real_name": "",
  "platforms": {
    "instagram": {
      "handle": "@maya_brews",
      "follower_count": 24000,
      "engagement_rate": 0.062,
      "tier": "micro",
      "primary": true
    },
    "tiktok": {
      "handle": "@mayabrews",
      "follower_count": 9000,
      "engagement_rate": 0.085,
      "tier": "nano",
      "primary": false
    }
  },
  "content_themes": ["coffee_brewing", "slow_mornings", "home_interiors"],
  "voice_register": "warm_ironic_conversational",
  "niche": "coffee + slow living",
  "audience_demographic_guess": "US/UK 25-40, design-aware",
  "language_preference": "english",
  "geography": "Brooklyn, NY",
  "time_zone": "America/New_York",
  "best_contact_method": "instagram_dm",
  "email_known": "",
  "manager_email_known": "",
  "first_contact_date": "2026-05-01",
  "last_contact_at": "2026-05-22",
  "relationship_stage": "responded",
  "relationship_stage_history": [
    {"stage": "new", "since": "2026-05-01", "until": "2026-05-01"},
    {"stage": "outreached", "since": "2026-05-01", "until": "2026-05-08"},
    {"stage": "follow_up_sent_a", "since": "2026-05-08", "until": "2026-05-15"},
    {"stage": "responded", "since": "2026-05-15", "until": null, "reason": "Maya replied with interest"}
  ],
  "outreach_history": [
    {
      "date": "2026-05-01",
      "channel": "instagram_dm",
      "outreach_type": "initial",
      "platform": "instagram",
      "tier_at_time": "micro",
      "framework_offered": "hybrid",
      "rate_offered_usd": 400,
      "product_offered": "river-stone-pour-over-bundle",
      "summary": "Initial outreach pitching brewing bundle + $400 for Reel + 2 Stories",
      "response_status": "no_reply_initial",
      "skill_run_id": "20260501-1030"
    },
    {
      "date": "2026-05-08",
      "channel": "instagram_dm",
      "outreach_type": "follow_up_variant_a",
      "summary": "Soft nudge",
      "response_status": "no_reply",
      "skill_run_id": "20260508-1100"
    },
    {
      "date": "2026-05-15",
      "channel": "instagram_dm",
      "outreach_type": "follow_up_variant_b",
      "summary": "Reframed offer — flexible deliverables format",
      "response_status": "responded_positive",
      "response_summary": "Maya is interested; asked about timing flexibility",
      "skill_run_id": "20260515-1400"
    }
  ],
  "pending_responses": [],
  "post_context_history": [
    {
      "captured_at": "2026-05-01",
      "captions_pasted": [
        "Post about pour-over coffee on camping trip ...",
        "Post about morning routine in winter ...",
        "Post about studio mug collection ..."
      ],
      "extracted_themes": ["coffee_brewing", "slow_mornings", "home_interiors"],
      "specific_references_extracted": [
        {"reference": "camping pour-over post", "from_caption_index": 0},
        {"reference": "winter morning routine", "from_caption_index": 1}
      ]
    }
  ],
  "deliverables_history": [],
  "payment_history": {
    "total_gifted_value_usd": 78,
    "total_cash_paid_usd": 0,
    "total_affiliate_paid_usd": 0
  },
  "exclusivity_windows": [],
  "blacklisted": false,
  "notes": [
    {"date": "2026-05-15", "note": "Maya is interested but mentioned upcoming travel — flexible timing wins"}
  ],
  "alignment_score": 8.5,
  "alignment_notes": "Strong brand fit; potential competitor overlap window 3 weeks ago",
  "last_updated": "2026-05-22T14:30:00Z"
}
```

## Field semantics

### `relationship_stage`

Possible values:
- `new` — never contacted before
- `outreached` — initial outreach sent, awaiting reply
- `follow_up_sent_a` — soft nudge sent
- `follow_up_sent_b` — reframed offer sent
- `follow_up_sent_c` — final ask sent
- `no_reply_terminal` — gone silent through all follow-ups
- `responded` — creator engaged in conversation
- `negotiating` — terms being worked out
- `agreed` — partnership terms agreed; awaiting deliverables
- `completed` — deliverables delivered; campaign closed
- `declined` — creator said no
- `strained` — past dispute / unmet deliverables / late deliverables
- `blacklisted` — buyer marked as do-not-contact

### `content_themes`

Auto-extracted from pasted post context. Persists across outreach attempts.

### `voice_register`

Captured from post context analysis. Helps the skill match tone in subsequent outreach.

### `outreach_history`

Append-only log. Every outreach attempt logged. Useful for:
- Avoiding duplicate outreach
- Calibrating follow-up cadence
- Reviewing past asks (so the next ask doesn't repeat or contradict)

### `post_context_history`

Logs every time the buyer pastes recent post context. Helps detect when creator content has shifted (themes diverge between captures → re-evaluate alignment).

### `pending_responses`

Active outreach attempts awaiting response. Drives follow-up reminders.

## Read flow

When drafting a new outreach to a creator, the skill:

1. Look up `~/.the-ecommerce-seller/cache/influencers/{handle-slug}.json`
2. If exists:
   - Pull relationship_stage, history, themes, voice
   - Adjust the outreach (continuing relationship vs. cold)
   - Reference prior interaction context appropriately
3. If doesn't exist:
   - Create new file with whatever the buyer provides
   - First outreach is cold-contact (no past references)

## Write flow

After each outreach is drafted, the skill writes:

1. Adds to `outreach_history`
2. Updates `relationship_stage` per the new state
3. Updates `last_contact_at`
4. Adds to `pending_responses`
5. Logs post context (if buyer pasted new posts)

## Stage transitions

| Trigger | Transition |
|---|---|
| First outreach sent | `new` → `outreached` |
| Follow-up A sent | `outreached` → `follow_up_sent_a` |
| Follow-up B sent | `follow_up_sent_a` → `follow_up_sent_b` |
| Follow-up C sent | `follow_up_sent_b` → `follow_up_sent_c` |
| No reply after C + 30 days | `follow_up_sent_c` → `no_reply_terminal` |
| Creator responds | Any stage → `responded` |
| Negotiating | `responded` → `negotiating` |
| Terms agreed | `negotiating` → `agreed` |
| Deliverables completed | `agreed` → `completed` |
| Creator declines | Any → `declined` |
| Quality / payment issue | `agreed` → `strained` |
| Buyer marks do-not-contact | Any → `blacklisted` |

Buyer can manually override any transition.

## Re-outreach cooling periods

If a creator declined or went silent, the skill enforces cooling periods before allowing fresh outreach:

| Prior stage | Cooling period before re-outreach |
|---|---|
| `declined` (polite) | 6 months |
| `declined` (hostile) | 18 months or never |
| `no_reply_terminal` | 3 months |
| `strained` | 12 months + buyer override |
| `blacklisted` | Skill refuses to draft |

The skill warns the buyer when attempting to re-outreach inside a cooling period and asks for confirmation.

## Cross-platform creator

A creator who's active on multiple platforms gets one influencer memory file with platform sub-entries:

```json
"platforms": {
  "instagram": {...},
  "tiktok": {...},
  "youtube": {...}
}
```

The skill chooses the primary outreach platform based on:
1. Creator's most-active platform (highest follower count / engagement)
2. Brand's content-fit preference
3. Where the buyer says they want to engage

## Multi-influencer family (e.g., couple-run accounts)

For accounts run by multiple people:

```json
"display_name": "Maya & Marcus Lin",
"real_names": ["Maya Lin", "Marcus Lin"],
"voice_register": "co-hosted_warm_humorous"
```

The skill addresses both names in the opener when applicable.

## Privacy + portability

The influencer memory is local-only. The buyer can:
- Edit notes manually
- Delete a file to forget a creator
- Export the `~/.the-ecommerce-seller/cache/influencers/` folder for backup
- Mark `blacklisted: true` to prevent future outreach

The skill never writes to the file any data not directly provided by the buyer (no API scraping behind the scenes).

## CLI

```bash
python influencer_memory.py list                  # list all cached influencers
python influencer_memory.py show <handle>         # show full file
python influencer_memory.py pending               # list creators awaiting reply
python influencer_memory.py blacklist <handle>    # mark do-not-contact
python influencer_memory.py transition <handle> <new_stage>
```

Helps the buyer manage the influencer network as it grows.
