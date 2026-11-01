"""
Render a single review reply to a .docx file.

The .docx is the buyer-facing deliverable for single mode. Contains:
- Review header (reviewer, platform, star rating, tier, sentiment)
- The original review (for reference)
- The drafted public reply (paste-ready, with character count vs limit)
- The drafted private follow-up (when applicable)
- The dispute draft (only for flagged fake/abusive reviews)
- Cache write summary (testimonials, objections, keyword enrichment)

Input JSON shape:
    {
      "brand_name": "...",
      "reviewer_name": "Sarah M.",
      "platform": "judge_me",
      "star_rating": 5,
      "review_title": "Beautiful piece",
      "review_body": "...",
      "received_at": "2026-05-10",
      "verified_purchase": true,
      "product_name": "River Stone Pour-Over",
      "tier": "amplify",
      "sentiment": "constructive",
      "issue_category": "",
      "public_reply": {
        "body": "Hi Sarah,\n\n...\n\n— Jamie",
        "character_count": 178,
        "character_limit": 5000
      },
      "private_followup": {
        "subject": "...",
        "body": "..."
      },
      "dispute_draft": "",
      "cache_writes": {
        "testimonials_added": 1,
        "objections_added": 0,
        "keywords_enriched": 2,
        "testimonial_cache_path": "...",
        "objection_cache_path": "...",
        "keyword_cache_path": "..."
      }
    }

Requires python-docx (pip install python-docx --break-system-packages).
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor


TIER_DISPLAY = {
    "recovery": "Recovery (1-2★)",
    "clarify": "Clarify (3★)",
    "amplify": "Amplify (4-5★)",
}

TIER_COLORS = {
    "recovery": RGBColor(0xC0, 0x00, 0x00),
    "clarify": RGBColor(0xB8, 0x86, 0x0B),
    "amplify": RGBColor(0x1E, 0x7A, 0x2C),
}

SENTIMENT_COLORS = {
    "constructive": RGBColor(0x55, 0x55, 0x55),
    "abusive": RGBColor(0xC0, 0x00, 0x00),
    "fake": RGBColor(0xC0, 0x00, 0x00),
    "sycophantic": RGBColor(0xB8, 0x86, 0x0B),
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
    "google": "Google Business Profile",
    "trustpilot": "Trustpilot",
    "facebook": "Facebook Page Reviews",
}


def _add_divider(doc):
    p = doc.add_paragraph("══════════════════════════════════════════════════")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def _add_section_header(doc, text: str):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)


def _add_subheader(doc, text: str):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(11)


def _add_kv(doc, label: str, value: str):
    p = doc.add_paragraph()
    label_run = p.add_run(f"{label}: ")
    label_run.bold = True
    p.add_run(value if value not in (None, "") else "—")


def _render_header(doc, data: dict):
    title_p = doc.add_paragraph()
    reviewer_name = data.get("reviewer_name", "Unknown Reviewer")
    star = data.get("star_rating", "?")
    platform = PLATFORM_DISPLAY.get(data.get("platform", ""), data.get("platform", ""))
    title_run = title_p.add_run(f"Reply to: {reviewer_name}  ·  {star}★  ·  {platform}")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    received_at = data.get("received_at", "")
    product_name = data.get("product_name", "")
    verified = "verified purchase" if data.get("verified_purchase") else "unverified"
    meta_run = meta_p.add_run(
        f"Posted {received_at}  ·  {product_name}  ·  {verified}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    tier = data.get("tier", "")
    tier_p = doc.add_paragraph()
    tier_run = tier_p.add_run(f"Tier: {TIER_DISPLAY.get(tier, tier)}")
    tier_run.bold = True
    if tier in TIER_COLORS:
        tier_run.font.color.rgb = TIER_COLORS[tier]

    sentiment = data.get("sentiment", "constructive")
    sent_p = doc.add_paragraph()
    sent_run = sent_p.add_run(f"Sentiment: {sentiment}")
    sent_run.bold = True
    if sentiment in SENTIMENT_COLORS:
        sent_run.font.color.rgb = SENTIMENT_COLORS[sentiment]

    if data.get("issue_category"):
        _add_kv(doc, "Issue category", data.get("issue_category"))


def _render_original_review(doc, data: dict):
    _add_divider(doc)
    _add_section_header(doc, "ORIGINAL REVIEW (for reference)")
    if data.get("review_title"):
        _add_subheader(doc, data["review_title"])
    body = data.get("review_body", "")
    if body:
        for paragraph in body.split("\n\n"):
            p = doc.add_paragraph(paragraph)
            for run in p.runs:
                run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def _render_public_reply(doc, reply: dict):
    if not reply:
        return
    _add_divider(doc)
    _add_section_header(doc, "DRAFTED PUBLIC REPLY")
    body = reply.get("body", "")
    if body:
        for paragraph in body.split("\n\n"):
            doc.add_paragraph(paragraph)

    char_count = reply.get("character_count")
    char_limit = reply.get("character_limit")
    if char_count is not None:
        limit_text = f"(limit: {char_limit})" if char_limit else ""
        p = doc.add_paragraph()
        run = p.add_run(f"Character count: {char_count} {limit_text}")
        run.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x77, 0x77, 0x77)


def _render_private_followup(doc, follow_up: dict):
    if not follow_up or not follow_up.get("body"):
        return
    _add_divider(doc)
    _add_section_header(doc, "DRAFTED PRIVATE FOLLOW-UP")
    if follow_up.get("subject"):
        _add_kv(doc, "Subject", follow_up["subject"])
    body = follow_up.get("body", "")
    _add_subheader(doc, "Body")
    for paragraph in body.split("\n\n"):
        doc.add_paragraph(paragraph)


def _render_dispute(doc, dispute_text: str):
    if not dispute_text:
        return
    _add_divider(doc)
    _add_section_header(doc, "DISPUTE DRAFT (platform-removal request)")
    for paragraph in dispute_text.split("\n\n"):
        p = doc.add_paragraph(paragraph)
        for run in p.runs:
            run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def _render_cache_writes(doc, cache: dict):
    if not cache:
        return
    _add_divider(doc)
    _add_section_header(doc, "CACHE WRITES")
    test_added = cache.get("testimonials_added", 0)
    obj_added = cache.get("objections_added", 0)
    kw_enriched = cache.get("keywords_enriched", 0)
    _add_kv(doc, "Testimonials extracted", str(test_added))
    _add_kv(doc, "Objections extracted", str(obj_added))
    _add_kv(doc, "Keyword phrases enriched", str(kw_enriched))
    if cache.get("testimonial_cache_path"):
        _add_kv(doc, "Testimonial cache", cache["testimonial_cache_path"])
    if cache.get("objection_cache_path"):
        _add_kv(doc, "Objection cache", cache["objection_cache_path"])
    if cache.get("keyword_cache_path"):
        _add_kv(doc, "Keyword cache", cache["keyword_cache_path"])


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_header(doc, data)
    _render_original_review(doc, data)
    _render_public_reply(doc, data.get("public_reply", {}))
    _render_private_followup(doc, data.get("private_followup", {}))
    _render_dispute(doc, data.get("dispute_draft", ""))
    _render_cache_writes(doc, data.get("cache_writes", {}))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_review_docx.py <review_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
