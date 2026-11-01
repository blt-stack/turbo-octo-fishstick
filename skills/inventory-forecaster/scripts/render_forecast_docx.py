"""
Render a single SKU forecast to a .docx file.

Structure:
- Header (SKU, product name, method, generated date)
- Data summary (history window, total units, average velocity, seasonal signal, trend)
- Method choice + rationale
- 30 / 60 / 90 day forecast (P10 / P50 / P90)
- Stockout risk + reorder math (urgency, supplier, lead time, payment terms)
- Risks + assumptions
- Next steps

Input JSON shape is the result of forecast_sku() augmented with supplier context.

Requires python-docx (pip install python-docx --break-system-packages).
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor


METHOD_DISPLAY = {
    "rolling_average_14d": "Rolling Average (14-day)",
    "holt": "Exponential Smoothing (Holt)",
    "holt_winters": "Seasonal Exponential Smoothing (Holt-Winters)",
    "poisson_heuristic": "Poisson Heuristic (sporadic)",
    "skipped": "Skipped",
    "failed": "Failed",
}

URGENCY_COLORS = {
    "healthy": RGBColor(0x1E, 0x7A, 0x2C),
    "reorder_soon": RGBColor(0xB8, 0x86, 0x0B),
    "urgent": RGBColor(0xC0, 0x55, 0x00),
    "stockout_imminent": RGBColor(0xC0, 0x00, 0x00),
}

CONFIDENCE_COLORS = {
    "high": RGBColor(0x1E, 0x7A, 0x2C),
    "medium": RGBColor(0xB8, 0x86, 0x0B),
    "low": RGBColor(0xC0, 0x55, 0x00),
    "unreliable": RGBColor(0xC0, 0x00, 0x00),
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


def _add_kv(doc, label: str, value):
    p = doc.add_paragraph()
    label_run = p.add_run(f"{label}: ")
    label_run.bold = True
    text = "—" if value in (None, "") else str(value)
    p.add_run(text)


def _render_header(doc, data: dict):
    title_p = doc.add_paragraph()
    sku = data.get("sku", "Unknown SKU")
    product_name = data.get("product_name", "")
    title_run = title_p.add_run(f"Forecast: {product_name or sku}")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    method = METHOD_DISPLAY.get(data.get("method_selected", ""), data.get("method_selected", ""))
    generated_at = data.get("generated_at", "")
    meta_run = meta_p.add_run(f"SKU: {sku}  ·  Method: {method}  ·  Generated: {generated_at}")
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    audit = data.get("audit", {})
    confidence = audit.get("confidence_assessment", "medium")
    conf_p = doc.add_paragraph()
    conf_run = conf_p.add_run(f"Confidence: {confidence}")
    conf_run.bold = True
    if confidence in CONFIDENCE_COLORS:
        conf_run.font.color.rgb = CONFIDENCE_COLORS[confidence]


def _render_data_summary(doc, data: dict):
    audit = data.get("audit", {})
    _add_divider(doc)
    _add_section_header(doc, "DATA SUMMARY")
    _add_kv(doc, "History days", audit.get("history_days"))
    _add_kv(doc, "First sale", audit.get("first_sale_date"))
    _add_kv(doc, "Last sale", audit.get("last_sale_date"))
    _add_kv(doc, "Total units sold (history)", audit.get("total_units_sold_history"))
    velocity = audit.get("mean_velocity_units_per_day")
    if velocity is not None:
        _add_kv(doc, "Average daily velocity", f"{velocity:.2f} units/day")
    if audit.get("seasonal_period_detected"):
        period = audit["seasonal_period_detected"]
        strength = audit.get("seasonal_signal_strength", 0)
        _add_kv(doc, "Seasonal signal", f"{period}-day period (autocorrelation {strength:.2f})")
    if audit.get("trend_detected"):
        _add_kv(doc, "Trend", audit["trend_detected"])


def _render_method_choice(doc, data: dict):
    _add_divider(doc)
    _add_section_header(doc, "METHOD CHOICE + RATIONALE")
    method = METHOD_DISPLAY.get(data.get("method_selected", ""), data.get("method_selected", ""))
    _add_kv(doc, "Method", method)
    _add_kv(doc, "Why", data.get("method_rationale", ""))
    audit = data.get("audit", {})
    if audit.get("fallback_applied"):
        p = doc.add_paragraph()
        run = p.add_run("Note: A fallback was applied due to model fit issues. See warnings.")
        run.italic = True
        run.font.color.rgb = RGBColor(0xB8, 0x86, 0x0B)


def _render_forecast(doc, data: dict):
    _add_divider(doc)
    _add_section_header(doc, "30 / 60 / 90 DAY FORECAST")

    fc = data.get("forecast", {})
    for label, key in [("30-day", "horizon_30d"), ("60-day", "horizon_60d"), ("90-day", "horizon_90d")]:
        h = fc.get(key, {})
        if h:
            _add_subheader(doc, f"{label} demand")
            doc.add_paragraph(f"Conservative (P10): {h.get('p10', 0):.0f} units", style="List Bullet")
            doc.add_paragraph(f"Base (P50):         {h.get('p50', 0):.0f} units", style="List Bullet")
            doc.add_paragraph(f"Aggressive (P90):   {h.get('p90', 0):.0f} units", style="List Bullet")


def _render_reorder_math(doc, data: dict):
    reorder = data.get("reorder_calc", {})
    if not reorder:
        return
    _add_divider(doc)
    _add_section_header(doc, "STOCKOUT RISK + REORDER MATH")

    urgency = reorder.get("urgency", "healthy")
    urg_p = doc.add_paragraph()
    urg_run = urg_p.add_run(f"Status: {urgency.upper().replace('_', ' ')}")
    urg_run.bold = True
    urg_run.font.size = Pt(13)
    if urgency in URGENCY_COLORS:
        urg_run.font.color.rgb = URGENCY_COLORS[urgency]

    _add_kv(doc, "Current on-hand", f"{reorder.get('current_on_hand', 0):.0f} units")
    _add_kv(doc, "Velocity (P50)", f"{reorder.get('velocity_p50_units_per_day', 0):.2f} units/day")
    _add_kv(doc, "Days until stockout (P50)", f"{reorder.get('days_until_stockout_p50', 0):.0f} days")
    _add_kv(doc, "Days until stockout (P90 — demand spike)", f"{reorder.get('days_until_stockout_p90', 0):.0f} days")

    _add_subheader(doc, "Supplier + reorder structure")
    _add_kv(doc, "Lead time", f"{reorder.get('lead_time_days', 0)} days")
    _add_kv(doc, "Transit", f"{reorder.get('transit_days', 0)} days")
    _add_kv(doc, "MOQ", f"{reorder.get('moq', 0)} units")
    _add_kv(doc, "Payment terms in force", reorder.get("payment_terms_in_force", "—"))

    _add_subheader(doc, "Recommended action")
    _add_kv(doc, "Reorder quantity", f"{reorder.get('recommended_reorder_quantity', 0)} units")
    _add_kv(doc, "Send deposit by", reorder.get("recommended_deposit_date", "—"))
    _add_kv(doc, "Expected arrival", reorder.get("expected_arrive_date", "—"))
    _add_kv(doc, "Estimated reorder cost", f"${reorder.get('estimated_reorder_cost_usd', 0):,.2f}")
    days_short = reorder.get("days_short_before_arrival", 0)
    if days_short > 0:
        p = doc.add_paragraph()
        run = p.add_run(f"⚠ {days_short} days short before arrival — consider expediting via air freight or accepting partial stockout.")
        run.bold = True
        run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)


def _render_warnings(doc, data: dict):
    warnings = data.get("warnings", [])
    if not warnings:
        return
    _add_divider(doc)
    _add_section_header(doc, "WARNINGS")
    for w in warnings:
        doc.add_paragraph(f"⚠ {w}", style="List Bullet")


def _render_next_steps(doc, data: dict):
    _add_divider(doc)
    _add_section_header(doc, "NEXT STEPS")
    reorder = data.get("reorder_calc", {})
    urgency = reorder.get("urgency", "healthy")
    if urgency == "stockout_imminent":
        doc.add_paragraph("1. Stockout will happen before reorder can arrive. Decide: expedite via air freight, or accept partial stockout.", style="List Number")
        doc.add_paragraph("2. Draft a reorder letter to the supplier today (skill #11 has the trigger).", style="List Number")
        doc.add_paragraph("3. Plan customer communication if stockout is unavoidable.", style="List Number")
    elif urgency == "urgent":
        doc.add_paragraph("1. Send reorder to supplier today. Trigger has been written to .cache/reorder_triggers/.", style="List Number")
        doc.add_paragraph("2. Skill #11 (Supplier Negotiation Assistant) will surface this trigger next time you draft supplier letters.", style="List Number")
        doc.add_paragraph("3. Re-forecast in 7 days to confirm reorder timing.", style="List Number")
    elif urgency == "reorder_soon":
        doc.add_paragraph("1. Schedule reorder within the next 7-14 days.", style="List Number")
        doc.add_paragraph("2. Trigger has been written to .cache/reorder_triggers/.", style="List Number")
        doc.add_paragraph("3. Re-forecast in 14 days to monitor velocity drift.", style="List Number")
    else:
        doc.add_paragraph("1. No immediate action needed — inventory is healthy.", style="List Number")
        doc.add_paragraph("2. Re-forecast in 14-30 days.", style="List Number")


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_header(doc, data)
    _render_data_summary(doc, data)
    _render_method_choice(doc, data)
    _render_forecast(doc, data)
    _render_reorder_math(doc, data)
    _render_warnings(doc, data)
    _render_next_steps(doc, data)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_forecast_docx.py <forecast_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
