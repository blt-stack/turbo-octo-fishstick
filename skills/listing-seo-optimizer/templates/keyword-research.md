# Keyword Research Workflow

Three sources combined into one ranked list. The full pipeline runs in 2-4 minutes per product (faster if Claude in Chrome isn't available).

## Why three sources

LLM inference is fast, free, and product-aware — but it's also pattern-matching from training data, which lags real search behavior by months or years. Live autocomplete (Amazon, Google) reflects what people are typing today. Combining the two gives you fresh signal grounded in product reality.

## Source A: LLM inference (always run)

Generate 30-50 candidate keywords from the product info + brand context. Cover four categories:

**Head terms** (broad, high-volume, often single-word or two-word):
- Examples: "coffee dripper", "pour over", "ceramic mug"
- These are competitive but they validate that the product fits a recognized category.

**Long-tail** (3-5 words, lower volume, higher buying intent):
- Examples: "single cup ceramic pour over", "handmade reusable filter coffee dripper", "small batch stoneware pour over"
- These are where most small sellers actually win — less competition, more intent.

**Audience / occasion modifiers**:
- Examples: "coffee gift for him", "slow morning ritual", "minimalist coffee setup", "anniversary gift for coffee lover"
- These pull in shoppers searching by life moment rather than product category.

**Use-case framings**:
- Examples: "paperless coffee brewing", "dishwasher safe pour over", "single serve coffee maker no electricity"
- These reframe the product around the problem it solves, which can surface entirely different search demand.

Output a flat candidate list with each keyword tagged by category. Don't rank yet — ranking happens after all three sources are merged.

## Source B: Amazon autocomplete (when Claude in Chrome is available)

Amazon's search-bar autocomplete is one of the cleanest signals for "what Amazon shoppers actually type." Use it for any product the buyer sells on Amazon (or wants to).

**Workflow:**

1. Use `mcp__Claude_in_Chrome__navigate` to go to `https://www.amazon.com`. Load schemas via ToolSearch if Chrome tools aren't loaded yet.
2. Use `mcp__Claude_in_Chrome__find` to locate the search input (selector typically `#twotabsearchtextbox`).
3. For each of the top 3-5 head terms from Source A:
   - Use `mcp__Claude_in_Chrome__form_input` to type the head term into the search box. Don't press Enter — just type.
   - Wait ~500ms for the autocomplete dropdown to populate.
   - Use `mcp__Claude_in_Chrome__get_page_text` or `mcp__Claude_in_Chrome__read_page` to capture the autocomplete suggestions.
   - Clear the search box and repeat.
4. Deduplicate suggestions across all head terms. Output is typically 30-80 unique suggestions.

**Pitfalls:**

- Amazon localizes autocomplete by region. If the buyer sells globally, run the workflow once per major market (.com, .co.uk, .de, .ca).
- Sponsored suggestions occasionally appear at the top of the dropdown — exclude these. They reflect what advertisers paid for, not what shoppers searched.
- If the page is logged into a specific account, autocomplete may be personalized. Prefer a fresh / incognito Chrome window where possible.

**When Chrome isn't available:** skip this source. Note in the output that Amazon-native keyword signal is missing. Don't try to substitute Google suggest for Amazon autocomplete — they reflect different intent.

## Source C: Google suggest (always run — no key needed)

Google's autocomplete endpoint is free and unauthenticated. Use `scripts/google_suggest_scraper.py`.

**Workflow:**

1. For each head term, call the scraper with the head term.
2. The scraper hits `https://suggestqueries.google.com/complete/search?client=chrome&q={query}` and parses the JSON response. Returns 8-10 suggestions per query.
3. Repeat for each head term (3-5 typically). Deduplicate.

Google suggest reflects what people search outside marketplaces — useful for Shopify SEO (which lives or dies by Google SERP) and for surfacing audience/occasion modifiers that Amazon autocomplete misses.

**Pitfalls:**

- Google personalizes by region (geo-detected from IP). Output reflects whichever region the script runs from. Fine for most cases.
- Suggestions include sponsored/trending terms occasionally. Filter out anything that looks like a brand name unrelated to the product.

## Cluster and rank

Once all three sources are merged into a flat list of 60-150 candidates, cluster and rank:

### Step 1: Cluster by intent

Bucket each keyword into one of:
- **Transactional** (buying intent): "buy ceramic pour over", "best pour over coffee dripper", "[brand] ceramic pour over"
- **Comparison** (researching options): "pour over vs french press", "ceramic vs glass pour over"
- **Informational** (learning): "how to use a pour over", "pour over brewing guide"
- **Audience/occasion**: "coffee gift for him", "minimalist kitchen", "anniversary gift coffee"

Transactional and audience/occasion are highest-priority for product listings. Comparison is mid-priority (good for landing pages and bullet content). Informational is generally low-priority for product listings (better suited to blog content).

### Step 2: Rank within each cluster

Rank by:
1. **Source convergence**: a keyword appearing in *both* Amazon autocomplete AND Google suggest is a stronger signal than one appearing in only one source.
2. **Relevance to the specific product**: LLM judgment, based on product info + brand voice.
3. **Specificity**: long-tail beats head term for small sellers. A keyword like "handmade ceramic pour over single cup" is more winnable than "coffee dripper."

### Step 3: Produce the final ranked list (15-25 keywords)

For each keyword in the final list, include:

```yaml
- keyword: "ceramic pour over"
  intent: transactional
  sources: [amazon_autocomplete, google_suggest, llm]
  relevance_score: 9.2  # LLM judgment 0-10
  recommended_placement:
    - amazon_title
    - shopify_title
    - shopify_meta_title
    - etsy_title
  rank: 1
  notes: "Primary head term. Should appear in the first 5 words of every title."
```

The `recommended_placement` field is what makes the keyword list actionable downstream. Be specific — don't say "use it in the title" without naming which platform's title.

## Output format

A YAML-ish ranked list as shown above, ready for the rewriter step (Step 6 in the main workflow). The same list is also serialized into `keywords.json` for the Product Description Writer to pick up.

## How long this takes

- LLM inference: <30 seconds
- Amazon autocomplete (5 head terms): 60-120 seconds (Chrome interactions are slow)
- Google suggest (5 head terms): 5-15 seconds
- Clustering + ranking: 30-60 seconds

Full run: 2-4 minutes per product. Bulk mode should parallelize where possible — Google suggest and LLM inference can run in parallel; Amazon autocomplete is serialized because Chrome is a single shared resource.
