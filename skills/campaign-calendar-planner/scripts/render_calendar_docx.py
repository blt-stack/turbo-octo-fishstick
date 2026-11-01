"""
Render the campaign calendar's per-campaign topic briefs to a .docx file.

The .docx complements the .xlsx grid (from render_calendar_xlsx.py). The
.xlsx is the operational tracker (what + when + status); the .docx is the
creative brief per campaign (topic, copy starters, channel reasoning).

Input JSON shape matches render_calendar_xlsx.py with additional per-campaign
brief fields:

    {
      "brand_name": "...",
      "region": "us" | ...,
      "calendar_window": {"start": "...", "end": "..."},
      "generated_at": "2026-05-22",
      "executive_summary": "One paragraph on what's in the calendar at a glance.",
      "campaigns": [
        {
          "campaign_name": "Mother's Day 2026",
          "campaign_type": "Holiday",
          "start_date": "2026-04-22",
          "end_date": "2026-05-12",
          "playbook": "Mother's Day campaign (21-day window)",
          "goal": "Drive 15-20% of monthly revenue through gift-shopping audience.",
          "audience": "All engaged subscribers, with extra effort for past gift buyers.",
          "topic_brief": "Two paragraphs on the angle, the brand-voice frame, the narrative...",
          "sends": [...]  # same as calendar_xlsx
          "copy_starters": {
            "email_subject_lines": ["...", "...", "..."],
            "sms_drafts": ["...", "..."],
            "paid_ad_hooks_by_archetype": {
              "problem_aware": "...",
              "social_proof": "...",
              "transformation": "...",
              "curiosity_gap": "...",
              "contrarian": "..."
            },
            "organic_post_angles": ["...", "...", "..."],
            "site_banner_options": ["...", "..."]
          }
        },
        ...
      ]
    }

Requires python-docx (pip install python-docx --break-system-packages).
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor


REGION_DISPLAY = {
    "us": "United States",
    "uk-eu": "UK / Europe",
    "canada-au-nz": "Canada / Australia / New Zealand",
    "global": "Multi-region",
}

CHANNEL_DISPLAY = {
    "email": "Email",
    "sms": "SMS",
    "paid_ad": "Paid Ad",
    "organic_social": "Organic Social",
    "site_update": "Site Update",
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


def _render_metadata(doc, data: dict):
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(f"{data.get('brand_name', 'Untitled')} — Campaign Calendar Brief")
    title_run.bold = True
    title_run.font.size = Pt(18)

    window = data.get("calendar_window", {})
    window_str = f"{window.get('start', '')} – {window.get('end', '')}"
    region_display = REGION_DISPLAY.get(data.get("region", "us"), data.get("region", "us"))
    meta_p = doc.add_paragraph()
    meta_run = meta_p.add_run(
        f"Generated {data.get('generated_at', '')}  ·  "
        f"Region: {region_display}  ·  "
        f"Window: {window_str}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    campaign_count = len(data.get("campaigns", []) or [])
    total_sends = sum(len(c.get("sends", []) or []) for c in (data.get("campaigns", []) or []))
    _add_kv(doc, "Total campaigns", str(campaign_count))
    _add_kv(doc, "Total sends across channels", str(total_sends))


def _render_executive_summary(doc, summary: str):
    if not summary:
        return
    _add_divider(doc)
    _add_section_header(doc, "EXECUTIVE SUMMARY")
    doc.add_paragraph(summary)


def _render_campaign(doc, campaign: dict, index: int):
    _add_divider(doc)
    name = campaign.get("campaign_name", "Campaign")
    start = campaign.get("start_date", "")
    end = campaign.get("end_date", "")
    _add_section_header(doc, f"CAMPAIGN {index + 1}: {name.upper()}  ({start} – {end})")

    _add_kv(doc, "Type", campaign.get("campaign_type", "Other"))
    _add_kv(doc, "Playbook", campaign.get("playbook", "—"))
    _add_kv(doc, "Goal", campaign.get("goal", "—"))
    _add_kv(doc, "Audience", campaign.get("audience", "—"))

    topic_brief = campaign.get("topic_brief")
    if topic_brief:
        _add_subheader(doc, "Topic brief")
        doc.add_paragraph(topic_brief)

    sends = campaign.get("sends", []) or []
    if sends:
        _add_subheader(doc, "Send schedule")
        table = doc.add_table(rows=1, cols=4)
        table.style = "Light Grid Accent 1"
        hdr = table.rows[0].cells
        hdr[0].text = "Date"
        hdr[1].text = "Time"
        hdr[2].text = "Channel"
        hdr[3].text = "Topic"
        for h in hdr:
            for p in h.paragraphs:
                for r in p.runs:
                    r.bold = True
        for send in sends:
            row = table.add_row().cells
            row[0].text = send.get("date", "")
            row[1].text = send.get("time", "")
            row[2].text = CHANNEL_DISPLAY.get(send.get("channel", ""), send.get("channel", ""))
            row[3].text = send.get("topic", "")

    starters = campaign.get("copy_starters", {}) or {}
    if starters:
        _add_subheader(doc, "Copy starters")

        subj = starters.get("email_subject_lines", []) or []
        if subj:
            p = doc.add_paragraph()
            p.add_run("Email subject lines:").bold = True
            for s in subj:
                doc.add_paragraph(s, style="List Bullet")

        sms = starters.get("sms_drafts", []) or []
        if sms:
            p = doc.add_paragraph()
            p.add_run("SMS drafts:").bold = True
            for s in sms:
                doc.add_paragraph(s, style="List Bullet")

        hooks = starters.get("paid_ad_hooks_by_archetype", {}) or {}
        if hooks:
            p = doc.add_paragraph()
            p.add_run("Paid ad hooks (across 5 archetypes):").bold = True
            archetype_labels = {
                "problem_aware": "Problem-aware",
                "social_proof": "Social-proof",
                "transformation": "Transformation",
                "curiosity_gap": "Curiosity-gap",
                "contrarian": "Contrarian",
            }
            for key, label in archetype_labels.items():
                if hooks.get(key):
                    p2 = doc.add_paragraph(style="List Bullet")
                    p2.add_run(f"{label}: ").bold = True
                    p2.add_run(hooks[key])

        angles = starters.get("organic_post_angles", []) or []
        if angles:
            p = doc.add_paragraph()
            p.add_run("Organic social post angles:").bold = True
            for a in angles:
                doc.add_paragraph(a, style="List Bullet")

        banner = starters.get("site_banner_options", []) or []
        if banner:
            p = doc.add_paragraph()
            p.add_run("Site banner copy options:").bold = True
            for b in banner:
                doc.add_paragraph(b, style="List Bullet")


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_metadata(doc, data)
    _render_executive_summary(doc, data.get("executive_summary", ""))

    campaigns = data.get("campaigns", []) or []
    for i, campaign in enumerate(campaigns):
        _render_campaign(doc, campaign, i)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_calendar_docx.py <calendar_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
