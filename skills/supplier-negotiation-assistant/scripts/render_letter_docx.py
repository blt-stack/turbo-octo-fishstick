"""
Render a single supplier letter to a .docx file.

Single-mode deliverable for the Supplier Negotiation Assistant.

Input JSON shape:
    {
      "brand_name": "...",
      "letter_type": "moq_reduction" | "pricing_tier" | "payment_terms" | "sample_request" | "dispute",
      "drafted_at": "2026-03-14",
      "supplier": {
        "company_name": "...",
        "supplier_id": "...",
        "region": "china" | "india" | "vietnam" | "north_america" | "eu",
        "country": "China",
        "primary_contact": {"name": "Cindy Chen", "honorific": "Ms.", "role": "Sales Manager"},
        "relationship_stage": "established",
        "first_contact_date": "2025-10-15",
        "orders_completed": 4,
        "total_volume_usd": 48000,
        "prior_asks": ["sample_request 2025-10-15", "moq_reduction 2025-11-08"],
        "current_moq": 1000,
        "current_unit_price_usd": 4.20,
        "current_payment_terms": "30/70 TT"
      },
      "product_context": {"product_name": "...", "summary": "..."},
      "letter": {
        "subject": "...",
        "body": "Dear Ms. Chen,\n\n..."
      },
      "why_this_works": [
        "Applied Chinese opening convention with formal honorific",
        "Bridged via reference to recent order #5118",
        "Indirect ask framing per region playbook",
        "Mutual benefit framing emphasizes long-term partnership"
      ],
      "alternate_phrasings": [
        {"section": "ask", "variants": ["Would 300 units be workable?", "We'd like to propose 300 units."]}
      ],
      "follow_up": {
        "days_to_wait": 3,
        "follow_up_date": "2026-03-21",
        "what_to_do_if_no_reply": "Send soft follow-up referencing the original letter, NA-direct style"
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


LETTER_TYPE_DISPLAY = {
    "moq_reduction": "MOQ Reduction",
    "pricing_tier": "Pricing Tier Request",
    "payment_terms": "Payment Terms",
    "sample_request": "Sample Request",
    "dispute": "Dispute Letter",
}

REGION_DISPLAY = {
    "china": "China",
    "india": "India",
    "vietnam": "Vietnam",
    "north_america": "North America (US / CA / MX)",
    "eu": "European Union",
}

STAGE_COLORS = {
    "new": RGBColor(0x1F, 0x6F, 0xB8),
    "developing": RGBColor(0x1F, 0x6F, 0xB8),
    "established": RGBColor(0x1E, 0x7A, 0x2C),
    "strained": RGBColor(0xC0, 0x55, 0x00),
    "dormant": RGBColor(0x77, 0x77, 0x77),
    "ended": RGBColor(0xC0, 0x00, 0x00),
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
    letter_type = LETTER_TYPE_DISPLAY.get(data.get("letter_type", ""), data.get("letter_type", ""))
    supplier = data.get("supplier", {})
    title_run = title_p.add_run(f"{letter_type}  →  {supplier.get('company_name', 'Supplier')}")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    drafted_at = data.get("drafted_at", "")
    region = REGION_DISPLAY.get(supplier.get("region", ""), supplier.get("region", ""))
    meta_run = meta_p.add_run(f"Drafted {drafted_at}  ·  Region playbook: {region}")
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    stage = supplier.get("relationship_stage", "new")
    stage_p = doc.add_paragraph()
    stage_run = stage_p.add_run(f"Relationship stage: {stage}")
    stage_run.bold = True
    if stage in STAGE_COLORS:
        stage_run.font.color.rgb = STAGE_COLORS[stage]

    contact = supplier.get("primary_contact", {})
    if contact.get("name"):
        contact_str = f"{contact.get('honorific', '')} {contact.get('name', '')}".strip()
        if contact.get("role"):
            contact_str = f"{contact_str}, {contact['role']}"
        _add_kv(doc, "Contact", contact_str)


def _render_supplier_memory_snapshot(doc, supplier: dict):
    if not supplier:
        return
    _add_divider(doc)
    _add_section_header(doc, "SUPPLIER MEMORY SNAPSHOT")
    if supplier.get("first_contact_date"):
        _add_kv(doc, "Known since", supplier["first_contact_date"])
    if supplier.get("orders_completed") is not None:
        _add_kv(doc, "Orders completed", str(supplier["orders_completed"]))
    if supplier.get("total_volume_usd"):
        _add_kv(doc, "Total volume to date", f"${supplier['total_volume_usd']:,}")
    prior = supplier.get("prior_asks", []) or []
    if prior:
        _add_kv(doc, "Prior asks", "; ".join(prior))
    if supplier.get("current_moq") is not None:
        _add_kv(doc, "Current MOQ on file", str(supplier["current_moq"]))
    if supplier.get("current_unit_price_usd") is not None:
        _add_kv(doc, "Current unit price", f"${supplier['current_unit_price_usd']:.2f}")
    if supplier.get("current_payment_terms"):
        _add_kv(doc, "Payment terms in force", supplier["current_payment_terms"])


def _render_product_context(doc, ctx: dict):
    if not ctx:
        return
    _add_divider(doc)
    _add_section_header(doc, "PRODUCT CONTEXT")
    if ctx.get("product_name"):
        _add_kv(doc, "Product", ctx["product_name"])
    if ctx.get("summary"):
        for paragraph in (ctx["summary"] or "").split("\n\n"):
            doc.add_paragraph(paragraph)


def _render_letter(doc, letter: dict):
    if not letter:
        return
    _add_divider(doc)
    _add_section_header(doc, "DRAFTED LETTER")
    if letter.get("subject"):
        _add_kv(doc, "Subject", letter["subject"])
    body = letter.get("body", "")
    if body:
        _add_subheader(doc, "Body")
        for paragraph in body.split("\n\n"):
            doc.add_paragraph(paragraph)


def _render_why_this_works(doc, items: list[str]):
    if not items:
        return
    _add_divider(doc)
    _add_section_header(doc, "WHY THIS LETTER WORKS")
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def _render_alternates(doc, alternates: list[dict]):
    if not alternates:
        return
    _add_divider(doc)
    _add_section_header(doc, "ALTERNATE PHRASINGS")
    for entry in alternates:
        section = entry.get("section", "")
        if section:
            _add_subheader(doc, f"Section: {section}")
        for variant in entry.get("variants", []):
            doc.add_paragraph(variant, style="List Bullet")


def _render_followup(doc, follow_up: dict):
    if not follow_up:
        return
    _add_divider(doc)
    _add_section_header(doc, "SUGGESTED FOLLOW-UP TIMING")
    if follow_up.get("days_to_wait"):
        _add_kv(doc, "Wait", f"{follow_up['days_to_wait']} day(s) before nudging")
    if follow_up.get("follow_up_date"):
        _add_kv(doc, "Follow-up date", follow_up["follow_up_date"])
    if follow_up.get("what_to_do_if_no_reply"):
        _add_kv(doc, "If no reply", follow_up["what_to_do_if_no_reply"])


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_header(doc, data)
    _render_supplier_memory_snapshot(doc, data.get("supplier", {}))
    _render_product_context(doc, data.get("product_context", {}))
    _render_letter(doc, data.get("letter", {}))
    _render_why_this_works(doc, data.get("why_this_works", []))
    _render_alternates(doc, data.get("alternate_phrasings", []))
    _render_followup(doc, data.get("follow_up", {}))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_letter_docx.py <letter_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
