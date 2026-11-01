"""
Render a single influencer outreach to a .docx file.

Input JSON shape:
    {
      "brand_name": "...",
      "generated_at": "2026-05-22",
      "creator": {
        "handle": "@maya_brews",
        "display_name": "Maya Lin",
        "platform": "instagram",
        "follower_count": 24000,
        "tier": "micro",
        "niche": "coffee + slow living",
        "content_themes": ["coffee_brewing", "slow_mornings"],
        "voice_register": "warm_ironic_conversational",
        "relationship_stage": "new"
      },
      "pitch": {
        "pitch_type": "bundle",
        "product_or_bundle_name": "The Slow Morning Bundle",
        "value_usd": 92,
        "fit_rationale": "Bundle matches creator's morning routine content"
      },
      "framework": {
        "type": "hybrid",
        "rate_offered_usd": 400,
        "rate_range_label": "$300-500 typical for this tier",
        "expected_reach": "20,000-30,000 impressions"
      },
      "outreach": {
        "channel": "instagram_dm",
        "subject": "",
        "body": "Hi Maya — your post about brewing pour-over on the camping trip last week ..."
      },
      "follow_ups": [
        {"variant": "A", "send_after_days": 7, "body": "..."},
        {"variant": "B", "send_after_days": 14, "body": "..."},
        {"variant": "C", "send_after_days": 28, "body": "..."}
      ],
      "deliverables": {
        "items": ["1 Reel", "3 Stories with link"],
        "timing_window": "within 14-30 days of receiving product",
        "usage_rights": "organic + 30-day brand repost rights",
        "exclusivity": "none"
      },
      "disclosure": {
        "required": ["Branded Content tag", "#ad in caption"],
        "framework_specific_note": "Standard for Hybrid + Instagram"
      },
      "alignment_audit": {
        "score": 8.5,
        "notes": "Strong brand fit; competitor mention 3 weeks ago — recommend 30+ day window"
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


TIER_DISPLAY = {
    "nano": "Nano (1K-10K)",
    "micro": "Micro (10K-100K)",
    "mid_tier": "Mid-tier (100K-500K)",
    "macro": "Macro (500K+)",
}

PLATFORM_DISPLAY = {
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "youtube": "YouTube",
    "x_twitter": "X / Twitter",
    "linkedin": "LinkedIn",
    "pinterest": "Pinterest",
}

FRAMEWORK_DISPLAY = {
    "gifted_only": "Gifted Only",
    "hybrid": "Hybrid (Product + Payment)",
    "paid": "Paid Partnership",
}

STAGE_COLORS = {
    "new": RGBColor(0x1F, 0x6F, 0xB8),
    "outreached": RGBColor(0xB8, 0x86, 0x0B),
    "responded": RGBColor(0x1E, 0x7A, 0x2C),
    "agreed": RGBColor(0x1E, 0x7A, 0x2C),
    "strained": RGBColor(0xC0, 0x55, 0x00),
    "blacklisted": RGBColor(0xC0, 0x00, 0x00),
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
    creator = data.get("creator", {})
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(f"Outreach: {creator.get('handle', '?')}")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    platform = PLATFORM_DISPLAY.get(creator.get("platform", ""), creator.get("platform", ""))
    tier = TIER_DISPLAY.get(creator.get("tier", ""), creator.get("tier", ""))
    follower_count = creator.get("follower_count", 0)
    meta_run = meta_p.add_run(
        f"Platform: {platform}  ·  Tier: {tier}  ·  Followers: {follower_count:,}  ·  Generated: {data.get('generated_at', '')}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    stage = creator.get("relationship_stage", "new")
    stage_p = doc.add_paragraph()
    stage_run = stage_p.add_run(f"Relationship stage: {stage}")
    stage_run.bold = True
    if stage in STAGE_COLORS:
        stage_run.font.color.rgb = STAGE_COLORS[stage]


def _render_creator_context(doc, data: dict):
    creator = data.get("creator", {})
    _add_divider(doc)
    _add_section_header(doc, "CREATOR CONTEXT")
    if creator.get("display_name"):
        _add_kv(doc, "Display name", creator["display_name"])
    if creator.get("niche"):
        _add_kv(doc, "Niche", creator["niche"])
    themes = creator.get("content_themes", [])
    if themes:
        _add_kv(doc, "Content themes", ", ".join(themes))
    if creator.get("voice_register"):
        _add_kv(doc, "Voice register", creator["voice_register"])

    audit = data.get("alignment_audit", {})
    if audit:
        _add_kv(doc, "Brand alignment score", f"{audit.get('score', '—')}/10")
        if audit.get("notes"):
            _add_kv(doc, "Alignment notes", audit["notes"])


def _render_pitch_recommendation(doc, data: dict):
    pitch = data.get("pitch", {})
    framework = data.get("framework", {})
    _add_divider(doc)
    _add_section_header(doc, "PITCH RECOMMENDATION")
    _add_kv(doc, "Pitch type", pitch.get("pitch_type"))
    _add_kv(doc, "Product/Bundle", pitch.get("product_or_bundle_name"))
    if pitch.get("value_usd"):
        _add_kv(doc, "Pitch value (product cost)", f"${pitch['value_usd']:,.2f}")
    _add_kv(doc, "Why this fits", pitch.get("fit_rationale"))
    _add_kv(doc, "Payment framework", FRAMEWORK_DISPLAY.get(framework.get("type", ""), framework.get("type", "")))
    if framework.get("rate_offered_usd") is not None:
        _add_kv(doc, "Rate offered", f"${framework['rate_offered_usd']:,.0f}")
    if framework.get("rate_range_label"):
        _add_kv(doc, "Tier rate range", framework["rate_range_label"])
    if framework.get("expected_reach"):
        _add_kv(doc, "Expected reach", framework["expected_reach"])


def _render_outreach(doc, data: dict):
    outreach = data.get("outreach", {})
    _add_divider(doc)
    _add_section_header(doc, "INITIAL OUTREACH (paste-ready)")
    if outreach.get("subject"):
        _add_kv(doc, "Subject", outreach["subject"])
    body = outreach.get("body", "")
    word_count = len(body.split()) if body else 0
    _add_kv(doc, "Word count", f"{word_count} words")
    _add_subheader(doc, "Body")
    for para in body.split("\n\n"):
        doc.add_paragraph(para)


def _render_follow_ups(doc, data: dict):
    follow_ups = data.get("follow_ups", [])
    if not follow_ups:
        return
    _add_divider(doc)
    _add_section_header(doc, "FOLLOW-UP VARIANTS (use if no reply)")
    for fu in follow_ups:
        variant = fu.get("variant", "?")
        days = fu.get("send_after_days", "?")
        _add_subheader(doc, f"Follow-up {variant} — send {days} days after initial")
        for para in fu.get("body", "").split("\n\n"):
            doc.add_paragraph(para)


def _render_deliverables(doc, data: dict):
    deliverables = data.get("deliverables", {})
    if not deliverables:
        return
    _add_divider(doc)
    _add_section_header(doc, "SUGGESTED DELIVERABLES STRUCTURE")
    items = deliverables.get("items", [])
    for item in items:
        doc.add_paragraph(item, style="List Bullet")
    _add_kv(doc, "Timing window", deliverables.get("timing_window"))
    _add_kv(doc, "Usage rights", deliverables.get("usage_rights"))
    _add_kv(doc, "Exclusivity", deliverables.get("exclusivity"))


def _render_disclosure(doc, data: dict):
    disclosure = data.get("disclosure", {})
    if not disclosure:
        return
    _add_divider(doc)
    _add_section_header(doc, "DISCLOSURE REQUIREMENTS")
    for req in disclosure.get("required", []):
        doc.add_paragraph(req, style="List Bullet")
    if disclosure.get("framework_specific_note"):
        _add_kv(doc, "Note", disclosure["framework_specific_note"])


def _render_next_steps(doc, data: dict):
    _add_divider(doc)
    _add_section_header(doc, "NEXT STEPS")
    outreach = data.get("outreach", {})
    channel = outreach.get("channel", "DM")
    doc.add_paragraph(f"1. Send the initial outreach via {channel}.", style="List Number")
    doc.add_paragraph("2. Update influencer memory cache when reply arrives.", style="List Number")
    doc.add_paragraph("3. If no reply by the suggested follow-up date, deploy Variant A.", style="List Number")
    doc.add_paragraph("4. Track deliverables via the cache after the partnership confirms.", style="List Number")


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_header(doc, data)
    _render_creator_context(doc, data)
    _render_pitch_recommendation(doc, data)
    _render_outreach(doc, data)
    _render_follow_ups(doc, data)
    _render_deliverables(doc, data)
    _render_disclosure(doc, data)
    _render_next_steps(doc, data)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_outreach_docx.py <outreach_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
