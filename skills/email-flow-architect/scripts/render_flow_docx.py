"""
Render the email flow program brief to a polished .docx file.

The .docx covers the full program — all flows being built in this run, all
their steps (email + SMS), timing, segmentation, and A/B test plans. The
companion Klaviyo paste-ready .txt files are produced by
render_klaviyo_blocks.py.

Input JSON shape:
    {
      "brand_name": "...",
      "generated_at": "2026-05-22",
      "flows_built": ["welcome", "abandoned_cart", "post_purchase"],
      "channels": ["email", "sms"],
      "total_emails": 12,
      "total_sms": 6,
      "keywords_source": "seo_cache" | "none",
      "ugc_hooks_source": "shared_cache" | "none",
      "deliverability_check": {
        "dkim_recommended": true,
        "spf_recommended": true,
        "dmarc_recommended": true,
        "sms_opt_in_setup_recommended": true,
        "issues": []
      },
      "flows": [
        {
          "flow_name": "welcome",
          "display_name": "Welcome Flow",
          "trigger": "Subscribed to newsletter",
          "total_duration": "14 days",
          "total_emails": 5,
          "total_sms": 2,
          "steps": [
            {
              "step_number": 1,
              "timing": "Immediate (within 1 min of signup)",
              "channel": "email",
              "purpose": "Welcome + brand intro + offer",
              "segment": "All new subscribers",
              "subject_line": "...",
              "subject_line_chars": 42,
              "preview_text": "...",
              "preview_text_chars": 58,
              "body_html_summary": "Personal opener, offer delivery, brand context, CTA, sign-off",
              "body_full_text": "Hi {{ first_name|default:'there' }}, ...",
              "merge_tags": ["first_name"],
              "ab_test": "Subject line A/B — brand-voice vs offer-led"
            },
            {
              "step_number": 2,
              "timing": "3 hours after signup",
              "channel": "sms",
              "purpose": "Mobile reminder of the offer",
              "segment": "Subscribers opted into SMS",
              "sms_body": "Hey [first name], your welcome code is WELCOME10 for 10% off...",
              "sms_chars": 140,
              "merge_tags": ["first_name"],
              "compliance": {
                "reply_stop_present": true,
                "brand_id_in_first_30": true
              }
            }
          ]
        }
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
    if limit:
        count_run = p.add_run(f"({len(text)}/{limit})")
        count_run.italic = True
        if len(text) > limit:
            count_run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
    doc.add_paragraph(text)


def _render_metadata(doc, data: dict):
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(f"{data.get('brand_name', 'Untitled')} — Email Flow Program Brief")
    title_run.bold = True
    title_run.font.size = Pt(18)

    flows_str = ", ".join(data.get("flows_built", []) or [])
    channels_str = ", ".join(data.get("channels", []) or [])
    meta_p = doc.add_paragraph()
    meta_run = meta_p.add_run(
        f"Generated {data.get('generated_at', '')}  ·  "
        f"Flows: {flows_str}  ·  "
        f"Channels: {channels_str}"
    )
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    total_emails = data.get("total_emails", 0)
    total_sms = data.get("total_sms", 0)
    _add_kv(doc, "Total assets", f"{total_emails} emails + {total_sms} SMS")
    _add_kv(doc, "Keywords source", data.get("keywords_source", "none"))
    _add_kv(doc, "UGC hooks source", data.get("ugc_hooks_source", "none"))


def _render_deliverability_check(doc, check: dict):
    if not check:
        return
    _add_divider(doc)
    _add_section_header(doc, "DELIVERABILITY CHECK")

    items = [
        ("DKIM record at sending domain", check.get("dkim_recommended", True)),
        ("SPF record updated for Klaviyo", check.get("spf_recommended", True)),
        ("DMARC record set (p=none or stricter)", check.get("dmarc_recommended", True)),
        ("Custom sender domain configured in Klaviyo", check.get("custom_sender_recommended", True)),
        ("SMS opt-in collection mechanism in place", check.get("sms_opt_in_setup_recommended", True)),
    ]
    for label, present in items:
        glyph = "☐" if present else "—"
        doc.add_paragraph(f"{glyph} {label}")

    issues = check.get("issues", []) or []
    if issues:
        _add_subheader(doc, "Issues found (verify before activating flows):")
        for issue in issues:
            p = doc.add_paragraph(issue, style="List Bullet")
            for r in p.runs:
                r.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)


def _render_step(doc, step: dict):
    step_num = step.get("step_number", "?")
    channel = step.get("channel", "email")
    timing = step.get("timing", "—")
    purpose = step.get("purpose", "")
    segment = step.get("segment", "All subscribers in flow")

    _add_subheader(doc, f"Step {step_num} ({timing}, {channel}): {purpose}")

    p = doc.add_paragraph()
    p.add_run("Segment: ").italic = True
    seg_run = p.add_run(segment)
    seg_run.italic = True
    seg_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    if channel == "email":
        subject = step.get("subject_line", "")
        preview = step.get("preview_text", "")
        body_summary = step.get("body_html_summary", "")
        _add_field_with_count(doc, "Subject line", subject, 60)
        _add_field_with_count(doc, "Preview text", preview, 90)
        if body_summary:
            p = doc.add_paragraph()
            p.add_run("Body summary: ").bold = True
            p.add_run(body_summary)
        # Full body
        body_full = step.get("body_full_text", "")
        if body_full:
            p = doc.add_paragraph()
            p.add_run("Body (full):").bold = True
            doc.add_paragraph(body_full)
    else:  # sms
        sms_body = step.get("sms_body", "")
        _add_field_with_count(doc, "SMS body", sms_body, 160)
        compliance = step.get("compliance", {})
        if compliance:
            p = doc.add_paragraph()
            p.add_run("Compliance: ").bold = True
            checks = [
                ("Reply STOP present", compliance.get("reply_stop_present", False)),
                ("Brand identifier in first 30 chars", compliance.get("brand_id_in_first_30", False)),
            ]
            for label, ok in checks:
                glyph = "✓" if ok else "✗"
                doc.add_paragraph(f"  {glyph} {label}")

    merge_tags = step.get("merge_tags", []) or []
    if merge_tags:
        _add_kv(doc, "Merge tags used", ", ".join(merge_tags))

    ab_test = step.get("ab_test")
    if ab_test:
        _add_kv(doc, "A/B test", ab_test)


def _render_flow(doc, flow: dict, index: int):
    _add_divider(doc)
    display_name = flow.get("display_name", flow.get("flow_name", "Flow"))
    _add_section_header(doc, f"FLOW {index + 1}: {display_name.upper()}")

    _add_kv(doc, "Trigger", flow.get("trigger", "—"))
    _add_kv(doc, "Total duration", flow.get("total_duration", "—"))
    _add_kv(doc, "Total emails", str(flow.get("total_emails", 0)))
    _add_kv(doc, "Total SMS", str(flow.get("total_sms", 0)))

    steps = flow.get("steps", []) or []
    for step in steps:
        _render_step(doc, step)


def _render_how_to_build(doc):
    _add_divider(doc)
    _add_section_header(doc, "HOW TO BUILD IN KLAVIYO")
    steps = [
        "Open Klaviyo → Flows → Create Flow.",
        "Name the flow after the flow_name (e.g., 'Welcome — Newsletter Signup').",
        "Set the trigger per the Trigger field above (e.g., 'Added to list: Newsletter Subscribers').",
        "For each step in the flow, add an Email or SMS action with the timing specified.",
        "Open the matching .txt file from the klaviyo_blocks/ folder produced by this skill.",
        "Copy Subject Line + Preview Text + Body sections into the corresponding Klaviyo fields.",
        "Verify merge tags render as colored chips in Klaviyo's editor.",
        "Set up the A/B test if recommended.",
        "Apply the segment filter from the step's Segment description.",
        "Repeat for each step. Activate the flow when all steps are configured.",
    ]
    for i, step in enumerate(steps, 1):
        doc.add_paragraph(f"{i}. {step}", style="List Number")


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_metadata(doc, data)
    _render_deliverability_check(doc, data.get("deliverability_check", {}))

    flows = data.get("flows", []) or []
    for i, flow in enumerate(flows):
        _render_flow(doc, flow, i)

    _render_how_to_build(doc)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_flow_docx.py <brief_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
