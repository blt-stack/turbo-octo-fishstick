"""
Render the ad creative brief to a polished .docx file.

The brief is the buyer-facing creative deliverable. Contains all 5 concepts
(one per archetype) with per-platform copy variants, image previews (when
Fal-generated), or Canva briefs (when not), plus compliance checks and
launch instructions.

Input JSON shape:
    {
      "product_name": "...",
      "brand_name": "...",
      "generated_at": "2026-05-22",
      "platforms": ["meta", "tiktok", "google"],
      "formats": ["static", "video_wrapper", "carousel", "collection"],
      "image_source": "fal_ai" | "canva_briefs" | "mixed",
      "ugc_hooks_source": "shared_cache" | "fresh",
      "keywords_source": "seo_cache" | "none",
      "concepts": [
        {
          "archetype": "Problem-aware",
          "hook": "...",
          "image": {
            "source": "fal" | "canva_brief" | "use_your_own_photo",
            "generated_paths": {"meta_1x1": "/path/to/image.png", ...},
            "canva_brief": "...",
            "notes": "..."
          },
          "platform_copy": {
            "meta": {
              "primary_text": "...",
              "headline": "...",
              "description": "...",
              "cta": "Shop Now"
            },
            "tiktok": {
              "caption": "...",
              "display_name": "...",
              "hashtags": ["...", "..."],
              "cta": "Shop Now"
            },
            "google_rsa": {
              "headlines": ["..."] * 15,
              "descriptions": ["..."] * 4,
              "path1": "...",
              "path2": "..."
            }
          }
        },
        ...  # 5 concepts
      ],
      "compliance_check": {
        "meta": {"prohibited_claims": "pass", ...},
        "tiktok": {"prohibited_claims": "pass", ...},
        "google": {"prohibited_claims": "pass", ...},
        "issues": [...]
      }
    }

Requires python-docx (pip install python-docx --break-system-packages).
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor


PLATFORM_DISPLAY = {
    "meta": "Meta (Facebook + Instagram)",
    "tiktok": "TikTok Ads",
    "google": "Google Ads",
    "google_rsa": "Google Search (RSA)",
    "google_shopping": "Google Shopping",
    "google_pmax": "Google Performance Max",
}

PLATFORM_FIELD_LIMITS = {
    "meta": {"primary_text": 125, "headline": 27, "description": 27},
    "tiktok": {"caption": 100, "display_name": 24},
    "google_rsa": {"headlines_each": 30, "descriptions_each": 90},
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


def _add_kv(doc, label: str, value: str):
    p = doc.add_paragraph()
    label_run = p.add_run(f"{label}: ")
    label_run.bold = True
    p.add_run(value or "—")


def _add_field_with_count(doc, label: str, text: str, limit: int):
    p = doc.add_paragraph()
    label_run = p.add_run(f"{label} ")
    label_run.bold = True
    count_run = p.add_run(f"({len(text)}/{limit})")
    count_run.italic = True
    if len(text) > limit:
        count_run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
    doc.add_paragraph(text)


def _render_metadata(doc, data: dict):
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(f"{data.get('product_name', 'Untitled')} — Paid Ad Creative Brief")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    platforms_str = ", ".join(PLATFORM_DISPLAY.get(p, p) for p in data.get("platforms", []) or [])
    formats_str = ", ".join(data.get("formats", []) or [])
    meta_run = meta_p.add_run(
        f"Generated {data.get('generated_at', '')}  ·  "
        f"Brand: {data.get('brand_name', '')}  ·  "
        f"Platforms: {platforms_str}  ·  "
        f"Formats: {formats_str}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    _add_kv(doc, "Image source", data.get("image_source", "unknown"))
    _add_kv(doc, "UGC hooks source", data.get("ugc_hooks_source", "fresh"))
    _add_kv(doc, "Keywords source", data.get("keywords_source", "none"))


def _render_concept_image(doc, image: dict):
    src = image.get("source", "unknown")
    if src == "fal":
        generated_paths = image.get("generated_paths", {}) or {}
        # Show the first available generated image inline
        for label, path_str in generated_paths.items():
            path = Path(path_str)
            if path.exists():
                _add_subheader(doc, f"Generated image ({label})")
                try:
                    doc.add_picture(str(path), width=Inches(4.5))
                except Exception as exc:
                    doc.add_paragraph(f"[Could not embed: {exc}]")
                    doc.add_paragraph(f"Image at: {path}")
                break
    elif src == "canva_brief":
        _add_subheader(doc, "Canva brief")
        doc.add_paragraph(image.get("canva_brief", ""))
    elif src == "use_your_own_photo":
        _add_subheader(doc, "Use your own photo")
        doc.add_paragraph(image.get("notes", ""))


def _render_meta_copy(doc, meta_copy: dict):
    if not meta_copy:
        return
    _add_subheader(doc, "Meta (Facebook + Instagram)")
    limits = PLATFORM_FIELD_LIMITS["meta"]
    _add_field_with_count(doc, "Primary text", meta_copy.get("primary_text", ""), limits["primary_text"])
    _add_field_with_count(doc, "Headline", meta_copy.get("headline", ""), limits["headline"])
    _add_field_with_count(doc, "Description", meta_copy.get("description", ""), limits["description"])
    _add_kv(doc, "CTA", meta_copy.get("cta", "Shop Now"))


def _render_tiktok_copy(doc, tt_copy: dict):
    if not tt_copy:
        return
    _add_subheader(doc, "TikTok Ads")
    limits = PLATFORM_FIELD_LIMITS["tiktok"]
    _add_field_with_count(doc, "Caption", tt_copy.get("caption", ""), limits["caption"])
    _add_field_with_count(doc, "Display name", tt_copy.get("display_name", ""), limits["display_name"])
    hashtags = tt_copy.get("hashtags", []) or []
    if hashtags:
        _add_kv(doc, "Hashtags", " ".join(hashtags))
    _add_kv(doc, "CTA", tt_copy.get("cta", "Shop Now"))


def _render_google_rsa(doc, rsa: dict):
    if not rsa:
        return
    _add_subheader(doc, "Google Search (Responsive Search Ad)")
    headlines = rsa.get("headlines", []) or []
    descriptions = rsa.get("descriptions", []) or []
    _add_kv(doc, "Total headlines", str(len(headlines)))
    for i, h in enumerate(headlines, 1):
        _add_field_with_count(doc, f"H{i}", h, 30)
    _add_kv(doc, "Total descriptions", str(len(descriptions)))
    for i, d in enumerate(descriptions, 1):
        _add_field_with_count(doc, f"D{i}", d, 90)
    _add_kv(doc, "Path 1", rsa.get("path1", ""))
    _add_kv(doc, "Path 2", rsa.get("path2", ""))


def _render_concept(doc, concept: dict, index: int):
    _add_divider(doc)
    archetype = concept.get("archetype", "Concept")
    _add_section_header(doc, f"CONCEPT {index + 1} — {archetype}")

    hook = concept.get("hook", "")
    if hook:
        p = doc.add_paragraph()
        p.add_run("Hook: ").bold = True
        p.add_run(hook)

    image = concept.get("image", {})
    if image:
        _render_concept_image(doc, image)

    platform_copy = concept.get("platform_copy", {})
    if "meta" in platform_copy:
        _render_meta_copy(doc, platform_copy["meta"])
    if "tiktok" in platform_copy:
        _render_tiktok_copy(doc, platform_copy["tiktok"])
    if "google_rsa" in platform_copy:
        _render_google_rsa(doc, platform_copy["google_rsa"])


def _render_compliance_check(doc, check: dict):
    if not check:
        return
    _add_divider(doc)
    _add_section_header(doc, "COMPLIANCE CHECK")

    for platform in ("meta", "tiktok", "google"):
        platform_check = check.get(platform)
        if not platform_check:
            continue
        _add_subheader(doc, PLATFORM_DISPLAY.get(platform, platform))
        for key, status in platform_check.items():
            glyph = "✓" if status == "pass" else "✗" if status == "fail" else "?"
            label = key.replace("_", " ").title()
            p = doc.add_paragraph()
            p.add_run(f"{glyph} {label}: ").bold = (status == "fail")
            run = p.add_run(str(status))
            if status == "fail":
                run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    issues = check.get("issues", []) or []
    if issues:
        _add_subheader(doc, "Issues found (fix before uploading):")
        for issue in issues:
            p = doc.add_paragraph(issue, style="List Bullet")
            for r in p.runs:
                r.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)


def _render_launch_instructions(doc, platforms: list[str]):
    _add_divider(doc)
    _add_section_header(doc, "HOW TO LAUNCH")
    if "meta" in platforms:
        doc.add_paragraph("Meta Ads Manager:", style="List Bullet")
        doc.add_paragraph("1. Open Ads Manager → Create new campaign or ad set.")
        doc.add_paragraph("2. Use Bulk Import → upload the meta-ads CSV produced by this skill.")
        doc.add_paragraph("3. Match the rows to your campaign/ad set IDs as prompted.")
        doc.add_paragraph("4. Upload the generated images (or your Canva-built images) when prompted.")
    if "tiktok" in platforms:
        doc.add_paragraph("TikTok Ads Manager:", style="List Bullet")
        doc.add_paragraph("1. TikTok Business Center → Ads Manager → Bulk Tools.")
        doc.add_paragraph("2. Upload the tiktok-ads CSV produced by this skill.")
        doc.add_paragraph("3. Upload videos (or set up Spark Ad authorization with the creator).")
    if "google" in platforms:
        doc.add_paragraph("Google Ads Editor:", style="List Bullet")
        doc.add_paragraph("1. Open Google Ads Editor (desktop app).")
        doc.add_paragraph("2. Account → Import → CSV → upload the google-ads CSV produced by this skill.")
        doc.add_paragraph("3. Review imported entries → Post Changes.")


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_metadata(doc, data)

    concepts = data.get("concepts", []) or []
    for i, concept in enumerate(concepts):
        _render_concept(doc, concept, i)

    _render_compliance_check(doc, data.get("compliance_check", {}))
    _render_launch_instructions(doc, data.get("platforms", []) or [])

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_brief_docx.py <brief_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
