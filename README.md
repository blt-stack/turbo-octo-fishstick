# The E-Commerce Seller

A persona plugin for solo operators running Shopify, Amazon, Etsy, eBay, Walmart, or TikTok Shop stores. Activate it and Claude becomes your in-house copywriter, ad buyer, email strategist, supplier negotiator, and ops analyst.

## What this plugin does

You run the store. The plugin runs everything else.

This is built for the operator who's wearing every hat — listings, ads, emails, customer service, supplier emails, inventory math, bundle ideas, influencer DMs, the morning numbers check. Fifteen skills cover the work an outsourced agency would charge you four figures a month for, and they all work together using the same brand voice and store data.

## Install

In Claude Code (2.1.275 or later):

```
/plugin install the-ecommerce-seller --marketplace blt-stack/turbo-octo-fishstick
```

On older versions, add the marketplace first, then install:

```
/plugin marketplace add blt-stack/turbo-octo-fishstick
/plugin install the-ecommerce-seller@blt-stack-plugins
```

To try it from a local copy without installing: `claude --plugin-dir /path/to/turbo-octo-fishstick`.

## Who it's for

You sell physical products online. You might be:

- A DTC private-label brand owner running Shopify + Meta Ads
- A dropshipper iterating fast on creative and listings
- A handmade maker scaling beyond Etsy
- An Amazon FBA seller managing listings and PPC
- A multi-channel seller juggling several marketplaces

The plugin doesn't assume your niche, your revenue band, or your brand voice. It learns those things the first time you run a skill and saves them so you never have to re-explain.

## The skills (v1 lineup)

**Listings & product pages**
1. Product Description Writer — descriptions across Shopify, Amazon, Etsy, eBay, Walmart, TikTok Shop
2. Listing SEO Optimizer — keyword research, title/bullet/backend tags, meta tags
3. Landing Page Copywriter — full PDP and collection page copy
4. A+ Content Creator — Amazon A+ modules with copy and image briefs

**Paid acquisition**
5. Ad Creative Generator — Meta + TikTok primary text, headlines, hooks
6. UGC Creator Brief Writer — briefs for creators making Reels/TikTok ads

**Email & retention**
7. Email Flow Architect — Welcome, Abandoned Cart, Post-Purchase flows
8. Campaign Calendar Planner — 90-day campaign calendar

**Customer operations**
9. Customer Service Reply Bot — support ticket replies
10. Review Response Writer — review responses by star rating

**Supply & inventory**
11. Supplier Negotiation Assistant — supplier emails and negotiation scripts
12. Inventory Forecaster — reorder points, safety stock, stockout alerts

**Growth & strategy**
13. Bundle Builder — bundle suggestions with pricing and copy
14. Influencer Outreach Pro — outreach DMs and partnership terms
15. Daily Store Digest — morning briefing on revenue, ads, email, inventory

## Connectors

The plugin works with any combination of these connectors. Skills check what's connected and fall back to manual input when something isn't available — you always get a result.

Bundled in `.mcp.json` (connect whichever you use):

- **Shopify** (core spine — used by most skills)
- **Klaviyo** (email + SMS)
- **Gmail** (outreach + customer replies)
- **Canva** (visual templates)
- **Supermetrics Marketing Analytics** (marketing data such as Meta Ads and GA4, used by the Daily Store Digest)

Also used when available:

- **Meta Ads** (Facebook + Instagram ads)
- **Amazon** (where MCP support is available)

The Ad Creative Generator and A+ Content Creator can optionally use a Fal AI API key to generate ad images directly. Add it to the config under `api_keys.fal_ai`, or set the `FAL_KEY` environment variable. Without a key they output Canva-ready specs.

## First-run setup

The first time you trigger any skill, it walks you through a brief onboarding that captures your store info, primary platforms, brand voice, target audience, and a vocabulary blocklist. This setup is shared across skills — answer once, every skill benefits.

Your answers are saved to `.config/the-ecommerce-seller.config.json` in the plugin directory. Skills keep their shared caches (keywords, supplier and influencer memory, reorder triggers and so on) under `.cache/`. Both folders hold your store data, so they are excluded from git.

You can re-run setup any time by saying "redo onboarding", "rerun setup" or "update my brand voice", or by editing the config file directly.

## Plugin status

This is v0.15.0. All 15 skills above are included.
