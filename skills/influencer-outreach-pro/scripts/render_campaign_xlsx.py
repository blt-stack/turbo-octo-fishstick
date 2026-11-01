"""
Render a bulk influencer campaign to a 5-sheet .xlsx workbook.

Sheets:
  1. Outreach Queue           — one row per creator
  2. Campaign Summary         — tier counts, budget, projected reach
  3. Disclosure Compliance    — per-creator disclosure requirements
  4. Follow-up Calendar       — chronological follow-up dates
  5. Influencer Memory Updates — per-creator cache writes

Input JSON shape:
    {
      "brand_name": "...",
      "campaign_name": "...",
      "generated_at": "2026-05-22",
      "creators": [
        {
          "handle": "@maya_brews",
          "platform": "instagram",
          "tier": "micro",
          "follower_count": 24000,
          "niche": "coffee + slow living",
          "content_themes_extracted": ["coffee_brewing", "slow_mornings"],
          "pitch_product_or_bundle": "The Slow Morning Bundle",
          "framework": "hybrid",
          "rate_offered_usd": 400,
          "product_value_usd": 92,
          "outreach_body": "Hi Maya — your post about ...",
          "outreach_subject": "",
          "expected_reply_by": "2026-05-29",
          "follow_up_a_date": "2026-05-29",
          "follow_up_b_date": "2026-06-12",
          "follow_up_c_date": "2026-06-26",
          "disclosure_required": "Branded Content tag + #ad",
          "memory_updates": ["Logged initial outreach", "Stage: new -> outreached"]
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
    "nano": "Nano",
    "micro": "Micro",
    "mid_tier": "Mid-tier",
    "macro": "Macro",
}

PLATFORM_DISPLAY = {
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "youtube": "YouTube",
    "x_twitter": "X / Twitter",
    "linkedin": "LinkedIn",
    "pinterest": "Pinterest",
}

TIER_FILLS = {
    "nano": PatternFill("solid", fgColor="E2F0D9"),
    "micro": PatternFill("solid", fgColor="C6EFCE"),
    "mid_tier": PatternFill("solid", fgColor="FFEB9C"),
    "macro": PatternFill("solid", fgColor="FFC7CE"),
}

STATUS_FILLS = {
    "Drafted": PatternFill("solid", fgColor="FFEB9C"),
    "Sent": PatternFill("solid", fgColor="D9E1F2"),
    "Responded": PatternFill("solid", fgColor="C6EFCE"),
    "Negotiating": PatternFill("solid", fgColor="BDD7EE"),
    "Agreed": PatternFill("solid", fgColor="C6E0B4"),
    "Declined": PatternFill("solid", fgColor="FFC7CE"),
    "Posted": PatternFill("solid", fgColor="A9D08E"),
}

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")


def _write_outreach_queue(ws, creators: list[dict]):
    headers = [
        "Handle", "Platform", "Tier", "Followers",
        "Niche", "Content Themes",
        "Pitch", "Framework", "Rate (USD)", "Product Value (USD)",
        "Subject", "Outreach Body",
        "Expected Reply By", "Status",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for c in creators:
        row = [
            c.get("handle", ""),
            PLATFORM_DISPLAY.get(c.get("platform", ""), c.get("platform", "")),
            TIER_DISPLAY.get(c.get("tier", ""), c.get("tier", "")),
            c.get("follower_count", ""),
            c.get("niche", ""),
            ", ".join(c.get("content_themes_extracted", [])),
            c.get("pitch_product_or_bundle", ""),
            c.get("framework", ""),
            c.get("rate_offered_usd", ""),
            c.get("product_value_usd", ""),
            c.get("outreach_subject", ""),
            c.get("outreach_body", ""),
            c.get("expected_reply_by", ""),
            "Drafted",
        ]
        ws.append(row)
        row_idx = ws.max_row
        tier = c.get("tier", "")
        if tier in TIER_FILLS:
            ws.cell(row=row_idx, column=3).fill = TIER_FILLS[tier]
        ws.cell(row=row_idx, column=14).fill = STATUS_FILLS["Drafted"]

    widths = [22, 14, 12, 12, 24, 28, 24, 14, 12, 14, 28, 70, 16, 14]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions


def _write_campaign_summary(ws, creators: list[dict]):
    ws.append(["Metric", "Value"])
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    ws.append(["Total creators", len(creators)])

    tier_counts = Counter(c.get("tier", "") for c in creators)
    ws.append([])
    ws.append(["Tier distribution", ""])
    for tier in ("nano", "micro", "mid_tier", "macro"):
        ws.append([f"  {TIER_DISPLAY.get(tier, tier)}", tier_counts.get(tier, 0)])

    platform_counts = Counter(c.get("platform", "") for c in creators)
    ws.append([])
    ws.append(["Platform distribution", ""])
    for plat, count in platform_counts.most_common():
        if plat:
            ws.append([f"  {PLATFORM_DISPLAY.get(plat, plat)}", count])

    framework_counts = Counter(c.get("framework", "") for c in creators)
    ws.append([])
    ws.append(["Framework distribution", ""])
    for fw, count in framework_counts.most_common():
        if fw:
            ws.append([f"  {fw}", count])

    total_cash = sum(c.get("rate_offered_usd", 0) or 0 for c in creators)
    total_product = sum(c.get("product_value_usd", 0) or 0 for c in creators)
    ws.append([])
    ws.append(["Budget exposure (if all convert)", ""])
    ws.append([f"  Total cash committed", f"${total_cash:,.2f}"])
    ws.append([f"  Total product value", f"${total_product:,.2f}"])
    ws.append([f"  Total exposure", f"${total_cash + total_product:,.2f}"])

    total_followers = sum(c.get("follower_count", 0) or 0 for c in creators)
    estimated_reach = int(total_followers * 0.15)  # rough estimate
    ws.append([])
    ws.append(["Projected reach (if all convert + 15% engagement)", f"~{estimated_reach:,} impressions"])
    ws.append(["Total combined follower base", f"{total_followers:,}"])

    widths = [44, 22]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def _write_disclosure_compliance(ws, creators: list[dict]):
    headers = ["Handle", "Platform", "Framework", "Required Disclosure", "Brand Monitoring"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for c in creators:
        framework = c.get("framework", "")
        platform = PLATFORM_DISPLAY.get(c.get("platform", ""), c.get("platform", ""))
        disclosure = c.get("disclosure_required", "—")
        monitoring = "Review live posts within 48h of publication"
        ws.append([c.get("handle", ""), platform, framework, disclosure, monitoring])

    widths = [22, 14, 14, 50, 36]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"


def _write_follow_up_calendar(ws, creators: list[dict]):
    headers = ["Date", "Handle", "Variant", "Outreach Type", "Action"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    rows = []
    for c in creators:
        handle = c.get("handle", "")
        if c.get("follow_up_a_date"):
            rows.append([c["follow_up_a_date"], handle, "A", "Soft nudge", "Send Variant A"])
        if c.get("follow_up_b_date"):
            rows.append([c["follow_up_b_date"], handle, "B", "Reframed offer", "Send Variant B"])
        if c.get("follow_up_c_date"):
            rows.append([c["follow_up_c_date"], handle, "C", "Final ask", "Send Variant C"])

    rows.sort(key=lambda r: r[0] or "9999-12-31")
    for r in rows:
        ws.append(r)

    if not rows:
        ws.append(["(No follow-up dates scheduled)", "", "", "", ""])

    widths = [14, 22, 10, 22, 24]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"


def _write_memory_updates(ws, creators: list[dict]):
    headers = ["Handle", "Memory Cache Updates"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for c in creators:
        updates = c.get("memory_updates", []) or []
        ws.append([c.get("handle", ""), "\n".join(f"• {u}" for u in updates)])

    widths = [22, 80]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"


def render(data: dict, output_path: Path) -> Path:
    creators = data.get("creators", []) or []

    wb = Workbook()
    ws_queue = wb.active
    ws_queue.title = "Outreach Queue"
    _write_outreach_queue(ws_queue, creators)

    ws_summary = wb.create_sheet("Campaign Summary")
    _write_campaign_summary(ws_summary, creators)

    ws_compliance = wb.create_sheet("Disclosure Compliance")
    _write_disclosure_compliance(ws_compliance, creators)

    ws_calendar = wb.create_sheet("Follow-up Calendar")
    _write_follow_up_calendar(ws_calendar, creators)

    ws_memory = wb.create_sheet("Influencer Memory Updates")
    _write_memory_updates(ws_memory, creators)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_campaign_xlsx.py <campaign_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
