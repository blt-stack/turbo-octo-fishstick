"""
Render bulk-mode output to a multi-sheet .xlsx workbook.

Three sheets:
  1. Products       — generated copy, one row per product, columns per platform variant
  2. Character Counts — same shape, cells are "actual/limit" with conditional formatting
  3. Source Info    — per-product audit trail

Usage:
    python render_bulk_xlsx.py <bulk_json> <output_path>

Where <bulk_json> is a JSON file:
    {
      "store_name": "...",
      "generated_at": "2026-05-21",
      "products": [
        {
          "product_name": "...",
          "sku": "...",
          "source": "Shopify | URL | ...",
          "voice_profile_version": "v2026-05-21",
          "keywords_used": ["..."],
          "notes": "...",
          "platforms": {
            "shopify": {"v1": {...}, "v2": {...}},
            "amazon":  {"v1": {...}, "v2": {...}},
            ...
          }
        },
        ...
      ]
    }

Requires openpyxl (install with `pip install openpyxl --break-system-packages`).
"""

import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


# Field map: (platform, variant) -> list of (column_label, field_path, char_limit)
# field_path is a dotted path inside the variant dict.
PLATFORM_COLUMNS = {
    "shopify": [
        ("Shopify Title", "title", None),
        ("Shopify Body", "story", None),
        ("Shopify Meta", "meta_description", 160),
    ],
    "amazon": [
        ("Amazon Title", "title", 200),
        ("Amazon Bullets", "bullets_joined", None),
        ("Amazon Description", "description", 2000),
        ("Amazon Search Terms", "search_terms", 250),
    ],
    "etsy": [
        ("Etsy Title", "title", 140),
        ("Etsy Description", "description", None),
        ("Etsy Tags", "tags_joined", None),
    ],
    "ebay": [
        ("eBay Title", "title", 80),
        ("eBay Description", "description", None),
    ],
    "walmart": [
        ("Walmart Title", "title", 200),
        ("Walmart Bullets", "bullets_joined", None),
        ("Walmart Description", "description", None),
    ],
    "tiktok_shop": [
        ("TikTok Name", "title", 34),
        ("TikTok Description", "description", 800),
    ],
}

PLATFORM_ORDER = ["shopify", "amazon", "etsy", "ebay", "walmart", "tiktok_shop"]

HEADER_FILL = PatternFill("solid", fgColor="1A1A1A")
HEADER_FONT = Font(bold=True, color="FFFFFF")
WRAP = Alignment(wrap_text=True, vertical="top")


def _get_value(variant: dict, field_path: str) -> str:
    """Read a field. Joins list fields into pipe-separated strings."""
    if field_path == "bullets_joined":
        return " | ".join(variant.get("bullets", []))
    if field_path == "tags_joined":
        return ", ".join(variant.get("tags", []))
    return str(variant.get(field_path, "") or "")


def _build_column_spec(platforms_enabled: list[str]) -> list[tuple[str, str, str, int | None]]:
    """
    Returns list of (column_label, platform, field_path, char_limit) for every
    platform x variant the buyer has enabled.
    """
    cols: list[tuple[str, str, str, int | None]] = []
    for platform in PLATFORM_ORDER:
        if platform not in platforms_enabled:
            continue
        for label, field, limit in PLATFORM_COLUMNS[platform]:
            for variant_key, variant_num in (("v1", "v1"), ("v2", "v2")):
                cols.append(
                    (
                        f"{label} {variant_num}",
                        platform,
                        f"{variant_key}.{field}",
                        limit,
                    )
                )
    return cols


def _detect_enabled_platforms(products: list[dict]) -> list[str]:
    """Detect which platforms appear in the data — derive enabled list from the data itself."""
    enabled = set()
    for product in products:
        for platform in product.get("platforms", {}).keys():
            enabled.add(platform)
    return [p for p in PLATFORM_ORDER if p in enabled]


def _write_products_sheet(ws, products: list[dict], col_spec: list[tuple]):
    headers = ["Product Name", "SKU", "Source"] + [c[0] for c in col_spec]
    ws.append(headers)

    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="left", vertical="center")

    for product in products:
        row = [
            product.get("product_name", ""),
            product.get("sku", ""),
            product.get("source", ""),
        ]
        for col_label, platform, field_path, _limit in col_spec:
            variant_key, field = field_path.split(".", 1)
            variant = product.get("platforms", {}).get(platform, {}).get(variant_key, {})
            row.append(_get_value(variant, field))
        ws.append(row)

    # Sizing
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 12
    for i in range(4, 4 + len(col_spec)):
        ws.column_dimensions[get_column_letter(i)].width = 48

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP

    ws.freeze_panes = "D2"


def _write_counts_sheet(ws, products: list[dict], col_spec: list[tuple]):
    headers = ["Product Name"] + [c[0] for c in col_spec if c[3] is not None]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    counted_cols = [c for c in col_spec if c[3] is not None]
    for product in products:
        row = [product.get("product_name", "")]
        for col_label, platform, field_path, limit in counted_cols:
            variant_key, field = field_path.split(".", 1)
            variant = product.get("platforms", {}).get(platform, {}).get(variant_key, {})
            value = _get_value(variant, field)
            row.append(f"{len(value)}/{limit}")
        ws.append(row)

    # Conditional formatting: red fill for over-limit cells
    if len(counted_cols) > 0 and len(products) > 0:
        last_col_letter = get_column_letter(1 + len(counted_cols))
        rng = f"B2:{last_col_letter}{1 + len(products)}"
        # Over-limit cells contain values where the part before "/" > part after.
        # openpyxl's rules work on cell text — we add cells with red fill where text
        # starts with a number bigger than its limit. Simplest: leave human review.
        # We still add a red fill for any cell whose text reads "<N>/<L>" with N>L.
        # Use formula-based rule.
        from openpyxl.formatting.rule import FormulaRule

        formula = f'VALUE(LEFT(B2,FIND("/",B2)-1)) > VALUE(MID(B2,FIND("/",B2)+1,10))'
        red_fill = PatternFill("solid", fgColor="FFC7CE")
        rule = FormulaRule(formula=[formula], fill=red_fill)
        ws.conditional_formatting.add(rng, rule)

    ws.column_dimensions["A"].width = 28
    for i in range(2, 2 + len(counted_cols)):
        ws.column_dimensions[get_column_letter(i)].width = 16
    ws.freeze_panes = "B2"


def _write_source_sheet(ws, products: list[dict]):
    headers = [
        "Product Name",
        "Input Source",
        "Voice Profile Version",
        "Keywords Used",
        "Generated At",
        "Notes",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for product in products:
        ws.append(
            [
                product.get("product_name", ""),
                product.get("source", ""),
                product.get("voice_profile_version", ""),
                ", ".join(product.get("keywords_used", [])),
                product.get("generated_at", ""),
                product.get("notes", ""),
            ]
        )

    widths = [28, 28, 22, 32, 18, 40]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "B2"


def render(data: dict, output_path: Path) -> Path:
    products = data.get("products", [])
    enabled = _detect_enabled_platforms(products)
    col_spec = _build_column_spec(enabled)

    wb = Workbook()
    ws_products = wb.active
    ws_products.title = "Products"
    _write_products_sheet(ws_products, products, col_spec)

    ws_counts = wb.create_sheet("Character Counts")
    _write_counts_sheet(ws_counts, products, col_spec)

    ws_source = wb.create_sheet("Source Info")
    _write_source_sheet(ws_source, products)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_bulk_xlsx.py <bulk_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
