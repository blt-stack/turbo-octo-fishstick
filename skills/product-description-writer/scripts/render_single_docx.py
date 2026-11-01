"""
Render a single-product description set to a .docx file.

Takes a structured dict of generated copy (one entry per platform per variant)
and renders it into a clean, copy-paste-ready Word document.

Usage:
    python render_single_docx.py <generated_json> <output_path>

Where <generated_json> is a JSON file with this shape:
    {
      "product_name": "River Stone Pour-Over",
      "brand_name": "Buyer's Brand",
      "source": "Shopify | URL | pasted | photo",
      "generated_at": "2026-05-21",
      "platforms": {
        "shopify": {
          "v1": {"angle": "Story-led", "title": "...", "hero": "...", "value_props": [...], "story": "...", "specs": [...], "faq": [...], "meta_description": "..."},
          "v2": {...}
        },
        "amazon": {
          "v1": {"angle": "Benefit-led", "title": "...", "bullets": [...], "description": "...", "search_terms": "..."},
          "v2": {...}
        },
        ...
      }
    }

Requires python-docx (install with `pip install python-docx --break-system-packages`).
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

# Character limits per platform field — used for the inline count annotations.
LIMITS = {
    "amazon": {"title": 200, "bullet": 250, "description": 2000, "search_terms_bytes": 250},
    "etsy": {"title": 140, "tag": 20, "tags_count": 13},
    "ebay": {"title": 80},
    "walmart": {"title": 200, "bullet": 80},
    "tiktok_shop": {"product_name": 34, "description": 800},
    "shopify": {"meta_description": 160},
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


def _count_annot(actual: int, limit: int) -> str:
    return f"({actual}/{limit})"


def _add_field(doc, label: str, value: str, limit: int | None = None):
    p = doc.add_paragraph()
    run_label = p.add_run(f"{label} ")
    run_label.bold = True
    if limit is not None:
        run_count = p.add_run(_count_annot(len(value), limit) + " ")
        run_count.italic = True
        if len(value) > limit:
            run_count.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
    doc.add_paragraph(value)


def _render_shopify(doc, variant: dict, variant_num: int):
    _add_subheader(doc, f"SHOPIFY — Variant {variant_num} (Angle: {variant.get('angle', '—')})")
    _add_field(doc, "Title", variant.get("title", ""))
    _add_field(doc, "Hero hook", variant.get("hero", ""))

    doc.add_paragraph().add_run("Value props").bold = True
    for vp in variant.get("value_props", []):
        doc.add_paragraph(vp, style="List Bullet")

    doc.add_paragraph().add_run("Story").bold = True
    doc.add_paragraph(variant.get("story", ""))

    doc.add_paragraph().add_run("Specs").bold = True
    for spec in variant.get("specs", []):
        doc.add_paragraph(spec, style="List Bullet")

    doc.add_paragraph().add_run("FAQ").bold = True
    for qa in variant.get("faq", []):
        p = doc.add_paragraph()
        p.add_run(f"Q: {qa.get('q', '')}").bold = True
        doc.add_paragraph(f"A: {qa.get('a', '')}")

    _add_field(
        doc,
        "Meta description",
        variant.get("meta_description", ""),
        limit=LIMITS["shopify"]["meta_description"],
    )


def _render_amazon(doc, variant: dict, variant_num: int):
    _add_subheader(doc, f"AMAZON — Variant {variant_num} (Angle: {variant.get('angle', '—')})")
    _add_field(doc, "Title", variant.get("title", ""), limit=LIMITS["amazon"]["title"])
    for i, bullet in enumerate(variant.get("bullets", []), 1):
        _add_field(doc, f"Bullet {i}", bullet, limit=LIMITS["amazon"]["bullet"])
    _add_field(doc, "Description", variant.get("description", ""), limit=LIMITS["amazon"]["description"])
    _add_field(
        doc,
        "Backend search terms",
        variant.get("search_terms", ""),
        limit=LIMITS["amazon"]["search_terms_bytes"],
    )


def _render_etsy(doc, variant: dict, variant_num: int):
    _add_subheader(doc, f"ETSY — Variant {variant_num} (Angle: {variant.get('angle', '—')})")
    _add_field(doc, "Title", variant.get("title", ""), limit=LIMITS["etsy"]["title"])
    doc.add_paragraph().add_run("Description").bold = True
    doc.add_paragraph(variant.get("description", ""))
    tags = variant.get("tags", [])
    doc.add_paragraph().add_run(f"Tags ({len(tags)}/{LIMITS['etsy']['tags_count']})").bold = True
    doc.add_paragraph(", ".join(tags))


def _render_ebay(doc, variant: dict, variant_num: int):
    _add_subheader(doc, f"EBAY — Variant {variant_num} (Angle: {variant.get('angle', '—')})")
    _add_field(doc, "Title", variant.get("title", ""), limit=LIMITS["ebay"]["title"])
    doc.add_paragraph().add_run("Condition").bold = True
    doc.add_paragraph(variant.get("condition", ""))
    doc.add_paragraph().add_run("Item specifics").bold = True
    for spec in variant.get("item_specifics", []):
        doc.add_paragraph(spec, style="List Bullet")
    doc.add_paragraph().add_run("Description").bold = True
    doc.add_paragraph(variant.get("description", ""))


def _render_walmart(doc, variant: dict, variant_num: int):
    _add_subheader(doc, f"WALMART — Variant {variant_num} (Angle: {variant.get('angle', '—')})")
    _add_field(doc, "Product name", variant.get("title", ""), limit=LIMITS["walmart"]["title"])
    doc.add_paragraph().add_run("Key features").bold = True
    for bullet in variant.get("bullets", []):
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(bullet)
        if len(bullet) > LIMITS["walmart"]["bullet"]:
            run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
    doc.add_paragraph().add_run("Description").bold = True
    doc.add_paragraph(variant.get("description", ""))


def _render_tiktok_shop(doc, variant: dict, variant_num: int):
    _add_subheader(doc, f"TIKTOK SHOP — Variant {variant_num} (Angle: {variant.get('angle', '—')})")
    _add_field(doc, "Product name", variant.get("title", ""), limit=LIMITS["tiktok_shop"]["product_name"])
    _add_field(doc, "Description", variant.get("description", ""), limit=LIMITS["tiktok_shop"]["description"])
    hashtags = variant.get("hashtags", [])
    if hashtags:
        doc.add_paragraph().add_run("Hashtags").bold = True
        doc.add_paragraph(" ".join(hashtags))


RENDERERS = {
    "shopify": _render_shopify,
    "amazon": _render_amazon,
    "etsy": _render_etsy,
    "ebay": _render_ebay,
    "walmart": _render_walmart,
    "tiktok_shop": _render_tiktok_shop,
}


def render(data: dict, output_path: Path) -> Path:
    doc = Document()

    # Title block
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(data.get("product_name", "Untitled Product"))
    title_run.bold = True
    title_run.font.size = Pt(20)

    meta_p = doc.add_paragraph()
    meta_run = meta_p.add_run(
        f"Generated {data.get('generated_at', '')}  ·  "
        f"Brand: {data.get('brand_name', '')}  ·  "
        f"Source: {data.get('source', 'unknown')}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    platforms = data.get("platforms", {})
    for platform_key in PLATFORM_DISPLAY_ORDER:
        platform_data = platforms.get(platform_key)
        if not platform_data:
            continue
        renderer = RENDERERS.get(platform_key)
        if not renderer:
            continue
        _add_divider(doc)
        _add_section_header(doc, PLATFORM_DISPLAY_NAMES[platform_key])
        for variant_key in ("v1", "v2"):
            variant = platform_data.get(variant_key)
            if not variant:
                continue
            renderer(doc, variant, int(variant_key[-1]))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_single_docx.py <generated_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
