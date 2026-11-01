"""
Render the campaign calendar to a 3-sheet .xlsx workbook.

Sheets:
  1. Calendar (chronological)  — one row per scheduled send, sorted by date
  2. Campaigns (campaign view)  — one row per campaign with aggregate send counts
  3. Monthly view (matrix)      — one row per day, channels as columns

Input JSON shape:
    {
      "brand_name": "...",
      "region": "us" | "uk-eu" | "canada-au-nz" | "global",
      "calendar_window": {"start": "2026-05-22", "end": "2026-08-20"},
      "generated_at": "2026-05-22",
      "campaigns": [
        {
          "campaign_name": "Mother's Day 2026",
          "campaign_type": "Holiday",
          "start_date": "2026-04-22",
          "end_date": "2026-05-12",
          "sends": [
            {
              "date": "2026-04-22",
              "time": "10:00",
              "timezone": "America/Los_Angeles",
              "channel": "email",
              "topic": "Pre-launch tease for Mother's Day collection",
              "status": "Planned",
              "owner": ""
            },
            ...
          ]
        },
        ...
      ]
    }

Requires openpyxl (pip install openpyxl --break-system-packages).
"""

import json
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


CHANNEL_DISPLAY = {
    "email": "Email",
    "sms": "SMS",
    "paid_ad": "Paid Ad",
    "organic_social": "Organic Social",
    "site_update": "Site Update",
}

CHANNEL_ORDER = ["email", "sms", "paid_ad", "organic_social", "site_update"]

CAMPAIGN_TYPE_COLORS = {
    "Holiday": PatternFill("solid", fgColor="FFEB9C"),
    "Product Launch": PatternFill("solid", fgColor="BDD7EE"),
    "Restock": PatternFill("solid", fgColor="C6E0B4"),
    "Flash Sale": PatternFill("solid", fgColor="FFC7CE"),
    "Brand Event": PatternFill("solid", fgColor="E2D8F3"),
    "Other": PatternFill("solid", fgColor="F2F2F2"),
}

STATUS_COLORS = {
    "Planned": PatternFill("solid", fgColor="FFFFFF"),
    "Drafted": PatternFill("solid", fgColor="D9E1F2"),
    "Scheduled": PatternFill("solid", fgColor="C6E0B4"),
    "Sent": PatternFill("solid", fgColor="70AD47"),
}

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")


def _parse_iso_date(s: str) -> date:
    return date.fromisoformat(s)


def _day_of_week(d: date) -> str:
    return d.strftime("%A")


def _write_calendar_sheet(ws, campaigns: list[dict]):
    """Sheet 1: chronological list of every send."""
    headers = ["Date", "Day", "Time", "Channel", "Campaign", "Topic", "Owner", "Status", "Notes"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    # Flatten all sends from all campaigns, attach campaign info
    all_sends: list[dict] = []
    for campaign in campaigns:
        for send in campaign.get("sends", []) or []:
            all_sends.append({
                **send,
                "_campaign_name": campaign.get("campaign_name", ""),
                "_campaign_type": campaign.get("campaign_type", "Other"),
            })

    # Sort by date, then time
    all_sends.sort(key=lambda s: (s.get("date", ""), s.get("time", "00:00")))

    for send in all_sends:
        date_str = send.get("date", "")
        day = _day_of_week(_parse_iso_date(date_str)) if date_str else ""
        channel = CHANNEL_DISPLAY.get(send.get("channel", ""), send.get("channel", ""))
        row_values = [
            date_str,
            day,
            send.get("time", ""),
            channel,
            send["_campaign_name"],
            send.get("topic", ""),
            send.get("owner", ""),
            send.get("status", "Planned"),
            send.get("notes", ""),
        ]
        ws.append(row_values)
        # Color the Status cell
        status_cell = ws.cell(row=ws.max_row, column=8)
        status = send.get("status", "Planned")
        if status in STATUS_COLORS:
            status_cell.fill = STATUS_COLORS[status]
        # Color the Campaign cell by type
        campaign_cell = ws.cell(row=ws.max_row, column=5)
        if send["_campaign_type"] in CAMPAIGN_TYPE_COLORS:
            campaign_cell.fill = CAMPAIGN_TYPE_COLORS[send["_campaign_type"]]

    widths = [12, 11, 8, 14, 30, 50, 14, 12, 30]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def _write_campaigns_sheet(ws, campaigns: list[dict]):
    """Sheet 2: one row per campaign with aggregate counts."""
    headers = [
        "Campaign Name",
        "Type",
        "Start Date",
        "End Date",
        "Duration (days)",
        "Email count",
        "SMS count",
        "Paid Ad count",
        "Organic Social count",
        "Site Update count",
        "Total sends",
        "Status",
        "Notes",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for campaign in campaigns:
        sends = campaign.get("sends", []) or []
        # Count per channel
        channel_counts = {ch: 0 for ch in CHANNEL_ORDER}
        for send in sends:
            ch = send.get("channel", "")
            if ch in channel_counts:
                channel_counts[ch] += 1
        start_str = campaign.get("start_date", "")
        end_str = campaign.get("end_date", "")
        duration = ""
        if start_str and end_str:
            try:
                d_start = _parse_iso_date(start_str)
                d_end = _parse_iso_date(end_str)
                duration = (d_end - d_start).days + 1
            except ValueError:
                duration = ""
        row_values = [
            campaign.get("campaign_name", ""),
            campaign.get("campaign_type", "Other"),
            start_str,
            end_str,
            duration,
            channel_counts["email"],
            channel_counts["sms"],
            channel_counts["paid_ad"],
            channel_counts["organic_social"],
            channel_counts["site_update"],
            len(sends),
            campaign.get("status", "Planned"),
            campaign.get("notes", ""),
        ]
        ws.append(row_values)
        # Color the campaign-type cell
        type_cell = ws.cell(row=ws.max_row, column=2)
        if campaign.get("campaign_type") in CAMPAIGN_TYPE_COLORS:
            type_cell.fill = CAMPAIGN_TYPE_COLORS[campaign["campaign_type"]]

    widths = [30, 14, 12, 12, 10, 10, 10, 10, 14, 14, 11, 11, 30]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def _write_monthly_view_sheet(ws, campaigns: list[dict], window_start: date, window_end: date):
    """Sheet 3: matrix of dates x channels showing send density."""
    headers = ["Date", "Day"] + [CHANNEL_DISPLAY[ch] for ch in CHANNEL_ORDER]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    # Build a date -> channel -> count map
    by_date: dict[date, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for campaign in campaigns:
        for send in campaign.get("sends", []) or []:
            try:
                d = _parse_iso_date(send.get("date", ""))
            except ValueError:
                continue
            ch = send.get("channel", "")
            by_date[d][ch] += 1

    # Iterate every day in the window
    cur = window_start
    while cur <= window_end:
        row = [cur.isoformat(), _day_of_week(cur)]
        for ch in CHANNEL_ORDER:
            count = by_date.get(cur, {}).get(ch, 0)
            row.append(count if count > 0 else "")
        ws.append(row)
        # Highlight weekends slightly
        if cur.weekday() >= 5:
            for col_idx in range(1, 8):
                ws.cell(row=ws.max_row, column=col_idx).fill = PatternFill("solid", fgColor="F7F7F7")
        cur += timedelta(days=1)

    widths = [12, 11, 8, 8, 10, 14, 14]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "C2"


def render(data: dict, output_path: Path) -> Path:
    campaigns = data.get("campaigns", []) or []
    window = data.get("calendar_window", {})
    window_start = _parse_iso_date(window.get("start", date.today().isoformat()))
    window_end = _parse_iso_date(window.get("end", (date.today() + timedelta(days=90)).isoformat()))

    wb = Workbook()
    ws_cal = wb.active
    ws_cal.title = "Calendar"
    _write_calendar_sheet(ws_cal, campaigns)

    ws_camp = wb.create_sheet("Campaigns")
    _write_campaigns_sheet(ws_camp, campaigns)

    ws_monthly = wb.create_sheet("Monthly View")
    _write_monthly_view_sheet(ws_monthly, campaigns, window_start, window_end)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_calendar_xlsx.py <calendar_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
