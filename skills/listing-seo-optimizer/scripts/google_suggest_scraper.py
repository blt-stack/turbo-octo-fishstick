"""
Scrape Google's free autocomplete endpoint to surface keyword suggestions.

Hits https://suggestqueries.google.com/complete/search — no API key, no auth,
unlimited requests within reasonable rate limits.

Usage from another script:
    from google_suggest_scraper import suggest, suggest_many

    suggestions = suggest("ceramic pour over")
    # ['ceramic pour over coffee maker', 'ceramic pour over dripper', ...]

    bulk = suggest_many(["ceramic pour over", "pour over coffee", "drip coffee maker"])
    # dict mapping query -> list of suggestions

CLI:
    python google_suggest_scraper.py "ceramic pour over"
    python google_suggest_scraper.py --multi "ceramic pour over" "drip coffee"
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from typing import Iterable


SUGGEST_URL = "https://suggestqueries.google.com/complete/search"
USER_AGENT = "Mozilla/5.0 (compatible; EcommerceSellerSkill/0.2)"
RATE_LIMIT_DELAY_SEC = 0.25  # be a polite citizen


def _build_url(query: str, client: str = "chrome", hl: str = "en") -> str:
    params = urllib.parse.urlencode({"client": client, "q": query, "hl": hl})
    return f"{SUGGEST_URL}?{params}"


def suggest(query: str, client: str = "chrome", hl: str = "en", timeout: int = 5) -> list[str]:
    """
    Return Google autocomplete suggestions for a query.

    The 'chrome' client returns a simple JSON array. Other clients ('firefox',
    'youtube') return slightly different shapes; chrome is the cleanest.
    """
    url = _build_url(query, client=client, hl=hl)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as exc:
        print(f"[google_suggest_scraper] Failed for '{query}': {exc}", file=sys.stderr)
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # 'chrome' client may return JSONP-ish — try to strip wrapper
        if raw.startswith("window.google.ac.h(") and raw.endswith(")"):
            raw = raw[len("window.google.ac.h(") : -1]
            data = json.loads(raw)
        else:
            print(f"[google_suggest_scraper] Couldn't parse response for '{query}'", file=sys.stderr)
            return []

    # Chrome-client response: [query, [suggestions], [descriptions], [...], metadata]
    if isinstance(data, list) and len(data) >= 2 and isinstance(data[1], list):
        return [s for s in data[1] if isinstance(s, str)]
    return []


def suggest_many(queries: Iterable[str], delay_sec: float = RATE_LIMIT_DELAY_SEC, **kwargs) -> dict[str, list[str]]:
    """Run suggest() for many queries with a small delay between requests."""
    results: dict[str, list[str]] = {}
    for i, q in enumerate(queries):
        if i > 0:
            time.sleep(delay_sec)
        results[q] = suggest(q, **kwargs)
    return results


def deduplicate(all_suggestions: dict[str, list[str]]) -> list[str]:
    """Merge per-query suggestions into a single deduplicated list, preserving order."""
    seen: set[str] = set()
    out: list[str] = []
    for query, suggestions in all_suggestions.items():
        for s in suggestions:
            key = s.lower().strip()
            if key and key not in seen:
                seen.add(key)
                out.append(s)
    return out


def _cli():
    parser = argparse.ArgumentParser(description="Scrape Google autocomplete suggestions.")
    parser.add_argument("queries", nargs="+", help="One or more seed queries")
    parser.add_argument("--multi", action="store_true", help="Run multiple queries and return a merged deduped list")
    parser.add_argument("--hl", default="en", help="Language code (default: en)")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    if args.multi or len(args.queries) > 1:
        all_results = suggest_many(args.queries, hl=args.hl)
        merged = deduplicate(all_results)
        if args.json:
            print(json.dumps({"queries": args.queries, "by_query": all_results, "merged": merged}, indent=2))
        else:
            print(f"=== {len(merged)} unique suggestions across {len(args.queries)} queries ===")
            for s in merged:
                print(s)
    else:
        results = suggest(args.queries[0], hl=args.hl)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for s in results:
                print(s)


if __name__ == "__main__":
    _cli()
