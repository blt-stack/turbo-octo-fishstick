"""
Render the landing-page brief to a polished .docx file.

The brief is the designer / VA / founder-facing deliverable. It contains the
page architecture, block-by-block copy, alternate hero blocks, and the A/B
test recommendation. Paired with the HTML output (render_html_sections.py).

Input JSON shape:
    {
      "page_name": "...",                  # product name, collection name, "About Us", etc.
      "page_type": "pdp | collection | marketing_lp | about",
      "brand_name": "...",
      "framework": "PAS",                  # framework used (or "narrative" for About)
      "framework_reason": "...",
      "keywords_used": ["...", "..."],     # may be empty
      "keywords_source": "seo_cache | none",
      "generated_at": "2026-05-21",
      "blocks": [
        {
          "name": "HERO",
          "purpose": "3-second qualification ...",
          "copy": {
            "headline": "...",
            "sub_headline": "...",
            "cta": "...",
            "trust_signals": ["...", "..."]
          },
          "visual_brief": "...",
          "designer_notes": "..."
        },
        ...
      ],
      "alternate_heroes": [
        {"name": "Hero A — Problem-aware", "headline": "...", "sub_headline": "...", "visual_brief": "...", "cta": "..."},
        {"name": "Hero B — Outcome-aware", ...},
        {"name": "Hero C — Social-proof-aware", ...}
      ],
      "ab_test_recommendation": {
        "test_first": "Hero A — Problem-aware",
        "why": "Current hero is feature-led; problem-aware angle is the biggest unknown.",
        "duration_days": 14,
        "expected_lift_band": "5-15% on add-to-cart rate"
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


PAGE_TYPE_DISPLAY = {
    "pdp": "Product Detail Page",
    "collection": "Collection / Category Page",
    "marketing_lp": "Marketing Landing Page",
    "about": "About / Brand Story Page",
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


def _add_kv_line(doc, label: str, value: str):
    p = doc.add_paragraph()
    label_run = p.add_run(f"{label}: ")
    label_run.bold = True
    p.add_run(value or "—")


def _render_metadata(doc, data: dict):
    page_type = data.get("page_type", "pdp")
    type_display = PAGE_TYPE_DISPLAY.get(page_type, page_type)

    title_p = doc.add_paragraph()
    title_run = title_p.add_run(f"{data.get('page_name', 'Untitled')} — Landing Page Brief")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    meta_run = meta_p.add_run(
        f"Generated {data.get('generated_at', '')}  ·  "
        f"Brand: {data.get('brand_name', '')}  ·  "
        f"Page type: {type_display}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    framework = data.get("framework", "—")
    fw_reason = data.get("framework_reason", "")
    fw_line = framework + (f" — {fw_reason}" if fw_reason else "")
    _add_kv_line(doc, "Framework", fw_line)

    kw_used = data.get("keywords_used", []) or []
    kw_src = data.get("keywords_source", "none")
    if kw_used:
        kw_line = ", ".join(kw_used) + f"  (source: {kw_src})"
    else:
        kw_line = "none — Listing SEO Optimizer cache empty for this product"
    _add_kv_line(doc, "Keywords used", kw_line)


def _render_block_copy(doc, copy: dict | str):
    """A block's copy can be a dict (structured) or a string (free-form prose)."""
    if isinstance(copy, str):
        doc.add_paragraph(copy)
        return
    if not isinstance(copy, dict):
        doc.add_paragraph(str(copy))
        return

    for key, value in copy.items():
        label = key.replace("_", " ").title()
        if isinstance(value, list):
            doc.add_paragraph().add_run(f"{label}:").bold = True
            for item in value:
                doc.add_paragraph(str(item), style="List Bullet")
        elif isinstance(value, dict):
            doc.add_paragraph().add_run(f"{label}:").bold = True
            for sub_k, sub_v in value.items():
                doc.add_paragraph(f"  {sub_k}: {sub_v}")
        else:
            p = doc.add_paragraph()
            p.add_run(f"{label}: ").bold = True
            p.add_run(str(value))


def _render_blocks(doc, blocks: list[dict]):
    _add_divider(doc)
    _add_section_header(doc, "PAGE ARCHITECTURE")
    for block in blocks:
        name = block.get("name", "BLOCK")
        purpose = block.get("purpose", "")
        _add_subheader(doc, name)
        if purpose:
            p = doc.add_paragraph()
            p.add_run("Purpose: ").italic = True
            run = p.add_run(purpose)
            run.italic = True
            run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        copy = block.get("copy", "")
        if copy:
            _render_block_copy(doc, copy)
        visual = block.get("visual_brief")
        if visual:
            p = doc.add_paragraph()
            p.add_run("Visual brief: ").bold = True
            p.add_run(visual)
        notes = block.get("designer_notes")
        if notes:
            p = doc.add_paragraph()
            p.add_run("Designer notes: ").bold = True
            p.add_run(notes)


def _render_alternate_heroes(doc, alternates: list[dict]):
    _add_divider(doc)
    _add_section_header(doc, "ALTERNATE HERO BLOCKS (for A/B testing)")
    for alt in alternates:
        _add_subheader(doc, alt.get("name", "ALTERNATE HERO"))
        _add_kv_line(doc, "Headline", alt.get("headline", ""))
        _add_kv_line(doc, "Sub-headline", alt.get("sub_headline", ""))
        _add_kv_line(doc, "Visual brief", alt.get("visual_brief", ""))
        _add_kv_line(doc, "CTA", alt.get("cta", ""))


def _render_ab_recommendation(doc, rec: dict):
    _add_divider(doc)
    _add_section_header(doc, "RECOMMENDED A/B TEST")
    _add_kv_line(doc, "Test first", rec.get("test_first", "—"))
    _add_kv_line(doc, "Why", rec.get("why", "—"))
    duration = rec.get("duration_days", "")
    if duration:
        _add_kv_line(doc, "Test duration", f"{duration} days")
    band = rec.get("expected_lift_band")
    if band:
        _add_kv_line(doc, "Expected lift band", band)


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_metadata(doc, data)

    blocks = data.get("blocks", []) or []
    if blocks:
        _render_blocks(doc, blocks)

    alternates = data.get("alternate_heroes", []) or []
    if alternates:
        _render_alternate_heroes(doc, alternates)

    rec = data.get("ab_test_recommendation")
    if rec:
        _render_ab_recommendation(doc, rec)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_brief_docx.py <brief_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
