"""
Render a comparison-bulk RFQ workbook with 4 sheets:

  1. Outreach Queue        — one row per supplier with tailored letter draft + status
  2. Quote Comparison      — auto-populates as buyer fills Reply columns; ranks by landed cost
  3. Supplier Memory Updates — what was written to each supplier's memory file
  4. Negotiation Tactics    — quick-reference card for evaluating quotes + countering

Input JSON shape:
    {
      "brand_name": "...",
      "rfq_name": "RS-Pour-Over-2026-Q2",
      "generated_at": "2026-03-14",
      "target_quantity": 1500,
      "target_lead_time_days": 60,
      "target_destination": "Brooklyn, NY, USA",
      "shipping_terms_expected": "FOB",
      "rfq_brief": "Full RFQ brief text...",
      "suppliers": [
        {
          "supplier_id": "shenzhen-stoneworks",
          "company_name": "Shenzhen Stoneworks Co., Ltd.",
          "region": "china",
          "country": "China",
          "primary_contact": "Cindy Chen",
          "contact_email": "cindy@...",
          "channel": "email",
          "relationship_stage": "established",
          "send_time_local": "2026-03-14 10:00 (Asia/Shanghai)",
          "follow_up_date": "2026-03-19",
          "letter": {"subject": "...", "body": "Dear Ms. Chen,\n\n..."},
          "memory_updates": ["Logged letter sent; pending response expected by 2026-03-19"]
        },
        ...
      ],
      "tactics_reference": {
        "red_flags": [...],
        "counter_negotiation_guidance": [...],
        "soft_tells": [...]
      }
    }

Requires openpyxl (pip install openpyxl --break-system-packages).
"""

import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


REGION_DISPLAY = {
    "china": "China",
    "india": "India",
    "vietnam": "Vietnam",
    "north_america": "North America",
    "eu": "European Union",
}

STAGE_FILLS = {
    "new": PatternFill("solid", fgColor="D9E1F2"),
    "developing": PatternFill("solid", fgColor="D9E1F2"),
    "established": PatternFill("solid", fgColor="C6EFCE"),
    "strained": PatternFill("solid", fgColor="FFC7CE"),
    "dormant": PatternFill("solid", fgColor="D9D9D9"),
    "ended": PatternFill("solid", fgColor="FFC7CE"),
}

STATUS_FILLS = {
    "Drafted": PatternFill("solid", fgColor="FFEB9C"),
    "Sent": PatternFill("solid", fgColor="D9E1F2"),
    "Replied": PatternFill("solid", fgColor="C6EFCE"),
    "No-reply": PatternFill("solid", fgColor="FFC7CE"),
    "Awarded": PatternFill("solid", fgColor="C6E0B4"),
    "Declined": PatternFill("solid", fgColor="F7CAAC"),
}

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")


def _write_outreach_queue(ws, suppliers: list[dict]):
    headers = [
        "Supplier",
        "Region",
        "Country",
        "Contact",
        "Channel",
        "Stage",
        "Send (local time)",
        "Follow-up Date",
        "Subject",
        "Letter Body",
        "Quote Response",
        "Quote Date Received",
        "Status",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for s in suppliers:
        letter = s.get("letter", {}) or {}
        row = [
            s.get("company_name", ""),
            REGION_DISPLAY.get(s.get("region", ""), s.get("region", "")),
            s.get("country", ""),
            s.get("primary_contact", ""),
            s.get("channel", ""),
            s.get("relationship_stage", ""),
            s.get("send_time_local", ""),
            s.get("follow_up_date", ""),
            letter.get("subject", ""),
            letter.get("body", ""),
            "",  # Quote Response — buyer fills in
            "",  # Quote Date Received
            "Drafted",
        ]
        ws.append(row)
        row_idx = ws.max_row
        stage = s.get("relationship_stage", "new")
        if stage in STAGE_FILLS:
            ws.cell(row=row_idx, column=6).fill = STAGE_FILLS[stage]
        ws.cell(row=row_idx, column=13).fill = STATUS_FILLS["Drafted"]

    widths = [26, 14, 14, 22, 12, 14, 22, 14, 30, 70, 50, 18, 12]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions


def _write_quote_comparison(ws, suppliers: list[dict], target_quantity: int):
    headers = [
        "Supplier",
        "Region",
        "MOQ Offered",
        "Unit Price (USD)",
        "Quoted Qty",
        "Total at Qty",
        "Lead Time (days)",
        "Payment Terms Offered",
        "Shipping Terms",
        "Sample Cost (USD)",
        "Sample Availability",
        "Quote Validity",
        "Shipping Estimate",
        "Duties Estimate",
        "Total Landed Cost",
        "Per-Unit Landed Cost",
        "Rank by Landed Cost",
        "Notes",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    # Pre-populate one row per supplier with the supplier name; the rest left blank for buyer to fill in
    for s in suppliers:
        ws.append([
            s.get("company_name", ""),
            REGION_DISPLAY.get(s.get("region", ""), s.get("region", "")),
            "",  # MOQ offered
            "",  # Unit price
            target_quantity,  # Quoted qty (default to target)
            "",  # Total at qty (formula filled in once price is in)
            "",  # Lead time
            "",  # Payment terms offered
            "",  # Shipping terms
            "",  # Sample cost
            "",  # Sample availability
            "",  # Quote validity
            "",  # Shipping estimate
            "",  # Duties estimate
            "",  # Total landed cost
            "",  # Per-unit landed cost
            "",  # Rank
            "",  # Notes
        ])

    # Add formulas in rows for total at qty + per-unit landed cost (once user fills in price + estimates)
    for row_idx in range(2, len(suppliers) + 2):
        ws.cell(row=row_idx, column=6).value = f"=IF(AND(D{row_idx}<>\"\",E{row_idx}<>\"\"),D{row_idx}*E{row_idx},\"\")"
        ws.cell(row=row_idx, column=15).value = f"=IF(AND(F{row_idx}<>\"\",M{row_idx}<>\"\",N{row_idx}<>\"\"),F{row_idx}+M{row_idx}+N{row_idx},\"\")"
        ws.cell(row=row_idx, column=16).value = f"=IF(AND(O{row_idx}<>\"\",E{row_idx}<>\"\"),O{row_idx}/E{row_idx},\"\")"

    widths = [26, 14, 12, 14, 12, 14, 14, 24, 14, 14, 22, 14, 14, 14, 16, 16, 12, 30]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"


def _write_memory_updates(ws, suppliers: list[dict]):
    headers = ["Supplier", "Updates"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for s in suppliers:
        updates = s.get("memory_updates", []) or []
        ws.append([s.get("company_name", ""), "\n".join(f"• {u}" for u in updates)])

    widths = [30, 80]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"


def _write_tactics_reference(ws, tactics: dict):
    ws.append(["Section", "Item"])
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    sections = [
        ("RED FLAGS in incoming quotes", tactics.get("red_flags", []) or []),
        ("COUNTER-NEGOTIATION guidance", tactics.get("counter_negotiation_guidance", []) or []),
        ("SOFT TELLS in supplier replies", tactics.get("soft_tells", []) or []),
        ("DECLINE letter pattern", tactics.get("decline_letter_pattern", []) or []),
    ]

    for section_title, items in sections:
        ws.append([section_title, ""])
        for item in items:
            ws.append(["", f"• {item}"])
        ws.append([])

    if not any(t for _, t in sections):
        ws.append(["(No tactics reference items provided.)", ""])

    widths = [32, 90]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"


def render(data: dict, output_path: Path) -> Path:
    suppliers = data.get("suppliers", []) or []
    target_quantity = data.get("target_quantity", 0)

    wb = Workbook()
    ws_outreach = wb.active
    ws_outreach.title = "Outreach Queue"
    _write_outreach_queue(ws_outreach, suppliers)

    ws_compare = wb.create_sheet("Quote Comparison")
    _write_quote_comparison(ws_compare, suppliers, target_quantity)

    ws_memory = wb.create_sheet("Supplier Memory Updates")
    _write_memory_updates(ws_memory, suppliers)

    ws_tactics = wb.create_sheet("Negotiation Tactics")
    _write_tactics_reference(ws_tactics, data.get("tactics_reference", {}))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_rfq_comparison_xlsx.py <rfq_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
