"""
Render a bulk-mode SEO audit to a multi-sheet .xlsx workbook.

Three sheets:
  1. Scores       — one row per product, columns for total + sub-scores per platform.
                    Conditional formatting (red < 60, yellow 60-79, green >= 80).
  2. Rewrites     — one row per product, columns for optimized title/bullets/etc.
                    per enabled platform.
  3. Action Items — one row per (product × issue), sortable for triage.

Input JSON shape:
    {
      "store_name": "...",
      "generated_at": "2026-05-21",
      "products": [
        {
          "product_name": "...",
          "sku": "...",
          "source": "Shopify | URL | pasted",
          "scores": {
            "shopify": {"total": 72, "subscores": {...}, "issues": [...]},
            "amazon":  {"total": 61, ...},
            ...
          },
          "rewrites": {
            "shopify": {"meta_title": "...", "meta_description": "...", "url_handle": "..."},
            "amazon":  {"title": "...", "bullets_joined": "...", "description": "...", "backend_search_terms": "..."},
            ...
          }
        },
        ...
      ]
    }

Requires openpyxl (pip install openpyxl --break-system-packages).
"""

import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


PLATFORM_ORDER = ["shopify", "amazon", "etsy", "ebay", "walmart", "tiktok_shop"]
PLATFORM_DISPLAY = {
    "shopify": "Shopify",
    "amazon": "Amazon",
    "etsy": "Etsy",
    "ebay": "eBay",
    "walmart": "Walmart",
    "tiktok_shop": "TikTok Shop",
}

# Per-platform rewrite columns (column_label, key in rewrite dict)
REWRITE_COLUMNS = {
    "shopify": [
        ("Meta Title", "meta_title"),
        ("Meta Description", "meta_description"),
        ("URL Handle", "url_handle"),
    ],
    "amazon": [
        ("Title", "title"),
        ("Bullets", "bullets_joined"),
        ("Description", "description"),
        ("Backend Search Terms", "backend_search_terms"),
    ],
    "etsy": [
        ("Title", "title"),
        ("Tags", "tags_joined"),
        ("Description", "description"),
    ],
    "ebay": [
        ("Title", "title"),
        ("Description", "description"),
    ],
    "walmart": [
        ("Product Name", "title"),
        ("Bullets", "bullets_joined"),
        ("Description", "description"),
    ],
    "tiktok_shop": [
        ("Product Name", "title"),
        ("Description", "description"),
    ],
}

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")


def _detect_enabled_platforms(products: list[dict]) -> list[str]:
    enabled: set[str] = set()
    for p in products:
        for platform in p.get("scores", {}).keys():
            enabled.add(platform)
        for platform in p.get("rewrites", {}).keys():
            enabled.add(platform)
    return [p for p in PLATFORM_ORDER if p in enabled]


def _get_rewrite_value(rewrite: dict, key: str) -> str:
    if key == "bullets_joined":
        return " | ".join(rewrite.get("bullets", []) or [])
    if key == "tags_joined":
        return ", ".join(rewrite.get("tags", []) or [])
    return str(rewrite.get(key, "") or "")


def _write_scores_sheet(ws, products: list[dict], platforms: list[str]):
    headers = ["Product Name", "SKU"]
    for p in platforms:
        prefix = PLATFORM_DISPLAY[p]
        headers.extend([
            f"{prefix} Total",
            f"{prefix} KW Cov",
            f"{prefix} Title",
            f"{prefix} Bullets",
            f"{prefix} Backend",
            f"{prefix} Complete",
        ])
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for product in products:
        row = [product.get("product_name", ""), product.get("sku", "")]
        scores_obj = product.get("scores", {})
        for platform in platforms:
            s = scores_obj.get(platform, {})
            sub = s.get("subscores", {})
            row.extend([
                s.get("total", ""),
                sub.get("keyword_coverage", ""),
                sub.get("title_strength", ""),
                sub.get("bullet_quality", ""),
                sub.get("backend_structured", ""),
                sub.get("completeness", ""),
            ])
        ws.append(row)

    # Conditional formatting on the Total columns
    if products:
        last_row = 1 + len(products)
        col_idx = 3  # first total column is C
        for i in range(len(platforms)):
            total_col_letter = get_column_letter(col_idx)
            rng = f"{total_col_letter}2:{total_col_letter}{last_row}"
            green = PatternFill("solid", fgColor="C6EFCE")
            yellow = PatternFill("solid", fgColor="FFEB9C")
            red = PatternFill("solid", fgColor="FFC7CE")
            ws.conditional_formatting.add(
                rng, CellIsRule(operator="greaterThanOrEqual", formula=["80"], fill=green)
            )
            ws.conditional_formatting.add(
                rng, CellIsRule(operator="between", formula=["60", "79.99"], fill=yellow)
            )
            ws.conditional_formatting.add(
                rng, CellIsRule(operator="lessThan", formula=["60"], fill=red)
            )
            col_idx += 6  # next platform block starts 6 cols later

    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 14
    for i in range(3, 3 + len(platforms) * 6):
        ws.column_dimensions[get_column_letter(i)].width = 11
    ws.freeze_panes = "C2"


def _write_rewrites_sheet(ws, products: list[dict], platforms: list[str]):
    headers = ["Product Name", "SKU"]
    col_specs: list[tuple[str, str, str]] = []  # (label, platform, key)
    for platform in platforms:
        for label, key in REWRITE_COLUMNS[platform]:
            full_label = f"{PLATFORM_DISPLAY[platform]} {label}"
            headers.append(full_label)
            col_specs.append((full_label, platform, key))
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for product in products:
        row = [product.get("product_name", ""), product.get("sku", "")]
        rewrites_obj = product.get("rewrites", {})
        for _label, platform, key in col_specs:
            rewrite = rewrites_obj.get(platform, {})
            row.append(_get_rewrite_value(rewrite, key))
        ws.append(row)

    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 14
    for i in range(3, 3 + len(col_specs)):
        ws.column_dimensions[get_column_letter(i)].width = 48

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "C2"


def _write_action_items_sheet(ws, products: list[dict]):
    ws.append(["Product Name", "SKU", "Platform", "Issue"])
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for product in products:
        scores_obj = product.get("scores", {})
        for platform, s in scores_obj.items():
            for issue in s.get("issues", []):
                ws.append([
                    product.get("product_name", ""),
                    product.get("sku", ""),
                    PLATFORM_DISPLAY.get(platform, platform),
                    issue,
                ])

    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 14
    ws.column_dimensions["D"].width = 80
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.auto_filter.ref = ws.dimensions
    ws.freeze_panes = "A2"


def render(data: dict, output_path: Path) -> Path:
    products = data.get("products", [])
    platforms = _detect_enabled_platforms(products)

    wb = Workbook()
    ws_scores = wb.active
    ws_scores.title = "Scores"
    _write_scores_sheet(ws_scores, products, platforms)

    ws_rewrites = wb.create_sheet("Rewrites")
    _write_rewrites_sheet(ws_rewrites, products, platforms)

    ws_actions = wb.create_sheet("Action Items")
    _write_action_items_sheet(ws_actions, products)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_bulk_audit_xlsx.py <bulk_audit_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
