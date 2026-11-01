"""
Render a single CS ticket reply to a .docx file.

The .docx is the buyer-facing deliverable for single mode. Contains:
- Ticket header (customer info, category, sentiment, order context)
- The drafted reply (subject + body, paste-ready)
- The recommended action + rationale + estimated cost
- The original ticket for reference

Input JSON shape:
    {
      "customer_name": "...",
      "customer_email": "...",
      "received_at": "2026-05-22",
      "category": "shipping_issues",
      "sub_type": "delayed",
      "sentiment": "neutral" | "angry" | "friendly",
      "sentiment_reasoning": "...",
      "order_context": {
        "order_id": "#1024",
        "order_date": "2026-05-10",
        "ship_date": "2026-05-12",
        "fulfillment_status": "in_transit",
        "tracking_carrier": "UPS",
        "tracking_number": "1Z...",
        "last_known_location": "Memphis, TN",
        "products": [{"name": "...", "qty": 1, "price": 48.00}],
        "order_total": 52.00,
        "customer_ltv": 340.00,
        "customer_order_count": 4
      },
      "reply": {
        "subject": "Re: Where is my order #1024",
        "body": "Hi [name],\n\n...\n\n— [Founder]"
      },
      "action": {
        "code": "refund_partial_plus_credit",
        "label": "Issue partial refund + $10 store credit",
        "rationale": "Order delayed 6 days past estimate due to UPS facility backup. Partial refund of $10 + matching store credit acknowledges the wait without giving away the full order.",
        "estimated_cost": "$10 refund + $10 credit = ~$15 (credit may not be used)"
      },
      "original_ticket": "Customer's original message text..."
    }

Requires python-docx (pip install python-docx --break-system-packages).
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor


CATEGORY_DISPLAY = {
    "shipping_issues": "Shipping Issue",
    "returns_refunds": "Returns / Refunds / Exchanges",
    "defects_damages": "Defects / Damages",
    "pre_purchase_questions": "Pre-purchase Question",
}

SENTIMENT_COLORS = {
    "angry": RGBColor(0xC0, 0x00, 0x00),
    "neutral": RGBColor(0x55, 0x55, 0x55),
    "friendly": RGBColor(0x1E, 0x7A, 0x2C),
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
    cust_name = data.get("customer_name", "Unknown Customer")
    title_run = title_p.add_run(f"Reply to: {cust_name}")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    category = CATEGORY_DISPLAY.get(data.get("category", ""), data.get("category", ""))
    sub_type = data.get("sub_type", "")
    received_at = data.get("received_at", "")
    meta_run = meta_p.add_run(
        f"Received {received_at}  ·  Category: {category}"
        + (f" — {sub_type}" if sub_type else "")
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    sentiment = data.get("sentiment", "neutral")
    sent_p = doc.add_paragraph()
    sent_run = sent_p.add_run(f"Sentiment: {sentiment}")
    sent_run.bold = True
    if sentiment in SENTIMENT_COLORS:
        sent_run.font.color.rgb = SENTIMENT_COLORS[sentiment]

    reasoning = data.get("sentiment_reasoning", "")
    if reasoning:
        p = doc.add_paragraph()
        p.add_run("Reasoning: ").italic = True
        run = p.add_run(reasoning)
        run.italic = True
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def _render_order_context(doc, ctx: dict):
    if not ctx:
        return
    _add_divider(doc)
    _add_section_header(doc, "ORDER CONTEXT")
    if ctx.get("order_id"):
        _add_kv(doc, "Order", ctx["order_id"])
    if ctx.get("order_date"):
        _add_kv(doc, "Placed", ctx["order_date"])
    if ctx.get("ship_date"):
        _add_kv(doc, "Shipped", ctx["ship_date"])
    if ctx.get("fulfillment_status"):
        _add_kv(doc, "Status", ctx["fulfillment_status"])
    if ctx.get("tracking_carrier") and ctx.get("tracking_number"):
        _add_kv(doc, "Tracking", f"{ctx['tracking_carrier']} {ctx['tracking_number']}")
    if ctx.get("last_known_location"):
        _add_kv(doc, "Last known location", ctx["last_known_location"])
    products = ctx.get("products", []) or []
    if products:
        _add_subheader(doc, "Products in order")
        for p in products:
            doc.add_paragraph(
                f"{p.get('qty', 1)} × {p.get('name', '')} — ${p.get('price', 0):.2f}",
                style="List Bullet",
            )
    if ctx.get("order_total") is not None:
        _add_kv(doc, "Order total", f"${ctx['order_total']:.2f}")
    if ctx.get("customer_ltv") is not None:
        _add_kv(
            doc,
            "Customer LTV",
            f"${ctx['customer_ltv']:.2f} across {ctx.get('customer_order_count', 1)} orders",
        )


def _render_reply(doc, reply: dict):
    _add_divider(doc)
    _add_section_header(doc, "DRAFTED REPLY")
    if reply.get("subject"):
        _add_kv(doc, "Subject", reply["subject"])
    body = reply.get("body", "")
    if body:
        _add_subheader(doc, "Body")
        for paragraph in body.split("\n\n"):
            doc.add_paragraph(paragraph)


def _render_action(doc, action: dict):
    if not action:
        return
    _add_divider(doc)
    _add_section_header(doc, "RECOMMENDED ACTION")
    _add_kv(doc, "Action", action.get("label", action.get("code", "—")))
    _add_kv(doc, "Rationale", action.get("rationale", "—"))
    if action.get("estimated_cost"):
        _add_kv(doc, "Estimated cost", action["estimated_cost"])


def _render_original_ticket(doc, ticket_text: str):
    if not ticket_text:
        return
    _add_divider(doc)
    _add_section_header(doc, "ORIGINAL TICKET (for reference)")
    for paragraph in ticket_text.split("\n\n"):
        p = doc.add_paragraph(paragraph)
        for run in p.runs:
            run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_header(doc, data)
    _render_order_context(doc, data.get("order_context", {}))
    _render_reply(doc, data.get("reply", {}))
    _render_action(doc, data.get("action", {}))
    _render_original_ticket(doc, data.get("original_ticket", ""))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_reply_docx.py <reply_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
