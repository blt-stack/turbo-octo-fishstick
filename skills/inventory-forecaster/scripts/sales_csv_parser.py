"""
Multi-platform sales CSV parser.

Auto-detects platform from header signature and maps to canonical schema:
    {"sku": str, "product_name": str, "date": "YYYY-MM-DD", "units_sold": int, "revenue": float|None, "channel": str}

Supported platforms: Shopify, Amazon, Etsy, Generic.

Usage:
    from sales_csv_parser import parse_csv, detect_platform, normalize_to_canonical

    rows = parse_csv("/path/to/sales.csv")    # auto-detects + normalizes
    # rows is a list of canonical-shaped dicts

CLI:
    python sales_csv_parser.py /path/to/sales.csv
"""

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path


CHANNEL_SHOPIFY = "shopify"
CHANNEL_AMAZON = "amazon"
CHANNEL_ETSY = "etsy"
CHANNEL_GENERIC = "manual"


def _norm(h: str) -> str:
    return (h or "").strip().lower().replace("_", " ")


def detect_platform(headers: list[str]) -> str:
    """Detect platform from header row signature."""
    h = [_norm(x) for x in headers]
    h_set = set(h)
    if any(x.startswith("(child) asin") for x in h) or "asin" in h_set or "units ordered" in h_set:
        return CHANNEL_AMAZON
    if "listing id" in h_set and ("quantity sold" in h_set or "qty sold" in h_set):
        return CHANNEL_ETSY
    if "lineitem sku" in h_set and ("created at" in h_set or "name" in h_set):
        return CHANNEL_SHOPIFY
    if "sku" in h_set and "date" in h_set and ("units sold" in h_set or "units_sold" in h_set):
        return CHANNEL_GENERIC
    return "unknown"


def _parse_date(s: str) -> str | None:
    """Return ISO YYYY-MM-DD or None."""
    if not s:
        return None
    s = s.strip()
    # Strip time and timezone if present
    s = re.sub(r"\s+\d{2}:\d{2}.*$", "", s)
    s = re.sub(r"T\d{2}:\d{2}.*$", "", s)
    # Try common formats
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%m-%d-%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def _to_int(s) -> int:
    if isinstance(s, int):
        return s
    try:
        return int(float(str(s).replace(",", "").strip()))
    except (ValueError, TypeError):
        return 0


def _to_float(s) -> float | None:
    if s in (None, ""):
        return None
    try:
        return float(str(s).replace("$", "").replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def _shopify_row_to_canonical(row: dict) -> dict | None:
    if (row.get("Cancelled at") or "").strip():
        return None
    sku = (row.get("Lineitem sku") or "").strip()
    if not sku:
        return None
    date = _parse_date(row.get("Created at", ""))
    if not date:
        return None
    qty = _to_int(row.get("Lineitem quantity"))
    if qty <= 0:
        return None
    price = _to_float(row.get("Lineitem price"))
    revenue = (price * qty) if price is not None else None
    return {
        "sku": sku.upper(),
        "product_name": (row.get("Lineitem name") or "").strip(),
        "date": date,
        "units_sold": qty,
        "revenue": revenue,
        "channel": CHANNEL_SHOPIFY,
    }


def _amazon_row_to_canonical(row: dict) -> dict | None:
    # Amazon column names vary; we look for ASIN-ish + Units Ordered
    sku = ""
    for key in ("(Child) ASIN", "(Parent) ASIN", "ASIN", "asin"):
        if key in row and row[key]:
            sku = row[key].strip()
            break
    if not sku:
        return None
    date = None
    for key in ("Date", "Reporting Period", "date"):
        if key in row and row[key]:
            date = _parse_date(row[key])
            if date:
                break
    if not date:
        return None
    qty = _to_int(row.get("Units Ordered") or row.get("units ordered") or 0)
    if qty <= 0:
        return None
    revenue = _to_float(row.get("Ordered Product Sales") or row.get("ordered product sales"))
    return {
        "sku": sku.upper(),
        "product_name": (row.get("Title") or row.get("title") or "").strip(),
        "date": date,
        "units_sold": qty,
        "revenue": revenue,
        "channel": CHANNEL_AMAZON,
    }


def _etsy_row_to_canonical(row: dict) -> dict | None:
    sku = (row.get("Listing ID") or row.get("listing id") or "").strip()
    if not sku:
        return None
    date = _parse_date(row.get("Date") or row.get("date") or "")
    if not date:
        return None
    qty = _to_int(row.get("Quantity sold") or row.get("Qty sold") or 0)
    if qty <= 0:
        return None
    revenue = _to_float(row.get("Revenue") or row.get("revenue"))
    return {
        "sku": f"ETSY-{sku}",
        "product_name": (row.get("Listing title") or "").strip(),
        "date": date,
        "units_sold": qty,
        "revenue": revenue,
        "channel": CHANNEL_ETSY,
    }


def _generic_row_to_canonical(row: dict) -> dict | None:
    # Case-insensitive key access
    lower_row = {k.lower(): v for k, v in row.items()}
    sku = (lower_row.get("sku") or "").strip()
    if not sku:
        return None
    date = _parse_date(lower_row.get("date", ""))
    if not date:
        return None
    qty = _to_int(lower_row.get("units_sold") or lower_row.get("units sold"))
    if qty <= 0:
        return None
    revenue = _to_float(lower_row.get("revenue"))
    return {
        "sku": sku.upper(),
        "product_name": (lower_row.get("product_name") or "").strip(),
        "date": date,
        "units_sold": qty,
        "revenue": revenue,
        "channel": (lower_row.get("channel") or CHANNEL_GENERIC).lower(),
    }


def parse_csv(path: str | Path, platform_hint: str | None = None) -> list[dict]:
    """Parse a sales CSV file into canonical rows."""
    path = Path(path)
    rows: list[dict] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        platform = platform_hint or detect_platform(reader.fieldnames or [])
        parsers = {
            CHANNEL_SHOPIFY: _shopify_row_to_canonical,
            CHANNEL_AMAZON: _amazon_row_to_canonical,
            CHANNEL_ETSY: _etsy_row_to_canonical,
            CHANNEL_GENERIC: _generic_row_to_canonical,
        }
        parser = parsers.get(platform)
        if not parser:
            raise ValueError(
                f"Could not detect platform from headers: {reader.fieldnames}. "
                f"Pass platform_hint='shopify'|'amazon'|'etsy'|'manual'."
            )
        for row in reader:
            canonical = parser(row)
            if canonical:
                rows.append(canonical)
    return rows


def aggregate_by_sku_date(rows: list[dict]) -> list[dict]:
    """Collapse multi-row (sku, date) entries by summing units_sold + revenue."""
    bucket: dict[tuple[str, str], dict] = {}
    for r in rows:
        key = (r["sku"], r["date"])
        if key not in bucket:
            bucket[key] = dict(r)
        else:
            bucket[key]["units_sold"] += r["units_sold"]
            if r.get("revenue") and bucket[key].get("revenue") is not None:
                bucket[key]["revenue"] += r["revenue"]
            elif r.get("revenue"):
                bucket[key]["revenue"] = r["revenue"]
    return sorted(bucket.values(), key=lambda x: (x["sku"], x["date"]))


def split_by_sku(rows: list[dict]) -> dict[str, list[dict]]:
    """Group rows by SKU."""
    by_sku: dict[str, list[dict]] = {}
    for r in rows:
        by_sku.setdefault(r["sku"], []).append(r)
    return by_sku


def normalize_to_canonical(path: str | Path, platform_hint: str | None = None) -> list[dict]:
    """Parse, aggregate, and return canonical rows."""
    rows = parse_csv(path, platform_hint=platform_hint)
    return aggregate_by_sku_date(rows)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sales_csv_parser.py <csv_path> [platform_hint]")
        sys.exit(1)
    path = sys.argv[1]
    hint = sys.argv[2] if len(sys.argv) >= 3 else None
    rows = normalize_to_canonical(path, platform_hint=hint)
    by_sku = split_by_sku(rows)
    print(f"Parsed {len(rows)} canonical rows across {len(by_sku)} SKUs")
    for sku, sku_rows in list(by_sku.items())[:5]:
        total = sum(r["units_sold"] for r in sku_rows)
        print(f"  {sku}: {len(sku_rows)} day(s), {total} units total")
