"""
Render a batch of CS tickets + drafted replies to a 3-sheet .xlsx workbook.

Sheets:
  1. Reply Queue          — one row per ticket with reply + action + status column
  2. Category Breakdown   — aggregate counts per category + sentiment + action + cost
  3. Systemic Issues      — auto-detected patterns worth investigating

Input JSON shape:
    {
      "brand_name": "...",
      "generated_at": "2026-05-22",
      "tickets": [
        {  # one per ticket
          "ticket_id": "auto or external",
          "received_at": "2026-05-22 09:14",
          "customer_name": "...",
          "customer_email": "...",
          "category": "shipping_issues",
          "sub_type": "delayed",
          "sentiment": "neutral",
          "original_ticket": "...",
          "order_id": "...",
          "reply": {"subject": "...", "body": "..."},
          "action": {"code": "...", "label": "...", "rationale": "...", "estimated_cost_value": 15.00, "estimated_cost_label": "$10 refund + $10 credit = ~$15"}
        },
        ...
      ],
      "systemic_issues": [
        {
          "pattern": "Shipping delay — UPS Memphis facility",
          "ticket_count": 5,
          "first_seen": "2026-05-15",
          "recommendation": "Switch fulfillment to a non-UPS carrier for orders shipping from this region"
        },
        ...
      ]
    }

Requires openpyxl (pip install openpyxl --break-system-packages).
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


CATEGORY_DISPLAY = {
    "shipping_issues": "Shipping",
    "returns_refunds": "Returns/Refunds",
    "defects_damages": "Defects/Damages",
    "pre_purchase_questions": "Pre-purchase",
}

SENTIMENT_COLORS = {
    "angry": PatternFill("solid", fgColor="FFC7CE"),
    "neutral": PatternFill("solid", fgColor="FFFFFF"),
    "friendly": PatternFill("solid", fgColor="C6EFCE"),
}

STATUS_COLORS = {
    "Pending review": PatternFill("solid", fgColor="FFEB9C"),
    "Approved": PatternFill("solid", fgColor="D9E1F2"),
    "Sent": PatternFill("solid", fgColor="C6E0B4"),
    "Held": PatternFill("solid", fgColor="F7CAAC"),
    "Escalated": PatternFill("solid", fgColor="FFC7CE"),
}

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")


def _write_reply_queue(ws, tickets: list[dict]):
    headers = [
        "Received",
        "Customer",
        "Email",
        "Category",
        "Sub-type",
        "Sentiment",
        "Original Ticket",
        "Drafted Reply Subject",
        "Drafted Reply Body",
        "Recommended Action",
        "Rationale",
        "Est. Cost",
        "Status",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for ticket in tickets:
        reply = ticket.get("reply", {}) or {}
        action = ticket.get("action", {}) or {}
        row = [
            ticket.get("received_at", ""),
            ticket.get("customer_name", ""),
            ticket.get("customer_email", ""),
            CATEGORY_DISPLAY.get(ticket.get("category", ""), ticket.get("category", "")),
            ticket.get("sub_type", ""),
            ticket.get("sentiment", "neutral"),
            ticket.get("original_ticket", ""),
            reply.get("subject", ""),
            reply.get("body", ""),
            action.get("label", action.get("code", "")),
            action.get("rationale", ""),
            action.get("estimated_cost_label", ""),
            "Pending review",
        ]
        ws.append(row)
        # Color the sentiment cell
        sent_cell = ws.cell(row=ws.max_row, column=6)
        sentiment = ticket.get("sentiment", "neutral")
        if sentiment in SENTIMENT_COLORS:
            sent_cell.fill = SENTIMENT_COLORS[sentiment]
        # Color the status cell
        status_cell = ws.cell(row=ws.max_row, column=13)
        status_cell.fill = STATUS_COLORS["Pending review"]

    widths = [16, 18, 22, 14, 18, 10, 50, 30, 60, 26, 40, 18, 14]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions


def _write_category_breakdown(ws, tickets: list[dict]):
    headers = ["Metric", "Value"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    ws.append(["Total tickets in batch", len(tickets)])

    # Category counts
    cat_counts = Counter(CATEGORY_DISPLAY.get(t.get("category", ""), t.get("category", "")) for t in tickets)
    ws.append([])
    ws.append(["Tickets per category", ""])
    for cat, count in cat_counts.most_common():
        ws.append([f"  {cat}", count])

    # Sentiment distribution
    sent_counts = Counter(t.get("sentiment", "neutral") for t in tickets)
    ws.append([])
    ws.append(["Sentiment distribution", ""])
    for sent in ("angry", "neutral", "friendly"):
        ws.append([f"  {sent}", sent_counts.get(sent, 0)])

    # Action frequencies
    action_counts = Counter((t.get("action", {}) or {}).get("code", "") for t in tickets)
    ws.append([])
    ws.append(["Recommended actions", ""])
    for code, count in action_counts.most_common():
        if code:
            ws.append([f"  {code}", count])

    # Cost summary
    total_cost = 0.0
    for t in tickets:
        action = t.get("action", {}) or {}
        cost = action.get("estimated_cost_value", 0)
        if isinstance(cost, (int, float)):
            total_cost += cost
    ws.append([])
    ws.append(["Total estimated cost across batch", f"${total_cost:.2f}"])

    widths = [40, 14]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def _write_systemic_issues(ws, issues: list[dict]):
    headers = ["Pattern", "Ticket Count", "First Seen", "Recommendation"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for issue in issues:
        ws.append([
            issue.get("pattern", ""),
            issue.get("ticket_count", ""),
            issue.get("first_seen", ""),
            issue.get("recommendation", ""),
        ])

    if not issues:
        ws.append(["(No systemic issues detected in this batch.)", "", "", ""])

    widths = [40, 12, 14, 60]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"


def render(data: dict, output_path: Path) -> Path:
    tickets = data.get("tickets", []) or []
    systemic_issues = data.get("systemic_issues", []) or []

    wb = Workbook()
    ws_queue = wb.active
    ws_queue.title = "Reply Queue"
    _write_reply_queue(ws_queue, tickets)

    ws_breakdown = wb.create_sheet("Category Breakdown")
    _write_category_breakdown(ws_breakdown, tickets)

    ws_systemic = wb.create_sheet("Systemic Issues")
    _write_systemic_issues(ws_systemic, systemic_issues)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_replies_xlsx.py <batch_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
