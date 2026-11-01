"""
Render a bulk bundle catalog to a 5-sheet .xlsx workbook.

Sheets:
  1. Bundle Suggestions   — one row per bundle, ranked by composite score
  2. Type Breakdown       — counts + expected impact per bundle type
  3. SKU Participation    — which SKUs appear in which bundles
  4. AOV-Lift Analysis    — for AOV-Lift bundles specifically
  5. Discovery Audit      — per-bundle source layer + reasoning

Requires openpyxl (pip install openpyxl --break-system-packages).
"""

import json
import sys
from collections import Counter
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


TYPE_DISPLAY = {
    "fbt": "FBT",
    "complementary": "Complementary",
    "aov_lift": "AOV-Lift",
    "gift_set": "Gift Set",
    "starter_kit": "Starter Kit",
}

TYPE_FILLS = {
    "fbt": PatternFill("solid", fgColor="D9E1F2"),
    "complementary": PatternFill("solid", fgColor="C6EFCE"),
    "aov_lift": PatternFill("solid", fgColor="FFEB9C"),
    "gift_set": PatternFill("solid", fgColor="FCD5CE"),
    "starter_kit": PatternFill("solid", fgColor="E7CCFC"),
}

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")


def _write_bundle_suggestions(ws, bundles: list[dict]):
    headers = [
        "Rank", "Bundle Name (descriptive)", "Evocative", "Type", "Secondary Types",
        "Composite Score", "SKUs", "SKU Count",
        "Individual Total", "Recommended Price", "Recommended Tier", "Savings",
        "Blended Margin", "Cost Data?", "Status",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for i, b in enumerate(bundles, 1):
        recommended_tier = b.get("recommended_tier", "standard")
        tier_data = b.get("pricing_tiers", {}).get(recommended_tier, {})
        skus_list = "; ".join(s.get("sku", "") for s in b.get("skus_included", []))
        retail_total = sum((s.get("individual_price_usd") or 0) for s in b.get("skus_included", []))
        ev = b.get("discovery_evidence", {})
        has_cost = "Yes" if ev.get("has_cost_data") else "No"

        row = [
            i,
            b.get("bundle_name_descriptive", ""),
            b.get("bundle_name_evocative", ""),
            TYPE_DISPLAY.get(b.get("bundle_type_primary", ""), b.get("bundle_type_primary", "")),
            ", ".join([TYPE_DISPLAY.get(t, t) for t in b.get("bundle_type_secondary", [])]),
            ev.get("composite_score", 0),
            skus_list,
            len(b.get("skus_included", [])),
            round(retail_total, 2),
            tier_data.get("bundle_price_usd", ""),
            recommended_tier,
            tier_data.get("savings_usd", ""),
            f"{tier_data.get('blended_margin_pct', 0) * 100:.1f}%" if tier_data.get("blended_margin_pct") is not None else "n/a",
            has_cost,
            "Suggested",
        ]
        ws.append(row)
        row_idx = ws.max_row
        primary_type = b.get("bundle_type_primary", "")
        if primary_type in TYPE_FILLS:
            ws.cell(row=row_idx, column=4).fill = TYPE_FILLS[primary_type]

    widths = [6, 32, 28, 18, 22, 14, 50, 10, 14, 16, 16, 12, 14, 10, 14]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions


def _write_type_breakdown(ws, bundles: list[dict]):
    headers = ["Bundle Type", "Count", "Avg Composite Score", "Total Potential Savings"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    type_buckets: dict[str, list[dict]] = {}
    for b in bundles:
        t = b.get("bundle_type_primary", "unknown")
        type_buckets.setdefault(t, []).append(b)

    for t in ("fbt", "complementary", "aov_lift", "gift_set", "starter_kit"):
        bucket = type_buckets.get(t, [])
        if not bucket:
            ws.append([TYPE_DISPLAY.get(t, t), 0, "", ""])
            continue
        avg_score = sum(b.get("discovery_evidence", {}).get("composite_score", 0) for b in bucket) / len(bucket)
        total_savings = sum(
            b.get("pricing_tiers", {}).get(b.get("recommended_tier", "standard"), {}).get("savings_usd", 0)
            for b in bucket
        )
        ws.append([TYPE_DISPLAY.get(t, t), len(bucket), round(avg_score, 1), round(total_savings, 2)])
        if t in TYPE_FILLS:
            ws.cell(row=ws.max_row, column=1).fill = TYPE_FILLS[t]

    widths = [22, 12, 22, 22]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def _write_sku_participation(ws, bundles: list[dict]):
    sku_to_bundles: dict[str, list[str]] = {}
    for b in bundles:
        for s in b.get("skus_included", []):
            sku = s.get("sku", "")
            if sku:
                sku_to_bundles.setdefault(sku, []).append(b.get("bundle_name_descriptive", b.get("bundle_id", "")))

    headers = ["SKU", "Participates In # Bundles", "Bundle Names"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    # Sort by participation count descending
    for sku, bundle_names in sorted(sku_to_bundles.items(), key=lambda x: -len(x[1])):
        ws.append([sku, len(bundle_names), "; ".join(bundle_names)])

    widths = [22, 20, 80]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions


def _write_aov_lift_analysis(ws, bundles: list[dict]):
    aov_bundles = [
        b for b in bundles
        if b.get("bundle_type_primary") == "aov_lift" or "aov_lift" in b.get("bundle_type_secondary", [])
    ]

    headers = ["Bundle", "Bundle Price", "Above Threshold By", "SKUs", "Expected Conversion Rate", "Est. AOV Lift per Conversion"]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    if not aov_bundles:
        ws.append(["(No AOV-Lift bundles in this batch — set free_shipping_threshold_usd in config to enable.)"] + [""] * 5)
    else:
        for b in aov_bundles:
            tier = b.get("recommended_tier", "standard")
            bundle_price = b.get("pricing_tiers", {}).get(tier, {}).get("bundle_price_usd", 0)
            skus = "; ".join(s.get("sku", "") for s in b.get("skus_included", []))
            ws.append([
                b.get("bundle_name_descriptive", ""),
                bundle_price,
                "",  # buyer fills in
                skus,
                "10-20% (estimate; varies)",
                f"${bundle_price * 0.15:.2f} per conversion",
            ])

    widths = [32, 14, 20, 50, 26, 26]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"


def _write_discovery_audit(ws, bundles: list[dict]):
    headers = [
        "Bundle", "Source Layer",
        "Apriori Support", "Apriori Lift", "Co-occurrence Count",
        "Categorical Use-Case", "Margin Score", "In-Stock Score", "Composite Score",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for b in bundles:
        ev = b.get("discovery_evidence", {})
        ws.append([
            b.get("bundle_name_descriptive", ""),
            ev.get("source_layer", ""),
            f"{ev.get('apriori_support', 0) * 100:.2f}%" if ev.get("apriori_support") is not None else "—",
            f"{ev.get('apriori_lift', 0):.2f}×" if ev.get("apriori_lift") is not None else "—",
            ev.get("co_occurrence_count", "—"),
            ev.get("categorical_use_case", "—"),
            ev.get("margin_score", "—"),
            ev.get("in_stock_velocity_score", "—"),
            ev.get("composite_score", "—"),
        ])

    widths = [32, 22, 16, 14, 18, 26, 14, 14, 16]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"


def render(data: dict, output_path: Path) -> Path:
    bundles = data.get("bundles", []) or []

    wb = Workbook()
    ws_main = wb.active
    ws_main.title = "Bundle Suggestions"
    _write_bundle_suggestions(ws_main, bundles)

    ws_breakdown = wb.create_sheet("Type Breakdown")
    _write_type_breakdown(ws_breakdown, bundles)

    ws_skus = wb.create_sheet("SKU Participation")
    _write_sku_participation(ws_skus, bundles)

    ws_aov = wb.create_sheet("AOV-Lift Analysis")
    _write_aov_lift_analysis(ws_aov, bundles)

    ws_audit = wb.create_sheet("Discovery Audit")
    _write_discovery_audit(ws_audit, bundles)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_bundles_xlsx.py <bundles_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
