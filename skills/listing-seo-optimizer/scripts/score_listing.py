"""
Apply the listing audit rubric programmatically.

The rubric lives in `templates/audit-rubric.md`. This script implements the
mechanical sub-score calculations so they're consistent across runs. The LLM
driving the skill still does the qualitative checks (benefit-led bullet
detection, brand-voice alignment), but the deterministic checks (character
length utilization, keyword counting, bullet count) belong in code.

Usage from another script:
    from score_listing import score_amazon, score_etsy, score_shopify, ...

    score = score_amazon(
        listing={"title": "...", "bullets": [...], "description": "...",
                 "backend_search_terms": "...", "images_count": 7,
                 "attributes_filled": 12, "attributes_total": 15},
        keywords=ranked_keyword_list,
    )
    # {"total": 76, "subscores": {...}, "issues": [...]}

CLI:
    python score_listing.py <listing_json> <keywords_json> <platform>
"""

import argparse
import json
import sys
from pathlib import Path


# Sweet-spot character ranges per platform. (target_min, target_max, hard_cap)
TITLE_RANGES = {
    "amazon": (150, 180, 200),
    "shopify": (50, 60, 60),
    "etsy": (110, 140, 140),
    "ebay": (75, 80, 80),
    "walmart": (50, 75, 200),
    "tiktok_shop": (28, 34, 34),
}


def _length_utilization_score(length: int, target_min: int, target_max: int, hard_cap: int, max_points: int = 6) -> tuple[float, str]:
    """Generic length utilization scorer. Returns (score, note)."""
    if length > hard_cap:
        return 0.0, f"OVER HARD CAP: {length}/{hard_cap}"
    if length >= target_min:
        if length <= target_max:
            return float(max_points), f"In sweet spot ({length}/{hard_cap})"
        # Over target but under cap — still good
        return float(max_points) * 0.9, f"Above target, under cap ({length}/{hard_cap})"
    # Under target
    ratio = length / target_min if target_min else 0
    if ratio >= 0.8:
        return max_points * 0.67, f"Slightly short ({length}/{target_min} target min)"
    if ratio >= 0.6:
        return max_points * 0.33, f"Short ({length}/{target_min} target min)"
    return 0.0, f"Way under target ({length}/{target_min} target min)"


def _count_keyword_matches(text: str, keywords: list[str]) -> int:
    """Count how many of the keywords appear in text (case-insensitive, whole-phrase match)."""
    text_lower = text.lower()
    count = 0
    for kw in keywords:
        if kw.lower() in text_lower:
            count += 1
    return count


def _normalize_keywords(keywords_ranked: list) -> list[str]:
    """Accept either a list of strings or a list of dicts with 'keyword' field."""
    if not keywords_ranked:
        return []
    if isinstance(keywords_ranked[0], dict):
        return [kw.get("keyword", "") for kw in keywords_ranked if kw.get("keyword")]
    return [str(kw) for kw in keywords_ranked]


def _score_keyword_coverage(listing_text: str, keywords: list[str]) -> tuple[float, list[str]]:
    """Dimension 1: Keyword coverage. Returns (score_out_of_30, notes)."""
    issues: list[str] = []
    if not keywords:
        return 15.0, ["No keyword list provided — coverage score is a default 15/30"]

    top_5 = keywords[:5]
    top_6_to_15 = keywords[5:15]

    top_5_hits = _count_keyword_matches(listing_text, top_5)
    top_15_hits = _count_keyword_matches(listing_text, top_6_to_15)

    # Each top-5 keyword = 3 points (max 15)
    top_5_score = min(15, top_5_hits * 3)
    # Each top 6-15 keyword = 1 point (max 10)
    top_15_score = min(10, top_15_hits)

    # Stuffing penalty: subtract 1 pt per keyword repeated >3 times, cap at -5
    stuffing = 0
    listing_lower = listing_text.lower()
    for kw in keywords[:15]:
        occurrences = listing_lower.count(kw.lower())
        if occurrences > 3:
            stuffing += 1
    no_stuff_score = max(0, 5 - stuffing)

    if top_5_hits < len(top_5):
        missing = [kw for kw in top_5 if kw.lower() not in listing_lower]
        issues.append(f"Top-5 keywords missing from listing: {missing}")
    if stuffing > 0:
        issues.append(f"{stuffing} keyword(s) appear more than 3 times in body — softens A10/A9 ranking")

    return top_5_score + top_15_score + no_stuff_score, issues


def _score_title_strength(title: str, platform: str, top_keyword: str | None) -> tuple[float, list[str]]:
    """Dimension 2: Title strength. Returns (score_out_of_20, notes)."""
    if platform not in TITLE_RANGES:
        return 14.0, [f"No title range defined for {platform} — default 14/20"]
    issues: list[str] = []
    target_min, target_max, hard_cap = TITLE_RANGES[platform]

    # 6 pts: length utilization
    length_score, length_note = _length_utilization_score(len(title), target_min, target_max, hard_cap, max_points=6)
    if "OVER" in length_note or "Way under" in length_note or "Short" in length_note:
        issues.append(f"Title length: {length_note}")

    # 6 pts: front-loading
    front_load_score = 0.0
    if top_keyword:
        title_lower = title.lower()
        kw_lower = top_keyword.lower()
        pos = title_lower.find(kw_lower)
        if pos == -1:
            issues.append(f"Primary keyword '{top_keyword}' missing from title")
        else:
            # Where in the title (by word count)?
            words_before = len(title[:pos].split())
            if words_before <= 4:
                front_load_score = 6.0
            elif words_before <= 9:
                front_load_score = 4.0
            else:
                front_load_score = 2.0
                issues.append(f"Primary keyword is deep in the title (word {words_before + 1}); move it forward")
    else:
        front_load_score = 4.0  # neutral default

    # 4 pts: brand placement (deferred — platform-specific, LLM checks qualitatively)
    brand_score = 4.0

    # 4 pts: no spammy patterns
    spam_score = 4.0
    spammy_markers = ["L@@K", "WOW", "BEST", "AMAZING", "###", "!!!"]
    spam_hits = sum(1 for m in spammy_markers if m in title.upper())
    if spam_hits:
        spam_score = max(0.0, 4.0 - spam_hits)
        issues.append(f"Title has spammy patterns (-{spam_hits} pt): {spam_hits} flagged marker(s)")
    if title.isupper() and len(title) > 5:
        spam_score = max(0.0, spam_score - 1)
        issues.append("Title is ALL CAPS — most platforms downrank this")

    return length_score + front_load_score + brand_score + spam_score, issues


def _score_bullets(bullets: list[str], platform: str, keywords: list[str]) -> tuple[float, list[str]]:
    """Dimension 3: Bullet quality. Returns (score_out_of_20, notes)."""
    issues: list[str] = []
    if not bullets:
        if platform in ("amazon", "walmart"):
            issues.append("No bullets used — Amazon/Walmart expect them")
            return 0.0, issues
        # Other platforms don't require bullets; give neutral score
        return 14.0, ["Platform doesn't require bullets — neutral score"]

    bullet_limit = {"amazon": 250, "walmart": 80}.get(platform, 250)
    max_bullets = {"amazon": 5, "walmart": 10}.get(platform, 5)

    # 6 pts: count utilization
    count_score = min(6.0, (len(bullets) / max_bullets) * 6)
    if len(bullets) < max_bullets:
        issues.append(f"Only {len(bullets)} of {max_bullets} bullet slots used")

    # 6 pts: benefit-led (heuristic — opens with caps phrase or "BENEFIT —")
    benefit_count = 0
    for b in bullets:
        opener = b.split(" ", 5)[0]
        if opener.isupper() and len(opener) > 2:
            benefit_count += 1
        elif "—" in b[:50] or " - " in b[:50]:
            benefit_count += 1
    benefit_score = (benefit_count / len(bullets)) * 6
    if benefit_count < len(bullets):
        issues.append(f"{len(bullets) - benefit_count} bullet(s) don't open with a clear benefit headline")

    # 4 pts: character utilization (≥70% of limit)
    util_count = sum(1 for b in bullets if len(b) >= bullet_limit * 0.7)
    util_score = (util_count / len(bullets)) * 4
    if util_count < len(bullets):
        issues.append(f"{len(bullets) - util_count} bullet(s) are under 70% of character limit — wasted space")

    # 4 pts: differentiation (heuristic — first 5 words of each should be unique across bullets)
    openers = [" ".join(b.split()[:5]).lower() for b in bullets]
    unique_openers = len(set(openers))
    diff_score = (unique_openers / len(bullets)) * 4 if bullets else 0
    if unique_openers < len(bullets):
        issues.append("Multiple bullets open with the same phrase — looks redundant")

    return count_score + benefit_score + util_score + diff_score, issues


def _score_backend(listing: dict, platform: str) -> tuple[float, list[str]]:
    """Dimension 4: Backend / structured fields. Returns (score_out_of_15, notes)."""
    issues: list[str] = []

    # Field utilization (6 pts) — varies by platform
    if platform == "amazon":
        terms = listing.get("backend_search_terms", "")
        bytes_used = len(terms.encode("utf-8"))
        util = min(1.0, bytes_used / 250)
        util_score = util * 6
        if bytes_used < 200:
            issues.append(f"Backend search terms only use {bytes_used}/250 bytes — fill it up")
    elif platform == "etsy":
        tags = listing.get("tags", []) or []
        util_score = (len(tags) / 13) * 6
        if len(tags) < 13:
            issues.append(f"Only {len(tags)} of 13 tag slots used")
    elif platform in ("ebay", "walmart", "tiktok_shop"):
        attrs_filled = listing.get("attributes_filled", 0)
        attrs_total = listing.get("attributes_total", 0) or 1
        util_score = (attrs_filled / attrs_total) * 6
        if attrs_filled < attrs_total:
            issues.append(f"Attributes: {attrs_filled}/{attrs_total} filled")
    else:
        util_score = 4.0  # shopify has no equivalent — give partial credit

    # No duplication with front-end fields (5 pts) — Amazon-specific check
    no_dup_score = 5.0
    if platform == "amazon":
        terms = listing.get("backend_search_terms", "").lower()
        title = listing.get("title", "").lower()
        if terms and title:
            term_words = set(terms.split())
            title_words = set(title.split())
            overlap = len(term_words & title_words)
            overlap_pct = overlap / max(1, len(term_words))
            if overlap_pct > 0.5:
                no_dup_score = 2.0
                issues.append(f"Backend search terms ~{int(overlap_pct*100)}% overlap with title — wasted bytes")
            elif overlap_pct > 0.3:
                no_dup_score = 3.5

    # Uniqueness across catalog (4 pts) — only meaningful in bulk mode; default 4
    uniqueness_score = 4.0

    return util_score + no_dup_score + uniqueness_score, issues


def _score_completeness(listing: dict, platform: str) -> tuple[float, list[str]]:
    """Dimension 5: Completeness. Returns (score_out_of_15, notes)."""
    issues: list[str] = []

    if platform == "shopify":
        score = 0.0
        meta_desc = listing.get("meta_description", "") or ""
        if meta_desc and len(meta_desc) <= 160:
            score += 4.0
        else:
            issues.append("Meta description missing or over 160 chars")

        images = listing.get("images", []) or []
        if images:
            with_alt = sum(1 for img in images if (isinstance(img, dict) and img.get("alt")))
            if with_alt == len(images):
                score += 3.0
            elif with_alt > 0:
                score += 1.5
                issues.append(f"{len(images) - with_alt} of {len(images)} images missing alt text")
            else:
                issues.append("No images have alt text")
        else:
            issues.append("No images on listing")

        handle = listing.get("url_handle", "") or ""
        if handle and "-" in handle and not any(c.isupper() for c in handle):
            score += 3.0
        elif handle:
            score += 1.5
            issues.append("URL handle could be improved (lowercase, keyword-rich, hyphen-separated)")
        else:
            issues.append("URL handle missing")

        if listing.get("schema_present"):
            score += 3.0
        else:
            issues.append("Product schema markup not detected")

        # Category assignment (2 pts) — default credit
        score += 2.0
        return score, issues

    # For marketplaces — rescale to attribute completion + image count + main image
    attrs_filled = listing.get("attributes_filled", 0)
    attrs_total = listing.get("attributes_total", 0) or 1
    attr_score = (attrs_filled / attrs_total) * 10

    image_count = listing.get("images_count", 0)
    img_target = {"amazon": 7, "etsy": 5, "ebay": 5, "walmart": 4, "tiktok_shop": 4}.get(platform, 5)
    img_score = min(5.0, (image_count / img_target) * 5)
    if image_count < img_target:
        issues.append(f"Image count: {image_count}/{img_target} target")

    return attr_score + img_score, issues


def score(listing: dict, keywords_ranked: list, platform: str) -> dict:
    """
    Compute the full 0-100 score for a listing on a given platform.

    Returns:
        {
          "platform": str,
          "total": float (0-100),
          "subscores": {"keyword_coverage": ..., "title_strength": ..., ...},
          "issues": [str, ...]
        }
    """
    keywords = _normalize_keywords(keywords_ranked)
    top_keyword = keywords[0] if keywords else None

    title = listing.get("title", "") or ""
    bullets = listing.get("bullets", []) or []
    description = listing.get("description", "") or ""
    # Used for keyword-coverage calculation: full searchable text
    listing_text = " ".join([
        title,
        " ".join(bullets),
        description,
        listing.get("backend_search_terms", "") or "",
    ])

    all_issues: list[str] = []
    sub: dict[str, float] = {}

    kc_score, kc_issues = _score_keyword_coverage(listing_text, keywords)
    sub["keyword_coverage"] = round(kc_score, 1)
    all_issues.extend(kc_issues)

    ts_score, ts_issues = _score_title_strength(title, platform, top_keyword)
    sub["title_strength"] = round(ts_score, 1)
    all_issues.extend(ts_issues)

    bq_score, bq_issues = _score_bullets(bullets, platform, keywords)
    sub["bullet_quality"] = round(bq_score, 1)
    all_issues.extend(bq_issues)

    bk_score, bk_issues = _score_backend(listing, platform)
    sub["backend_structured"] = round(bk_score, 1)
    all_issues.extend(bk_issues)

    cp_score, cp_issues = _score_completeness(listing, platform)
    sub["completeness"] = round(cp_score, 1)
    all_issues.extend(cp_issues)

    total = sum(sub.values())
    return {
        "platform": platform,
        "total": round(total, 1),
        "subscores": sub,
        "issues": all_issues,
    }


def interpret(total: float) -> str:
    """Convert a numeric score to the qualitative band in the rubric."""
    if total >= 90:
        return "Excellent"
    if total >= 75:
        return "Strong"
    if total >= 60:
        return "Mediocre"
    if total >= 40:
        return "Weak"
    return "Poor"


# Convenience aliases (so callers can be platform-specific without if/else)
def score_amazon(listing, keywords):
    return score(listing, keywords, "amazon")


def score_shopify(listing, keywords):
    return score(listing, keywords, "shopify")


def score_etsy(listing, keywords):
    return score(listing, keywords, "etsy")


def score_ebay(listing, keywords):
    return score(listing, keywords, "ebay")


def score_walmart(listing, keywords):
    return score(listing, keywords, "walmart")


def score_tiktok_shop(listing, keywords):
    return score(listing, keywords, "tiktok_shop")


def _cli():
    parser = argparse.ArgumentParser(description="Apply the listing audit rubric.")
    parser.add_argument("listing_json", help="Path to listing JSON (title, bullets, description, etc.)")
    parser.add_argument("keywords_json", help="Path to ranked keywords JSON (list of strings or list of dicts)")
    parser.add_argument("platform", choices=list(TITLE_RANGES.keys()), help="Platform to score against")
    args = parser.parse_args()

    listing = json.loads(Path(args.listing_json).read_text(encoding="utf-8"))
    keywords = json.loads(Path(args.keywords_json).read_text(encoding="utf-8"))
    result = score(listing, keywords, args.platform)
    result["interpretation"] = interpret(result["total"])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    _cli()
