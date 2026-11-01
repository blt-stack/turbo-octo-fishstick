"""
Render a single-product SEO audit + rewrites to a .docx file.

The audit data is produced by the LLM driving the skill (using the rubric in
templates/audit-rubric.md and the platform guides). This script is the
deterministic renderer that turns the generated data into a polished Word
document the buyer can use.

Input JSON shape:
    {
      "product_name": "...",
      "brand_name": "...",
      "source": "Shopify | URL | pasted | greenfield",
      "generated_at": "2026-05-21",
      "scores": {
        "shopify": {"total": 72, "subscores": {...}, "issues": [...], "interpretation": "Strong"},
        "amazon": {"total": 61, ...},
        ...
      },
      "keywords_ranked": [{"keyword": "...", "intent": "...", "sources": [...], "rank": 1, "recommended_placement": [...]}, ...],
      "rewrites": {
        "shopify": {"meta_title": "...", "meta_description": "...", "url_handle": "...", "alt_text": [...], "body_notes": "...", "schema_notes": "..."},
        "amazon": {"title": "...", "bullets": [...], "description": "...", "backend_search_terms": "...", "compliance_notes": [...], "a_plus_notes": "..."},
        ...
      },
      "action_checklist": ["...", "...", ...]
    }

Requires python-docx (pip install python-docx --break-system-packages).
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor


PLATFORM_DISPLAY_ORDER = ["shopify", "amazon", "etsy", "ebay", "walmart", "tiktok_shop"]
PLATFORM_DISPLAY_NAMES = {
    "shopify": "Shopify",
    "amazon": "Amazon",
    "etsy": "Etsy",
    "ebay": "eBay",
    "walmart": "Walmart",
    "tiktok_shop": "TikTok Shop",
}


def _band_color(total: float) -> RGBColor:
    if total >= 90:
        return RGBColor(0x1E, 0x7A, 0x2C)  # green
    if total >= 75:
        return RGBColor(0x4E, 0x90, 0x3A)  # light green
    if total >= 60:
        return RGBColor(0xC0, 0x82, 0x00)  # amber
    if total >= 40:
        return RGBColor(0xC0, 0x50, 0x00)  # orange
    return RGBColor(0xC0, 0x00, 0x00)  # red


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


def _add_field(doc, label: str, value: str, limit: int | None = None):
    p = doc.add_paragraph()
    label_run = p.add_run(f"{label}: ")
    label_run.bold = True
    if limit is not None:
        annot_run = p.add_run(f"({len(value)}/{limit}) ")
        annot_run.italic = True
        if len(value) > limit:
            annot_run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
    doc.add_paragraph(value)


def _render_audit_summary(doc, scores: dict):
    _add_divider(doc)
    _add_section_header(doc, "AUDIT SUMMARY")

    for platform_key in PLATFORM_DISPLAY_ORDER:
        if platform_key not in scores:
            continue
        s = scores[platform_key]
        p = doc.add_paragraph()
        name_run = p.add_run(f"{PLATFORM_DISPLAY_NAMES[platform_key]}: ")
        name_run.bold = True
        total_run = p.add_run(f"{s.get('total', 0):.1f}/100")
        total_run.bold = True
        total_run.font.color.rgb = _band_color(s.get("total", 0))
        interp = s.get("interpretation", "")
        if interp:
            interp_run = p.add_run(f"  ({interp})")
            interp_run.italic = True

    # Sub-score table per platform
    for platform_key in PLATFORM_DISPLAY_ORDER:
        if platform_key not in scores:
            continue
        s = scores[platform_key]
        sub = s.get("subscores", {})
        if not sub:
            continue
        _add_subheader(doc, f"{PLATFORM_DISPLAY_NAMES[platform_key]} — sub-score breakdown")
        max_points = {
            "keyword_coverage": 30,
            "title_strength": 20,
            "bullet_quality": 20,
            "backend_structured": 15,
            "completeness": 15,
        }
        for key, max_pts in max_points.items():
            if key in sub:
                label = key.replace("_", " ").title()
                doc.add_paragraph(f"  • {label}: {sub[key]:.1f}/{max_pts}")


def _render_keywords(doc, keywords: list[dict]):
    _add_divider(doc)
    _add_section_header(doc, "KEYWORD RESEARCH")
    if not keywords:
        doc.add_paragraph("(No keywords supplied.)")
        return

    doc.add_paragraph(f"Top {len(keywords)} ranked keywords:")
    for kw in keywords:
        p = doc.add_paragraph(style="List Number")
        rank = kw.get("rank", "")
        run_kw = p.add_run(f"{kw.get('keyword', '')} ")
        run_kw.bold = True
        intent = kw.get("intent", "")
        sources = ", ".join(kw.get("sources", []))
        meta = f"[{intent}] [sources: {sources}]"
        p.add_run(meta).italic = True
        placement = kw.get("recommended_placement", [])
        if placement:
            doc.add_paragraph(f"    → Use in: {', '.join(placement)}")
        notes = kw.get("notes")
        if notes:
            doc.add_paragraph(f"    Note: {notes}")


def _render_platform_rewrite(doc, platform_key: str, rewrite: dict, audit: dict):
    _add_divider(doc)
    _add_section_header(doc, f"{PLATFORM_DISPLAY_NAMES[platform_key].upper()} — Audit + Rewrite")

    issues = audit.get("issues", [])
    if issues:
        _add_subheader(doc, "Issues found")
        for issue in issues:
            doc.add_paragraph(issue, style="List Bullet")

    _add_subheader(doc, "Rewrite")

    if platform_key == "shopify":
        _add_field(doc, "Meta title", rewrite.get("meta_title", ""), limit=60)
        _add_field(doc, "Meta description", rewrite.get("meta_description", ""), limit=160)
        _add_field(doc, "URL handle", rewrite.get("url_handle", ""))
        alt = rewrite.get("alt_text", [])
        if alt:
            doc.add_paragraph("Recommended alt text per image:")
            for i, a in enumerate(alt, 1):
                doc.add_paragraph(f"  Image {i}: {a}")
        body_notes = rewrite.get("body_notes")
        if body_notes:
            _add_subheader(doc, "Body keyword integration notes")
            doc.add_paragraph(body_notes)
        schema_notes = rewrite.get("schema_notes")
        if schema_notes:
            _add_subheader(doc, "Schema markup notes")
            doc.add_paragraph(schema_notes)

    elif platform_key == "amazon":
        _add_field(doc, "Title", rewrite.get("title", ""), limit=200)
        for i, b in enumerate(rewrite.get("bullets", []), 1):
            _add_field(doc, f"Bullet {i}", b, limit=250)
        _add_field(doc, "Description", rewrite.get("description", ""), limit=2000)
        _add_field(doc, "Backend search terms", rewrite.get("backend_search_terms", ""), limit=250)
        compliance = rewrite.get("compliance_notes", [])
        if compliance:
            _add_subheader(doc, "Compliance check")
            for c in compliance:
                doc.add_paragraph(c, style="List Bullet")
        a_plus = rewrite.get("a_plus_notes")
        if a_plus:
            _add_subheader(doc, "A+ Content notes")
            doc.add_paragraph(a_plus)

    elif platform_key == "etsy":
        _add_field(doc, "Title", rewrite.get("title", ""), limit=140)
        tags = rewrite.get("tags", []) or []
        _add_subheader(doc, f"Tags ({len(tags)}/13)")
        for i, t in enumerate(tags, 1):
            doc.add_paragraph(f"  {i}. {t} ({len(t)}/20)")
        attrs = rewrite.get("attributes", {})
        if attrs:
            _add_subheader(doc, "Attributes")
            for k, v in attrs.items():
                doc.add_paragraph(f"  {k}: {v}")
        doc.add_paragraph().add_run("Description").bold = True
        doc.add_paragraph(rewrite.get("description", ""))

    elif platform_key == "ebay":
        _add_field(doc, "Title", rewrite.get("title", ""), limit=80)
        doc.add_paragraph().add_run("Condition").bold = True
        doc.add_paragraph(rewrite.get("condition", ""))
        if rewrite.get("condition_note"):
            doc.add_paragraph(f"Note: {rewrite.get('condition_note', '')}")
        item_specifics = rewrite.get("item_specifics", {})
        if item_specifics:
            _add_subheader(doc, "Item specifics")
            for k, v in item_specifics.items():
                doc.add_paragraph(f"  {k}: {v}")
        doc.add_paragraph().add_run("Description").bold = True
        doc.add_paragraph(rewrite.get("description", ""))

    elif platform_key == "walmart":
        _add_field(doc, "Product name", rewrite.get("title", ""), limit=200)
        _add_subheader(doc, "Key features")
        for b in rewrite.get("bullets", []):
            p = doc.add_paragraph(style="List Bullet")
            run = p.add_run(b)
            if len(b) > 80:
                run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
        doc.add_paragraph().add_run("Description").bold = True
        doc.add_paragraph(rewrite.get("description", ""))
        attrs = rewrite.get("attributes", {})
        if attrs:
            _add_subheader(doc, "Attributes")
            for k, v in attrs.items():
                doc.add_paragraph(f"  {k}: {v}")

    elif platform_key == "tiktok_shop":
        _add_field(doc, "Product name", rewrite.get("title", ""), limit=34)
        _add_field(doc, "Description", rewrite.get("description", ""), limit=800)
        attrs = rewrite.get("attributes", {})
        if attrs:
            _add_subheader(doc, "Attributes")
            for k, v in attrs.items():
                doc.add_paragraph(f"  {k}: {v}")
        hashtags = rewrite.get("hashtags", [])
        if hashtags:
            _add_subheader(doc, "Hashtags")
            doc.add_paragraph(" ".join(hashtags))


def _render_action_checklist(doc, items: list[str]):
    _add_divider(doc)
    _add_section_header(doc, "ACTION CHECKLIST")
    if not items:
        doc.add_paragraph("(No action items.)")
        return
    doc.add_paragraph("Ordered by estimated impact:")
    for item in items:
        doc.add_paragraph(f"☐ {item}", style="List Bullet")


def render(data: dict, output_path: Path) -> Path:
    doc = Document()

    title_p = doc.add_paragraph()
    title_run = title_p.add_run(f"{data.get('product_name', 'Untitled')} — SEO Audit & Optimization")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    meta_run = meta_p.add_run(
        f"Generated {data.get('generated_at', '')}  ·  "
        f"Brand: {data.get('brand_name', '')}  ·  "
        f"Source: {data.get('source', 'unknown')}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    scores = data.get("scores", {})
    if scores:
        _render_audit_summary(doc, scores)

    keywords = data.get("keywords_ranked", [])
    _render_keywords(doc, keywords)

    rewrites = data.get("rewrites", {})
    for platform_key in PLATFORM_DISPLAY_ORDER:
        if platform_key not in rewrites:
            continue
        audit = scores.get(platform_key, {})
        _render_platform_rewrite(doc, platform_key, rewrites[platform_key], audit)

    checklist = data.get("action_checklist", [])
    _render_action_checklist(doc, checklist)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_audit_docx.py <audit_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
