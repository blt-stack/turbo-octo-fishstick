"""
Render a batch of reviews + drafted replies to a 4-sheet .xlsx workbook.

Sheets:
  1. Reply Queue              — one row per review with public reply + private follow-up + dispute + status
  2. Tier & Sentiment Breakdown — tier counts, sentiment distribution, NPS-style summary
  3. Cache Mining Summary     — testimonials extracted, objections extracted, keyword enrichments
  4. Systemic Issues          — auto-detected recurring patterns worth fixing operationally

Input JSON shape:
    {
      "brand_name": "...",
      "generated_at": "2026-05-22",
      "reviews": [
        {  # one per review
          "review_id": "...",
          "received_at": "2026-05-10",
          "platform": "judge_me",
          "product_name": "...",
          "reviewer_name": "...",
          "reviewer_email": "...",
          "verified_purchase": true,
          "star_rating": 5,
          "tier": "amplify",
          "sentiment": "constructive",
          "issue_category": "",
          "review_title": "...",
          "review_body": "...",
          "public_reply": {"body": "...", "character_count": 178, "character_limit": 5000},
          "private_followup": {"subject": "...", "body": "..."},
          "dispute_draft": ""
        },
        ...
      ],
      "cache_mining": {
        "testimonials": [
          {"quote": "...", "reviewer": "Sam K.", "product": "...", "score": 87},
          ...
        ],
        "objections": [
          {"objection": "...", "category": "shipping", "frequency_tag": "systemic"},
          ...
        ],
        "keyword_enrichments": [
          {"phrase": "...", "occurrences": 5, "products": ["..."]},
          ...
        ]
      },
      "systemic_issues": [
        {
          "pattern": "...",
          "review_count": 5,
          "first_seen": "...",
          "recommendation": "..."
        },
        ...
      ]
    }

Requires openpyxl (pip install openpyxl --break-system-packages).
"""

import json
import sys
from collections import Counter
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


TIER_DISPLAY = {
    "recovery": "Recovery (1-2★)",
    "clarify": "Clarify (3★)",
    "amplify": "Amplify (4-5★)",
}

PLATFORM_DISPLAY = {
    "shopify_judge_me": "Judge.me",
    "shopify_loox": "Loox",
    "shopify_yotpo": "Yotpo",
    "shopify_stamped": "Stamped",
    "shopify_reviews_io": "Reviews.io",
    "judge_me": "Judge.me",
    "loox": "Loox",
    "yotpo": "Yotpo",
    "amazon": "Amazon",
    "etsy": "Etsy",
    "google": "Google",
    "trustpilot": "Trustpilot",
    "facebook": "Facebook",
}

TIER_FILLS = {
    "recovery": PatternFill("solid", fgColor="FFC7CE"),
    "clarify": PatternFill("solid", fgColor="FFEB9C"),
    "amplify": PatternFill("solid", fgColor="C6EFCE"),
}

SENTIMENT_FILLS = {
    "constructive": PatternFill("solid", fgColor="FFFFFF"),
    "abusive": PatternFill("solid", fgColor="FFC7CE"),
    "fake": PatternFill("solid", fgColor="F7CAAC"),
    "sycophantic": PatternFill("solid", fgColor="FFEB9C"),
}

STATUS_FILLS = {
    "Pending review": PatternFill("solid", fgColor="FFEB9C"),
    "Approved": PatternFill("solid", fgColor="D9E1F2"),
    "Sent": PatternFill("solid", fgColor="C6E0B4"),
    "Held": PatternFill("solid", fgColor="F7CAAC"),
    "Disputed": PatternFill("solid", fgColor="FFC7CE"),
}

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")


def _write_reply_queue(ws, reviews: list[dict]):
    headers = [
        "Received",
        "Platform",
        "Star",
        "Reviewer",
        "Verified",
        "Product",
        "Tier",
        "Sentiment",
        "Issue Category",
        "Original Review",
        "Drafted Public Reply",
        "Char Count",
        "Private Follow-up",
        "Dispute Draft",
        "Status",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for review in reviews:
        public_reply = review.get("public_reply", {}) or {}
        followup = review.get("private_followup", {}) or {}
        original = review.get("review_body", "")
        if review.get("review_title"):
            original = f"[{review['review_title']}]\n\n{original}"
        followup_text = ""
        if followup.get("body"):
            sub = followup.get("subject", "")
            followup_text = (f"Subject: {sub}\n\n" if sub else "") + followup["body"]
        row = [
            review.get("received_at", ""),
            PLATFORM_DISPLAY.get(review.get("platform", ""), review.get("platform", "")),
            review.get("star_rating", ""),
            review.get("reviewer_name", ""),
            "Y" if review.get("verified_purchase") else "N",
            review.get("product_name", ""),
            TIER_DISPLAY.get(review.get("tier", ""), review.get("tier", "")),
            review.get("sentiment", "constructive"),
            review.get("issue_category", ""),
            original,
            public_reply.get("body", ""),
            public_reply.get("character_count", ""),
            followup_text,
            review.get("dispute_draft", ""),
            "Pending review",
        ]
        ws.append(row)

        row_idx = ws.max_row
        tier = review.get("tier", "")
        sentiment = review.get("sentiment", "constructive")
        if tier in TIER_FILLS:
            ws.cell(row=row_idx, column=7).fill = TIER_FILLS[tier]
        if sentiment in SENTIMENT_FILLS:
            ws.cell(row=row_idx, column=8).fill = SENTIMENT_FILLS[sentiment]
        ws.cell(row=row_idx, column=15).fill = STATUS_FILLS["Pending review"]

    widths = [14, 14, 6, 18, 8, 22, 18, 14, 16, 50, 60, 10, 50, 50, 14]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions


def _write_tier_breakdown(ws, reviews: list[dict]):
    ws.append(["Metric", "Value"])
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    ws.append(["Total reviews in batch", len(reviews)])

    tier_counts = Counter(r.get("tier", "") for r in reviews)
    ws.append([])
    ws.append(["Tier distribution", ""])
    for tier in ("recovery", "clarify", "amplify"):
        ws.append([f"  {TIER_DISPLAY.get(tier, tier)}", tier_counts.get(tier, 0)])

    star_counts = Counter(r.get("star_rating", "") for r in reviews)
    ws.append([])
    ws.append(["Star distribution", ""])
    for star in (1, 2, 3, 4, 5):
        ws.append([f"  {star}★", star_counts.get(star, 0)])

    sent_counts = Counter(r.get("sentiment", "constructive") for r in reviews)
    ws.append([])
    ws.append(["Sentiment distribution", ""])
    for sent in ("constructive", "abusive", "fake", "sycophantic"):
        ws.append([f"  {sent}", sent_counts.get(sent, 0)])

    plat_counts = Counter(PLATFORM_DISPLAY.get(r.get("platform", ""), r.get("platform", "")) for r in reviews)
    ws.append([])
    ws.append(["Platform breakdown", ""])
    for plat, count in plat_counts.most_common():
        if plat:
            ws.append([f"  {plat}", count])

    issue_counts = Counter(r.get("issue_category", "") for r in reviews if r.get("issue_category"))
    if issue_counts:
        ws.append([])
        ws.append(["Issue categories (recovery/clarify tier)", ""])
        for issue, count in issue_counts.most_common():
            ws.append([f"  {issue}", count])

    # NPS-style summary
    promoters = sum(1 for r in reviews if r.get("star_rating", 0) >= 4)
    detractors = sum(1 for r in reviews if r.get("star_rating", 0) <= 2)
    passives = len(reviews) - promoters - detractors
    nps_score = ((promoters - detractors) / len(reviews) * 100) if reviews else 0
    ws.append([])
    ws.append(["NPS-style summary", ""])
    ws.append([f"  Promoters (4-5★)", promoters])
    ws.append([f"  Passives (3★)", passives])
    ws.append([f"  Detractors (1-2★)", detractors])
    ws.append([f"  NPS-style score", f"{nps_score:+.1f}"])

    widths = [40, 18]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def _write_cache_mining(ws, cache_mining: dict):
    cache_mining = cache_mining or {}
    testimonials = cache_mining.get("testimonials", []) or []
    objections = cache_mining.get("objections", []) or []
    keyword_enrichments = cache_mining.get("keyword_enrichments", []) or []

    ws.append(["Section", "Detail"])
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    ws.append(["TESTIMONIAL MINING", ""])
    ws.append(["  Quotes extracted", len(testimonials)])
    for i, t in enumerate(testimonials, 1):
        quote = t.get("quote", "")
        reviewer = t.get("reviewer", "")
        product = t.get("product", "")
        score = t.get("score", "")
        ws.append([f"  Quote #{i}", f"\"{quote}\" — {reviewer} ({product}, score {score})"])

    ws.append([])
    ws.append(["OBJECTION MINING", ""])
    ws.append(["  Objections extracted", len(objections)])
    for i, o in enumerate(objections, 1):
        text = o.get("objection", "")
        cat = o.get("category", "")
        freq = o.get("frequency_tag", "")
        ws.append([f"  Objection #{i}", f"{text} [category: {cat} · {freq}]"])

    ws.append([])
    ws.append(["KEYWORD ENRICHMENT", ""])
    ws.append(["  Phrases enriched", len(keyword_enrichments)])
    for i, k in enumerate(keyword_enrichments, 1):
        phrase = k.get("phrase", "")
        occ = k.get("occurrences", "")
        prods = ", ".join(k.get("products", []))
        ws.append([f"  Phrase #{i}", f"\"{phrase}\" ({occ} occurrences across: {prods})"])

    if not testimonials and not objections and not keyword_enrichments:
        ws.append([])
        ws.append(["(No cache mining outputs from this batch.)", ""])

    widths = [30, 90]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"


def _write_systemic_issues(ws, issues: list[dict]):
    headers = ["Pattern", "Review Count", "First Seen", "Recommendation"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for issue in issues:
        ws.append([
            issue.get("pattern", ""),
            issue.get("review_count", ""),
            issue.get("first_seen", ""),
            issue.get("recommendation", ""),
        ])

    if not issues:
        ws.append(["(No systemic issues detected in this batch.)", "", "", ""])

    widths = [40, 14, 14, 70]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"


def render(data: dict, output_path: Path) -> Path:
    reviews = data.get("reviews", []) or []
    cache_mining = data.get("cache_mining", {}) or {}
    systemic_issues = data.get("systemic_issues", []) or []

    wb = Workbook()
    ws_queue = wb.active
    ws_queue.title = "Reply Queue"
    _write_reply_queue(ws_queue, reviews)

    ws_breakdown = wb.create_sheet("Tier & Sentiment Breakdown")
    _write_tier_breakdown(ws_breakdown, reviews)

    ws_cache = wb.create_sheet("Cache Mining Summary")
    _write_cache_mining(ws_cache, cache_mining)

    ws_systemic = wb.create_sheet("Systemic Issues")
    _write_systemic_issues(ws_systemic, systemic_issues)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_reviews_xlsx.py <batch_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
