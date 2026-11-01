"""
Render per-platform CSV files for bulk upload to Meta Ads Manager,
TikTok Ads Manager, and Google Ads Editor.

Each platform has a different column schema. The skill writes one CSV per
platform when that platform is in scope for the run. Buyers paste each
CSV into the corresponding Ads Manager bulk-upload screen.

Time savings: 30-45 minutes of manual data entry per campaign.

Input JSON shape is the same as render_brief_docx.py — this script just
renders the platform_copy sections of each concept as a CSV row.

Output: writes one CSV per platform passed via the `platforms` field.
File naming: {output_dir}/{slug}_{platform}-ads_{date}.csv
"""

import csv
import json
import sys
from datetime import datetime
from pathlib import Path


# Column schemas per platform. These match what the platforms' bulk-upload
# tools accept. They may evolve over time — the schemas here reflect 2026
# conventions as understood at skill generation time.

META_COLUMNS = [
    "Ad Set Name",
    "Ad Name",
    "Body",                # primary text (125 char limit)
    "Title",               # headline (27 char limit)
    "Link Description",    # description (27 char limit)
    "Call to Action",
    "Display Link",
    "Creative Image File",
    "Concept Angle",       # custom column for buyer tracking
]

TIKTOK_COLUMNS = [
    "Campaign Name",
    "Ad Group Name",
    "Ad Name",
    "Ad Text",             # caption (100 char limit)
    "Display Name",        # 24 char limit
    "CTA Button",
    "Hashtags",
    "Video File",
    "Landing Page URL",
    "Concept Angle",
]

# Google Ads Editor expects RSAs in this format (one row per RSA ad).
# Headlines and descriptions get listed in numbered columns.
GOOGLE_RSA_COLUMNS = [
    "Campaign",
    "Ad group",
    "Ad type",
    *[f"Headline {i}" for i in range(1, 16)],   # 15 headline slots
    *[f"Description {i}" for i in range(1, 5)], # 4 description slots
    "Path 1",
    "Path 2",
    "Final URL",
    "Concept Angle",
]


def slugify(text: str, max_len: int = 60) -> str:
    out = text.lower().strip()
    out = "".join(c if c.isalnum() else "-" for c in out)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")[:max_len] or "untitled"


def _meta_rows(data: dict, slug: str) -> list[dict]:
    rows: list[dict] = []
    final_url = data.get("destination_url", "")
    display_link = data.get("display_link", "")
    concepts = data.get("concepts", []) or []
    for i, concept in enumerate(concepts, 1):
        meta_copy = (concept.get("platform_copy") or {}).get("meta", {})
        if not meta_copy:
            continue
        archetype = concept.get("archetype", f"Concept {i}")
        ad_set_name = f"{slug}_{slugify(archetype)}"
        ad_name = f"{ad_set_name}_v1"
        # Reference to the image file (relative to wherever the CSV gets uploaded)
        img_paths = (concept.get("image") or {}).get("generated_paths") or {}
        creative_file = img_paths.get("meta_1x1") or img_paths.get("meta_4x5") or "REPLACE_WITH_YOUR_IMAGE"
        creative_file_name = Path(creative_file).name if creative_file != "REPLACE_WITH_YOUR_IMAGE" else creative_file
        rows.append({
            "Ad Set Name": ad_set_name,
            "Ad Name": ad_name,
            "Body": meta_copy.get("primary_text", ""),
            "Title": meta_copy.get("headline", ""),
            "Link Description": meta_copy.get("description", ""),
            "Call to Action": meta_copy.get("cta", "Shop Now"),
            "Display Link": display_link,
            "Creative Image File": creative_file_name,
            "Concept Angle": archetype,
        })
    return rows


def _tiktok_rows(data: dict, slug: str) -> list[dict]:
    rows: list[dict] = []
    final_url = data.get("destination_url", "")
    concepts = data.get("concepts", []) or []
    for i, concept in enumerate(concepts, 1):
        tt_copy = (concept.get("platform_copy") or {}).get("tiktok", {})
        if not tt_copy:
            continue
        archetype = concept.get("archetype", f"Concept {i}")
        campaign_name = f"{slug}_campaign"
        ad_group_name = f"{slug}_{slugify(archetype)}_group"
        ad_name = f"{slug}_{slugify(archetype)}_v1"
        hashtags = " ".join(tt_copy.get("hashtags", []) or [])
        rows.append({
            "Campaign Name": campaign_name,
            "Ad Group Name": ad_group_name,
            "Ad Name": ad_name,
            "Ad Text": tt_copy.get("caption", ""),
            "Display Name": tt_copy.get("display_name", ""),
            "CTA Button": tt_copy.get("cta", "Shop Now"),
            "Hashtags": hashtags,
            "Video File": "REPLACE_WITH_VIDEO_PATH",
            "Landing Page URL": final_url,
            "Concept Angle": archetype,
        })
    return rows


def _google_rsa_rows(data: dict, slug: str) -> list[dict]:
    rows: list[dict] = []
    final_url = data.get("destination_url", "")
    concepts = data.get("concepts", []) or []
    for i, concept in enumerate(concepts, 1):
        rsa = (concept.get("platform_copy") or {}).get("google_rsa", {})
        if not rsa:
            continue
        archetype = concept.get("archetype", f"Concept {i}")
        campaign = f"{slug}_search_campaign"
        ad_group = f"{slug}_{slugify(archetype)}_adgroup"
        headlines = rsa.get("headlines", []) or []
        descriptions = rsa.get("descriptions", []) or []
        row: dict[str, str] = {
            "Campaign": campaign,
            "Ad group": ad_group,
            "Ad type": "Responsive search ad",
            "Path 1": rsa.get("path1", ""),
            "Path 2": rsa.get("path2", ""),
            "Final URL": final_url,
            "Concept Angle": archetype,
        }
        for h_i in range(1, 16):
            row[f"Headline {h_i}"] = headlines[h_i - 1] if len(headlines) >= h_i else ""
        for d_i in range(1, 5):
            row[f"Description {d_i}"] = descriptions[d_i - 1] if len(descriptions) >= d_i else ""
        rows.append(row)
    return rows


def _write_csv(rows: list[dict], columns: list[str], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return output_path


def render(data: dict, output_dir: Path) -> dict[str, Path]:
    """
    Returns a dict mapping platform -> file path. Only platforms that were
    requested AND have content get a file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    platforms = data.get("platforms", []) or []
    product_name = data.get("product_name", "untitled")
    slug = slugify(product_name)
    date_str = data.get("generated_at") or datetime.utcnow().strftime("%Y-%m-%d")
    results: dict[str, Path] = {}

    if "meta" in platforms:
        meta_rows = _meta_rows(data, slug)
        if meta_rows:
            out = output_dir / f"{slug}_meta-ads_{date_str}.csv"
            _write_csv(meta_rows, META_COLUMNS, out)
            results["meta"] = out

    if "tiktok" in platforms:
        tt_rows = _tiktok_rows(data, slug)
        if tt_rows:
            out = output_dir / f"{slug}_tiktok-ads_{date_str}.csv"
            _write_csv(tt_rows, TIKTOK_COLUMNS, out)
            results["tiktok"] = out

    if "google" in platforms:
        google_rows = _google_rsa_rows(data, slug)
        if google_rows:
            out = output_dir / f"{slug}_google-ads_{date_str}.csv"
            _write_csv(google_rows, GOOGLE_RSA_COLUMNS, out)
            results["google"] = out

    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_ads_csv.py <brief_json> <output_dir>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    written = render(data, Path(sys.argv[2]))
    if not written:
        print("No CSVs written — no matching platform copy in input.")
        sys.exit(0)
    for platform, path in written.items():
        print(f"{platform}: {path}")
