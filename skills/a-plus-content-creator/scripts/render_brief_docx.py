"""
Render the A+ Content brief to a polished .docx file.

The brief is the buyer-facing deliverable: every picked module with copy,
character counts, image preview (when generated), or Canva brief (when not),
plus the compliance check and Amazon publishing instructions.

Input JSON shape:
    {
      "product_name": "...",
      "brand_name": "...",
      "generated_at": "2026-05-22",
      "image_source": "fal_ai | canva_briefs | mixed",
      "modules_picked_rationale": "One paragraph explaining the picks.",
      "modules": [
        {
          "module_id": 2,
          "module_name": "Image Header With Text",
          "purpose": "Page hero — sets tone, names value proposition.",
          "copy": {
            "headline": {"text": "...", "limit": 150},
            "body": {"text": "...", "limit": 500},
            "image_alt": {"text": "...", "limit": 100}
          },
          "image": {
            "source": "fal | canva_brief | use_your_own_photo",
            "spec_dimensions": "970 x 600 px",
            "generated_path": "/path/to/aplus_module-2-hero.png",  // if fal
            "canva_brief": "Detailed brief text...",               // if canva
            "notes": "Recommended source: your own product photo"  // if use_your_own
          }
        },
        ...
      ],
      "compliance_check": {
        "prohibited_claims": "pass",
        "external_urls": "pass",
        "competitor_names": "pass",
        "pricing_language": "pass",
        "prohibited_ctas": "pass",
        "character_limits": "pass",
        "image_dimensions": "pass",
        "trademark_symbols": "pass",
        "testimonial_attribution": "pass",
        "issues": []
      },
      "keywords_used": ["...", "..."],
      "keywords_source": "seo_cache | none"
    }

Requires python-docx (pip install python-docx --break-system-packages).
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor


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
    p.add_run(value or "—")


def _add_field_with_count(doc, label: str, text: str, limit: int):
    p = doc.add_paragraph()
    label_run = p.add_run(f"{label} ")
    label_run.bold = True
    count_run = p.add_run(f"({len(text)}/{limit})")
    count_run.italic = True
    if len(text) > limit:
        count_run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
    doc.add_paragraph(text)


def _render_metadata(doc, data: dict):
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(f"{data.get('product_name', 'Untitled')} — Amazon A+ Content Brief")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    meta_run = meta_p.add_run(
        f"Generated {data.get('generated_at', '')}  ·  "
        f"Brand: {data.get('brand_name', '')}  ·  "
        f"Image source: {data.get('image_source', 'unknown')}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    modules_count = len(data.get("modules", []) or [])
    _add_kv(doc, "Modules picked", str(modules_count))

    kw_used = data.get("keywords_used", []) or []
    kw_src = data.get("keywords_source", "none")
    if kw_used:
        _add_kv(doc, "Keywords used", ", ".join(kw_used) + f"  (source: {kw_src})")
    else:
        _add_kv(doc, "Keywords used", "none — run Listing SEO Optimizer first for SEO-weighted A+ Content")


def _render_rationale(doc, rationale: str):
    if not rationale:
        return
    _add_divider(doc)
    _add_section_header(doc, "MODULE SELECTION RATIONALE")
    doc.add_paragraph(rationale)


def _render_module(doc, module: dict, index: int):
    _add_divider(doc)
    module_name = module.get("module_name", "Module")
    module_id = module.get("module_id", index + 1)
    _add_section_header(doc, f"MODULE {index + 1} — {module_name} (Amazon Module ID {module_id})")

    purpose = module.get("purpose")
    if purpose:
        p = doc.add_paragraph()
        run = p.add_run(f"Purpose: {purpose}")
        run.italic = True
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    image = module.get("image", {}) or {}
    if image:
        _add_subheader(doc, "Image")
        source = image.get("source", "unknown")
        spec = image.get("spec_dimensions", "")
        _add_kv(doc, "Source", source)
        if spec:
            _add_kv(doc, "Spec dimensions", spec)

        gen_path = image.get("generated_path")
        if source == "fal" and gen_path and Path(gen_path).exists():
            try:
                doc.add_picture(str(gen_path), width=Inches(5.0))
            except Exception as exc:
                doc.add_paragraph(f"[Could not embed generated image: {exc}]")
                doc.add_paragraph(f"Generated image saved to: {gen_path}")
        elif source == "canva_brief":
            _add_subheader(doc, "Canva brief")
            doc.add_paragraph(image.get("canva_brief", ""))
        elif source == "use_your_own_photo":
            doc.add_paragraph(image.get("notes", "Use your own photo for this module."))

    copy = module.get("copy", {}) or {}
    if copy:
        _add_subheader(doc, "Copy")
        for key, field in copy.items():
            if not isinstance(field, dict):
                continue
            label = key.replace("_", " ").title()
            text = field.get("text", "") or ""
            limit = int(field.get("limit", 0)) if field.get("limit") else None
            if limit:
                _add_field_with_count(doc, label, text, limit)
            else:
                _add_kv(doc, label, text)


def _render_compliance_check(doc, check: dict):
    if not check:
        return
    _add_divider(doc)
    _add_section_header(doc, "COMPLIANCE CHECK")

    checks_order = [
        ("prohibited_claims", "No prohibited claims"),
        ("external_urls", "No external URLs"),
        ("competitor_names", "No competitor names"),
        ("pricing_language", "No pricing language"),
        ("prohibited_ctas", "No prohibited CTAs"),
        ("character_limits", "All character limits respected"),
        ("image_dimensions", "All images within size + dimension limits"),
        ("trademark_symbols", "Trademark symbols accurate"),
        ("testimonial_attribution", "Reviews / testimonials properly genericized"),
    ]
    for key, label in checks_order:
        status = check.get(key, "?")
        glyph = "✓" if status == "pass" else "✗" if status == "fail" else "?"
        p = doc.add_paragraph()
        p.add_run(f"{glyph} {label}: ").bold = (status == "fail")
        run = p.add_run(str(status))
        if status == "fail":
            run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    issues = check.get("issues", []) or []
    if issues:
        _add_subheader(doc, "Issues found (fix before submitting):")
        for issue in issues:
            p = doc.add_paragraph(issue, style="List Bullet")
            for r in p.runs:
                r.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)


def _render_publishing_instructions(doc):
    _add_divider(doc)
    _add_section_header(doc, "HOW TO PUBLISH")
    steps = [
        "Sign into Amazon Seller Central.",
        "Brands menu → A+ Content Manager → Create A+ Content → Standard A+.",
        "For each module: pick the matching module type from Amazon's menu, paste the copy from this brief, upload the image.",
        "Use the alt text from this brief for each image (Amazon shows it in a separate field).",
        "Save & submit for Amazon review (typically 1-7 days).",
        "Once approved, the A+ Content goes live on the listing. Monitor conversion in Seller Central → Brand Analytics for 30+ days before iterating.",
    ]
    for i, step in enumerate(steps, 1):
        doc.add_paragraph(f"{i}. {step}", style="List Number")


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_metadata(doc, data)
    _render_rationale(doc, data.get("modules_picked_rationale", ""))

    modules = data.get("modules", []) or []
    for i, module in enumerate(modules):
        _render_module(doc, module, i)

    _render_compliance_check(doc, data.get("compliance_check", {}))
    _render_publishing_instructions(doc)

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
