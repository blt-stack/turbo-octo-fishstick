# Bundle Type: Frequently-Bought-Together (FBT)

Bundles where the data shows customers already purchase the items together. These are the lowest-risk bundles to launch — you're not asking customers to discover a new combination; you're packaging what they already do.

## Source layer

Apriori co-purchase mining. See `apriori-discovery.md` for the algorithm.

## Filter thresholds

A bundle qualifies as FBT when:
- **Support ≥ 0.01** (appears in 1%+ of orders) — ensures meaningful sample size
- **Confidence ≥ 0.25** (≥25% of A-buyers also buy B) — meaningful associative strength
- **Lift ≥ 2.0** (2× more likely than chance) — captures real correlation, not just popular items

Lower thresholds for smaller brands:
- < 200 orders/month: support ≥ 0.02, confidence ≥ 0.30, lift ≥ 1.7
- 200-1000 orders/month: standard thresholds
- 1000+ orders/month: support ≥ 0.005, confidence ≥ 0.20, lift ≥ 2.5

## Bundle structure

FBT bundles are typically:
- 2 SKUs (most common)
- 3 SKUs (still common; harder to discover at threshold)
- 4+ SKUs (rare; high lift would be exceptional)

The skill prefers 2-3 SKU bundles by default. 4+ SKU FBT bundles get flagged as "rare-find" in the discovery audit.

## Pricing strategy

FBT bundles typically use the **Standard tier (12-18% off)**. Rationale:
- Customers are already buying these together — they don't need a deep discount to convert
- A 5-10% nudge is often enough; 20%+ leaves margin on the table
- The discount signals "this bundle is curated" without screaming clearance

Exceptions:
- New FBT bundles in a fresh category: conservative tier to learn first
- High-margin SKU pairs: can go to aggressive without compromising margin
- Low-margin attractor + accessory: conservative; the bundle exists for cross-sell, not discount

## Positioning angle

FBT bundles position as **convenience**, not savings:
> "These three pieces work together — now in one click."
> "The set our customers reach for most often."

Avoid:
- "Save $X" leading the copy (cheapens the curation)
- "Limited time" language (FBT bundles should be permanent if they work)
- "Bundle and save" (generic; says nothing about the actual products)

## Why these bundles work

Customers self-organized the bundle through their own behavior. The brand's job is to:
1. Make the bundle visible (PDP cross-sell, dedicated landing page)
2. Reduce friction (single SKU, fewer clicks)
3. Apply a modest discount that's not the primary value prop

## Example FBT bundles

### Pour-Over + Filters
```
Anchor:   River Stone Pour-Over   $48.00
Add-on:   Filter Pack (100)       $12.00
Total individual:  $60.00
Bundle (15% off): $51.00
Savings: $9.00

Support: 8% of pour-over orders include filters
Confidence: 31% of pour-over buyers add filters
Lift: 2.6×
```

### Sneakers + Sock Pack
```
Anchor:   Everyday Sneaker        $95.00
Add-on:   Performance Sock 3-Pack $24.00
Total: $119.00
Bundle (12% off): $104.50
Savings: $14.50

Support: 14% of sneaker orders include socks
Confidence: 28%
Lift: 2.1×
```

### Candle + Trimmer + Snuffer
```
Anchor: Forest Candle    $38.00
Add-on: Wick Trimmer     $14.00
Add-on: Snuffer          $16.00
Total: $68.00
Bundle (18% off): $55.75
Savings: $12.25

Support: 4% of candle orders include both accessories
Confidence: 19% (lower because 3-SKU)
Lift: 4.2× (very high — these go together)
```

## FBT bundles vs. cross-sell suggestions

FBT bundles are different from on-PDP cross-sell ("Customers also bought..."):

| FBT Bundle | Cross-sell |
|---|---|
| Single SKU at checkout | Multiple separate SKUs |
| Discount applied | Full price each |
| Branded as a bundle | Positioned as related |
| Higher AOV per cart | Marginal AOV lift |

The skill suggests FBT bundles to convert frequent co-purchases into single-SKU experiences. Cross-sell still has its place; bundles compound the value.

## When FBT bundles fail

- **No discount applied**: customers see no reason to convert to the bundle SKU vs. buying separately
- **Too steep a discount**: signals desperation; customers wonder what's wrong
- **Hidden bundle (no merchandising)**: data shows the co-purchase exists but the bundle SKU doesn't get visibility
- **Wrong pairing surfaced**: low-confidence pairs (the data was coincidence, not real association)

The skill outputs bundle SKUs but the buyer has to merchandise them. The skill flags merchandising recommendations in the .docx.

## Re-discovery cadence

The skill recommends running the bundle suggestion engine:
- **Monthly** for active brands with growing co-purchase data
- **Quarterly** for stable brands
- **After a new product launch** — new SKUs may have surfaced new co-purchase patterns within 30-60 days

The bundle cache holds historical FBT bundles. The skill marks bundles that haven't been re-validated in 90+ days as "stale — re-validate."
