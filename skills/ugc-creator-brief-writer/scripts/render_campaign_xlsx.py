"""
Render the campaign-mode workbook to a multi-sheet .xlsx file.

Three sheets:
  1. Creator Roster   — one row per creator with assignments, deadlines, status.
  2. Hook Library     — all hooks generated, with assignment tracking.
  3. Campaign Calendar — chronological view of campaign milestones.

Input JSON shape:
    {
      "campaign_name": "...",
      "brand_name": "...",
      "generated_at": "2026-05-22",
      "creators": [
        {
          "handle": "@amyhouse",
          "real_name": "Amy Houseman",
          "platform": "tiktok",
          "assigned_hook_numbers": [1, 4],
          "assigned_archetypes": ["Problem-aware", "Curiosity gap"],
          "shoot_deadline": "2026-05-26",
          "delivery_deadline": "2026-05-28",
          "payment_terms": "$400 + 3mo Spark usage",
          "usage_rights_duration": "3 months Spark",
          "status": "Pending",
          "notes": "Prefers minimalist aesthetic"
        },
        ...
      ],
      "hooks": [
        {
          "number": 1,
          "archetype": "Problem-aware",
          "spoken_line": "...",
          "on_screen_text": "...",
          "assigned_to": ["@amyhouse"]
        },
        ...
      ],
      "calendar": [
        {"date": "2026-05-22", "creator": "All", "milestone": "Briefs sent"},
        ...
      ]
    }

Requires openpyxl (pip install openpyxl --break-system-packages).
"""

import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


PLATFORM_DISPLAY = {
    "tiktok": "TikTok",
    "reels": "Instagram Reels",
    "stories": "Instagram Stories",
    "shorts": "YouTube Shorts",
}

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")

STATUS_COLORS = {
    "pending": PatternFill("solid", fgColor="FFEB9C"),
    "briefed": PatternFill("solid", fgColor="D9E1F2"),
    "shooting": PatternFill("solid", fgColor="BDD7EE"),
    "delivered": PatternFill("solid", fgColor="C6E0B4"),
    "approved": PatternFill("solid", fgColor="A9D08E"),
    "published": PatternFill("solid", fgColor="70AD47"),
    "paid": PatternFill("solid", fgColor="548235"),
}


def _write_creator_roster(ws, creators: list[dict], hooks: list[dict]):
    headers = [
        "Creator handle",
        "Real name",
        "Platform",
        "Assigned hooks",
        "Assigned archetypes",
        "Shoot deadline",
        "Delivery deadline",
        "Payment terms",
        "Usage rights duration",
        "Status",
        "Notes",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    # Build a lookup so we can write hook descriptions inline with the number
    hooks_by_num = {h.get("number"): h for h in hooks or []}

    for creator in creators:
        assigned_nums = creator.get("assigned_hook_numbers", []) or []
        assigned_hook_descriptions = []
        for n in assigned_nums:
            h = hooks_by_num.get(n)
            if h:
                line = h.get("spoken_line", "")
                short = line[:60] + ("..." if len(line) > 60 else "")
                assigned_hook_descriptions.append(f"#{n}: {short}")
            else:
                assigned_hook_descriptions.append(f"#{n}")
        platform_display = PLATFORM_DISPLAY.get(creator.get("platform", ""), creator.get("platform", ""))
        row = [
            creator.get("handle", ""),
            creator.get("real_name", ""),
            platform_display,
            "\n".join(assigned_hook_descriptions),
            ", ".join(creator.get("assigned_archetypes", []) or []),
            creator.get("shoot_deadline", ""),
            creator.get("delivery_deadline", ""),
            creator.get("payment_terms", ""),
            creator.get("usage_rights_duration", ""),
            creator.get("status", "Pending"),
            creator.get("notes", ""),
        ]
        ws.append(row)
        # Color the status cell
        status_cell = ws.cell(row=ws.max_row, column=10)
        status_lower = (creator.get("status", "pending") or "pending").lower()
        if status_lower in STATUS_COLORS:
            status_cell.fill = STATUS_COLORS[status_lower]

    widths = [18, 18, 14, 38, 24, 14, 14, 22, 22, 14, 30]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"


def _write_hook_library(ws, hooks: list[dict]):
    headers = [
        "Hook #",
        "Archetype",
        "Spoken line",
        "On-screen text",
        "Assigned to",
        "Status",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for hook in hooks:
        assigned = hook.get("assigned_to", []) or []
        status = "Assigned" if assigned else "Unassigned"
        row = [
            hook.get("number", ""),
            hook.get("archetype", ""),
            hook.get("spoken_line", ""),
            hook.get("on_screen_text", ""),
            ", ".join(assigned),
            status,
        ]
        ws.append(row)
        if status == "Unassigned":
            ws.cell(row=ws.max_row, column=6).fill = STATUS_COLORS["pending"]

    widths = [8, 18, 60, 38, 24, 12]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"


def _write_calendar(ws, calendar: list[dict]):
    headers = ["Date", "Creator", "Milestone"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    # Sort by date
    sorted_events = sorted(calendar or [], key=lambda e: str(e.get("date", "")))
    for event in sorted_events:
        ws.append([
            event.get("date", ""),
            event.get("creator", ""),
            event.get("milestone", ""),
        ])

    widths = [14, 22, 50]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"


def render(data: dict, output_path: Path) -> Path:
    wb = Workbook()

    ws_roster = wb.active
    ws_roster.title = "Creator Roster"
    _write_creator_roster(ws_roster, data.get("creators", []) or [], data.get("hooks", []) or [])

    ws_hooks = wb.create_sheet("Hook Library")
    _write_hook_library(ws_hooks, data.get("hooks", []) or [])

    ws_calendar = wb.create_sheet("Campaign Calendar")
    _write_calendar(ws_calendar, data.get("calendar", []) or [])

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
