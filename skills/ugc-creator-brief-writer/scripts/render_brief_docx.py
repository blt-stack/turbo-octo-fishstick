"""
Render a UGC creator brief to a polished .docx file.

Handles both single-brief mode and per-creator briefs in campaign mode (same
function — campaign mode just calls this once per creator with the per-creator
hook subset and personalized intro).

Input JSON shape:
    {
      "brief_type": "organic | paid | affiliate",
      "platforms": ["tiktok", "reels", "stories", "shorts"],
      "product_name": "...",
      "brand_name": "...",
      "creator_name": "...",        # optional — only in per-creator briefs
      "campaign_name": "...",       # optional — only in campaign-mode briefs
      "personalized_intro": "...",  # optional — only in per-creator briefs
      "generated_at": "2026-05-22",
      "project_title": "...",
      "the_ask": "...",
      "product_context": "...",
      "audience": "...",
      "tone_of_voice": "...",
      "hooks": [
        {
          "number": 1,
          "archetype": "Problem-aware",
          "spoken_line": "...",
          "on_screen_text": "...",
          "creator_notes": "..."
        },
        ...  # 2-3 in per-creator briefs, 10 in master/single briefs
      ],
      "b_roll_shots": [
        {"number": 1, "description": "...", "why_it_matters": "...", "reference": "..."},
        ...
      ],
      "talking_points": ["...", "...", "..."],
      "dos": ["...", "..."],
      "donts": ["...", "..."],
      "deliverables": {
        "video_count": 1,
        "per_platform": [
          {"platform": "tiktok", "duration_seconds": 30, "aspect_ratio": "9:16"},
          ...
        ]
      },
      "timeline": {
        "shoot_deadline": "2026-05-26",
        "deliver_deadline": "2026-05-28",
        "delivery_method": "Frame.io link to be shared"
      },
      "ftc_disclosure": "...",          # required for paid + affiliate
      "usage_rights": "...",            # required for paid
      "brand_safety": [...],            # list of bullets, required for paid
      "affiliate_details": {            # required for affiliate
        "tracked_link": "...",
        "discount_code": "...",
        "commission_pct": 15,
        "on_screen_requirements": "..."
      }
    }

Requires python-docx (pip install python-docx --break-system-packages).
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor


BRIEF_TYPE_DISPLAY = {
    "organic": "Organic UGC",
    "paid": "Paid UGC (Spark Ads / Whitelisted)",
    "affiliate": "Affiliate / Commission",
}

PLATFORM_DISPLAY = {
    "tiktok": "TikTok",
    "reels": "Instagram Reels",
    "stories": "Instagram Stories",
    "shorts": "YouTube Shorts",
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


def _render_title_block(doc, data: dict):
    project_title = data.get("project_title") or f"UGC Brief — {data.get('product_name', 'Untitled')}"
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(project_title)
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    brief_type = BRIEF_TYPE_DISPLAY.get(data.get("brief_type", "organic"), data.get("brief_type", ""))
    platforms_str = ", ".join(PLATFORM_DISPLAY.get(p, p) for p in data.get("platforms", []) or [])
    meta_run = meta_p.add_run(
        f"Generated {data.get('generated_at', '')}  ·  "
        f"Brand: {data.get('brand_name', '')}  ·  "
        f"Brief type: {brief_type}  ·  "
        f"Platforms: {platforms_str}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    if data.get("creator_name"):
        _add_kv(doc, "For creator", data["creator_name"])
    if data.get("campaign_name"):
        _add_kv(doc, "Campaign", data["campaign_name"])


def _render_personalized_intro(doc, intro: str):
    if not intro:
        return
    _add_divider(doc)
    doc.add_paragraph(intro)


def _render_overview(doc, data: dict):
    _add_divider(doc)
    _add_section_header(doc, "OVERVIEW")
    _add_subheader(doc, "The ask")
    doc.add_paragraph(data.get("the_ask", "—"))
    _add_subheader(doc, "Product context")
    doc.add_paragraph(data.get("product_context", "—"))
    _add_subheader(doc, "Who this is for")
    doc.add_paragraph(data.get("audience", "—"))
    _add_subheader(doc, "Tone of voice")
    doc.add_paragraph(data.get("tone_of_voice", "—"))


def _render_hooks(doc, hooks: list[dict]):
    if not hooks:
        return
    _add_divider(doc)
    _add_section_header(doc, f"HOOKS ({len(hooks)} options across angle archetypes)")
    table = doc.add_table(rows=1, cols=5)
    table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    hdr[0].text = "#"
    hdr[1].text = "Archetype"
    hdr[2].text = "Spoken line"
    hdr[3].text = "On-screen text"
    hdr[4].text = "Notes for creator"
    for h in hdr:
        for p in h.paragraphs:
            for r in p.runs:
                r.bold = True
    for hook in hooks:
        row = table.add_row().cells
        row[0].text = str(hook.get("number", ""))
        row[1].text = hook.get("archetype", "")
        row[2].text = hook.get("spoken_line", "")
        row[3].text = hook.get("on_screen_text", "")
        row[4].text = hook.get("creator_notes", "")


def _render_b_roll(doc, shots: list[dict]):
    if not shots:
        return
    _add_divider(doc)
    _add_section_header(doc, f"B-ROLL SHOT LIST ({len(shots)} shots)")
    for shot in shots:
        _add_subheader(doc, f"Shot {shot.get('number', '?')}")
        doc.add_paragraph(shot.get("description", ""))
        why = shot.get("why_it_matters")
        if why:
            p = doc.add_paragraph()
            p.add_run("Why it matters: ").italic = True
            p.add_run(why)
        ref = shot.get("reference")
        if ref:
            p = doc.add_paragraph()
            p.add_run("Reference: ").italic = True
            p.add_run(ref)


def _render_talking_points(doc, points: list[str]):
    if not points:
        return
    _add_divider(doc)
    _add_section_header(doc, "TALKING POINTS")
    doc.add_paragraph("Mention these naturally — not a script, just things to weave in:")
    for point in points:
        doc.add_paragraph(point, style="List Bullet")


def _render_dos_donts(doc, dos: list[str], donts: list[str]):
    if not dos and not donts:
        return
    _add_divider(doc)
    _add_section_header(doc, "DO'S AND DON'TS")
    if dos:
        _add_subheader(doc, "Do")
        for item in dos:
            doc.add_paragraph(item, style="List Bullet")
    if donts:
        _add_subheader(doc, "Don't")
        for item in donts:
            doc.add_paragraph(item, style="List Bullet")


def _render_deliverables(doc, deliverables: dict):
    if not deliverables:
        return
    _add_divider(doc)
    _add_section_header(doc, "DELIVERABLES")
    count = deliverables.get("video_count", 1)
    _add_kv(doc, "Total videos", str(count))
    per_platform = deliverables.get("per_platform", []) or []
    if per_platform:
        _add_subheader(doc, "Per platform")
        for spec in per_platform:
            platform = PLATFORM_DISPLAY.get(spec.get("platform", ""), spec.get("platform", ""))
            line = f"{platform}: {spec.get('duration_seconds', '?')}s, {spec.get('aspect_ratio', '9:16')}"
            doc.add_paragraph(line, style="List Bullet")


def _render_timeline(doc, timeline: dict):
    if not timeline:
        return
    _add_divider(doc)
    _add_section_header(doc, "TIMELINE")
    _add_kv(doc, "Shoot by", timeline.get("shoot_deadline", "—"))
    _add_kv(doc, "Deliver by", timeline.get("deliver_deadline", "—"))
    _add_kv(doc, "How to deliver", timeline.get("delivery_method", "Frame.io / Dropbox / WeTransfer link"))


def _render_compliance(doc, data: dict):
    brief_type = data.get("brief_type", "organic")
    if brief_type not in ("paid", "affiliate"):
        return

    _add_divider(doc)
    _add_section_header(doc, "DISCLOSURE & RIGHTS")

    ftc = data.get("ftc_disclosure")
    if ftc:
        _add_subheader(doc, "FTC disclosure")
        doc.add_paragraph(ftc)

    rights = data.get("usage_rights")
    if rights and brief_type == "paid":
        _add_subheader(doc, "Usage rights")
        doc.add_paragraph(rights)

    affiliate = data.get("affiliate_details")
    if affiliate and brief_type == "affiliate":
        _add_subheader(doc, "Affiliate details")
        _add_kv(doc, "Tracked link", affiliate.get("tracked_link", "—"))
        _add_kv(doc, "Discount code", affiliate.get("discount_code", "—"))
        pct = affiliate.get("commission_pct")
        if pct is not None:
            _add_kv(doc, "Commission", f"{pct}%")
        on_screen = affiliate.get("on_screen_requirements")
        if on_screen:
            _add_kv(doc, "On-screen requirements", on_screen)

    safety = data.get("brand_safety", []) or []
    if safety and brief_type == "paid":
        _add_subheader(doc, "Brand safety — please avoid")
        for item in safety:
            doc.add_paragraph(item, style="List Bullet")


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_title_block(doc, data)
    _render_personalized_intro(doc, data.get("personalized_intro", ""))
    _render_overview(doc, data)
    _render_hooks(doc, data.get("hooks", []) or [])
    _render_b_roll(doc, data.get("b_roll_shots", []) or [])
    _render_talking_points(doc, data.get("talking_points", []) or [])
    _render_dos_donts(doc, data.get("dos", []) or [], data.get("donts", []) or [])
    _render_deliverables(doc, data.get("deliverables", {}) or {})
    _render_timeline(doc, data.get("timeline", {}) or {})
    _render_compliance(doc, data)

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
