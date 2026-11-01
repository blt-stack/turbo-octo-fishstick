"""
Render a full-catalog forecast to a 5-sheet .xlsx workbook.

Sheets:
  1. SKU Forecast              — one row per SKU with status, velocity, forecast, reorder action
  2. Stockout Risk             — filtered view of just at-risk SKUs (most urgent first)
  3. Reorder Calendar          — chronological list of recommended actions by date
  4. Seasonality Patterns      — SKUs with detected seasonality
  5. Method Audit Log          — per-SKU method selection + confidence

Input JSON shape:
    {
      "brand_name": "...",
      "generated_at": "2026-04-15",
      "skus": [
        { ...forecast_sku() result with product_name + supplier_id added... },
        ...
      ]
    }

Requires openpyxl (pip install openpyxl --break-system-packages).
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


METHOD_DISPLAY = {
    "rolling_average_14d": "Rolling Avg (14d)",
    "holt": "Holt",
    "holt_winters": "Holt-Winters",
    "poisson_heuristic": "Poisson (sporadic)",
    "skipped": "Skipped",
    "failed": "Failed",
}

URGENCY_FILLS = {
    "healthy": PatternFill("solid", fgColor="C6EFCE"),
    "reorder_soon": PatternFill("solid", fgColor="FFEB9C"),
    "urgent": PatternFill("solid", fgColor="F7CAAC"),
    "stockout_imminent": PatternFill("solid", fgColor="FFC7CE"),
}

CONFIDENCE_FILLS = {
    "high": PatternFill("solid", fgColor="C6EFCE"),
    "medium": PatternFill("solid", fgColor="FFEB9C"),
    "low": PatternFill("solid", fgColor="F7CAAC"),
    "unreliable": PatternFill("solid", fgColor="FFC7CE"),
}

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")


def _urgency_rank(u: str) -> int:
    order = ["stockout_imminent", "urgent", "reorder_soon", "healthy"]
    return order.index(u) if u in order else 5


def _write_sku_forecast(ws, skus: list[dict]):
    headers = [
        "SKU", "Product", "Supplier ID", "Method", "Confidence",
        "History Days", "Velocity (units/day)", "On Hand",
        "Days to Stockout (P50)",
        "30-day Forecast (P50)", "60-day Forecast (P50)", "90-day Forecast (P50)",
        "Status", "Recommended Reorder Qty", "Deposit Date", "Expected Arrival",
        "Est. Reorder Cost (USD)", "Warnings",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for sku in skus:
        audit = sku.get("audit", {})
        reorder = sku.get("reorder_calc", {})
        fc = sku.get("forecast", {})
        method = METHOD_DISPLAY.get(sku.get("method_selected", ""), sku.get("method_selected", ""))
        urgency = reorder.get("urgency", "healthy")
        confidence = audit.get("confidence_assessment", "medium")

        row = [
            sku.get("sku", ""),
            sku.get("product_name", ""),
            sku.get("supplier_id", ""),
            method,
            confidence,
            audit.get("history_days", ""),
            round(audit.get("mean_velocity_units_per_day", 0), 2),
            reorder.get("current_on_hand", ""),
            round(reorder.get("days_until_stockout_p50", 0), 1) if reorder.get("days_until_stockout_p50") is not None else "",
            round(fc.get("horizon_30d", {}).get("p50", 0), 0),
            round(fc.get("horizon_60d", {}).get("p50", 0), 0),
            round(fc.get("horizon_90d", {}).get("p50", 0), 0),
            urgency,
            reorder.get("recommended_reorder_quantity", ""),
            reorder.get("recommended_deposit_date", ""),
            reorder.get("expected_arrive_date", ""),
            reorder.get("estimated_reorder_cost_usd", ""),
            ", ".join(sku.get("warnings", []) or []),
        ]
        ws.append(row)
        row_idx = ws.max_row
        if urgency in URGENCY_FILLS:
            ws.cell(row=row_idx, column=13).fill = URGENCY_FILLS[urgency]
        if confidence in CONFIDENCE_FILLS:
            ws.cell(row=row_idx, column=5).fill = CONFIDENCE_FILLS[confidence]

    widths = [18, 26, 24, 16, 12, 12, 16, 10, 16, 14, 14, 14, 16, 18, 14, 16, 16, 36]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions


def _write_stockout_risk(ws, skus: list[dict]):
    at_risk = [s for s in skus if s.get("reorder_calc", {}).get("urgency") in ("stockout_imminent", "urgent", "reorder_soon")]
    at_risk.sort(key=lambda s: _urgency_rank(s.get("reorder_calc", {}).get("urgency", "healthy")))

    headers = [
        "SKU", "Product", "Urgency", "Days to Stockout (P50)", "Days to Stockout (P90)",
        "Lead Time (days)", "Days Short Before Arrival",
        "Reorder Qty", "Deposit Date", "Est. Cost (USD)",
        "Expedite Suggested?", "Action Plan (buyer fills in)",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for sku in at_risk:
        reorder = sku.get("reorder_calc", {})
        urgency = reorder.get("urgency", "")
        days_short = reorder.get("days_short_before_arrival", 0)
        expedite = "Yes" if days_short > 0 or urgency == "stockout_imminent" else "No"
        row = [
            sku.get("sku", ""),
            sku.get("product_name", ""),
            urgency,
            round(reorder.get("days_until_stockout_p50", 0), 1) if reorder.get("days_until_stockout_p50") is not None else "",
            round(reorder.get("days_until_stockout_p90", 0), 1) if reorder.get("days_until_stockout_p90") is not None else "",
            reorder.get("lead_time_days", ""),
            days_short,
            reorder.get("recommended_reorder_quantity", ""),
            reorder.get("recommended_deposit_date", ""),
            reorder.get("estimated_reorder_cost_usd", ""),
            expedite,
            "",  # action plan filled by buyer
        ]
        ws.append(row)
        row_idx = ws.max_row
        if urgency in URGENCY_FILLS:
            ws.cell(row=row_idx, column=3).fill = URGENCY_FILLS[urgency]

    if not at_risk:
        ws.append(["(No SKUs at risk in this forecast — catalog is healthy.)"] + [""] * 11)

    widths = [18, 26, 18, 16, 16, 14, 18, 14, 14, 16, 16, 40]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"


def _write_reorder_calendar(ws, skus: list[dict]):
    actions = []
    for sku in skus:
        reorder = sku.get("reorder_calc", {})
        urgency = reorder.get("urgency", "healthy")
        if urgency in ("urgent", "reorder_soon", "stockout_imminent"):
            actions.append({
                "deposit_date": reorder.get("recommended_deposit_date", "9999-12-31"),
                "sku": sku.get("sku", ""),
                "product": sku.get("product_name", ""),
                "supplier": sku.get("supplier_id", ""),
                "qty": reorder.get("recommended_reorder_quantity", 0),
                "cost": reorder.get("estimated_reorder_cost_usd", 0),
                "urgency": urgency,
                "expected_arrival": reorder.get("expected_arrive_date", ""),
            })
    actions.sort(key=lambda a: a["deposit_date"])

    headers = ["Deposit Date", "SKU", "Product", "Supplier", "Reorder Qty", "Est. Cost", "Urgency", "Expected Arrival"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for a in actions:
        ws.append([
            a["deposit_date"], a["sku"], a["product"], a["supplier"],
            a["qty"], a["cost"], a["urgency"], a["expected_arrival"],
        ])
        row_idx = ws.max_row
        if a["urgency"] in URGENCY_FILLS:
            ws.cell(row=row_idx, column=7).fill = URGENCY_FILLS[a["urgency"]]

    if not actions:
        ws.append(["(No reorders required in the forecast horizon.)"] + [""] * 7)

    widths = [16, 18, 26, 26, 14, 14, 18, 18]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "A2"


def _write_seasonality(ws, skus: list[dict]):
    seasonal_skus = [s for s in skus if s.get("audit", {}).get("seasonal_period_detected")]

    headers = ["SKU", "Product", "Seasonal Period (days)", "Signal Strength", "Method", "Confidence"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for sku in seasonal_skus:
        audit = sku.get("audit", {})
        ws.append([
            sku.get("sku", ""),
            sku.get("product_name", ""),
            audit.get("seasonal_period_detected", ""),
            round(audit.get("seasonal_signal_strength", 0), 2),
            METHOD_DISPLAY.get(sku.get("method_selected", ""), sku.get("method_selected", "")),
            audit.get("confidence_assessment", ""),
        ])

    if not seasonal_skus:
        ws.append(["(No seasonal patterns detected in this batch.)"] + [""] * 5)

    widths = [18, 26, 22, 16, 18, 14]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def _write_audit_log(ws, skus: list[dict]):
    headers = ["SKU", "Method", "Rationale", "Confidence", "History Days", "Fallback?", "Warnings"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for sku in skus:
        audit = sku.get("audit", {})
        ws.append([
            sku.get("sku", ""),
            METHOD_DISPLAY.get(sku.get("method_selected", ""), sku.get("method_selected", "")),
            sku.get("method_rationale", ""),
            audit.get("confidence_assessment", ""),
            audit.get("history_days", ""),
            "Yes" if audit.get("fallback_applied") else "No",
            ", ".join(sku.get("warnings", []) or []),
        ])
        row_idx = ws.max_row
        conf = audit.get("confidence_assessment", "medium")
        if conf in CONFIDENCE_FILLS:
            ws.cell(row=row_idx, column=4).fill = CONFIDENCE_FILLS[conf]

    widths = [18, 18, 60, 14, 12, 12, 36]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions


def render(data: dict, output_path: Path) -> Path:
    skus = data.get("skus", []) or []

    wb = Workbook()
    ws_main = wb.active
    ws_main.title = "SKU Forecast"
    _write_sku_forecast(ws_main, skus)

    ws_risk = wb.create_sheet("Stockout Risk")
    _write_stockout_risk(ws_risk, skus)

    ws_cal = wb.create_sheet("Reorder Calendar")
    _write_reorder_calendar(ws_cal, skus)

    ws_seas = wb.create_sheet("Seasonality Patterns")
    _write_seasonality(ws_seas, skus)

    ws_audit = wb.create_sheet("Method Audit Log")
    _write_audit_log(ws_audit, skus)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_catalog_xlsx.py <catalog_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
