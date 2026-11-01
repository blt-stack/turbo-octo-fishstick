"""
Render Klaviyo-paste-ready .txt files — one per email step + one per SMS step,
across all flows being built in this run.

These are plain-text files structured exactly the way Klaviyo's email + SMS
builders expect, so the buyer pastes one file's contents into Klaviyo and is
done. Saves 60-90 minutes per flow vs rebuilding from scratch.

Input JSON shape is the same as render_flow_docx.py.

Output structure:
    {output_dir}/klaviyo_blocks/
    ├── welcome_01_email.txt
    ├── welcome_02_email.txt
    ├── welcome_sms_01.txt
    ├── ...

Each .txt file follows the format defined in templates/klaviyo-paste-conventions.md.
"""

import json
import sys
from pathlib import Path


EMAIL_BLOCK_TEMPLATE = """=== KLAVIYO EMAIL BLOCK ===
Flow: {flow_display_name}
Step: {step_number} of {total_steps_in_flow}
Send timing: {timing}
Segment: {segment}

=== SUBJECT LINE ===
{subject_line}

=== PREVIEW TEXT ===
{preview_text}

=== BODY (HTML) ===
{body_html}

=== BODY (PLAIN TEXT FALLBACK) ===
{body_plain}

=== KLAVIYO MERGE TAGS USED ===
{merge_tags}

=== A/B TEST RECOMMENDATIONS ===
{ab_test}
"""

SMS_BLOCK_TEMPLATE = """=== KLAVIYO SMS BLOCK ===
Flow: {flow_display_name}
Step: {step_number} of {total_steps_in_flow}
Send timing: {timing}
Segment: {segment}
Quiet hours: respected (8am-9pm recipient local time)

=== SMS BODY ({chars}/160 chars) ===
{sms_body}

=== LINK ===
{link}

=== KLAVIYO MERGE TAGS USED ===
{merge_tags}

=== COMPLIANCE NOTES ===
- Reply STOP language present: {reply_stop}
- Brand identifier in first 30 chars: {brand_id}
"""


def _slugify_for_filename(text: str) -> str:
    text = text.lower().strip()
    out = "".join(c if c.isalnum() else "_" for c in text)
    while "__" in out:
        out = out.replace("__", "_")
    return out.strip("_")


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _render_email_step(flow: dict, step: dict) -> str:
    flow_display_name = flow.get("display_name", flow.get("flow_name", "Flow"))
    total_steps = len(flow.get("steps", []) or [])
    merge_tags = step.get("merge_tags", []) or []
    merge_tags_str = ", ".join(merge_tags) if merge_tags else "(none)"
    body_html = step.get("body_html", step.get("body_full_text", "(body not provided)"))
    body_plain = step.get("body_plain_text", "(plain text fallback not provided)")
    return EMAIL_BLOCK_TEMPLATE.format(
        flow_display_name=flow_display_name,
        step_number=step.get("step_number", "?"),
        total_steps_in_flow=total_steps,
        timing=step.get("timing", "—"),
        segment=step.get("segment", "All subscribers in flow"),
        subject_line=step.get("subject_line", ""),
        preview_text=step.get("preview_text", ""),
        body_html=body_html,
        body_plain=body_plain,
        merge_tags=merge_tags_str,
        ab_test=step.get("ab_test", "(no specific test recommended for this step)"),
    )


def _render_sms_step(flow: dict, step: dict) -> str:
    flow_display_name = flow.get("display_name", flow.get("flow_name", "Flow"))
    total_steps = len(flow.get("steps", []) or [])
    merge_tags = step.get("merge_tags", []) or []
    merge_tags_str = ", ".join(merge_tags) if merge_tags else "(none)"
    sms_body = step.get("sms_body", "")
    compliance = step.get("compliance", {}) or {}
    return SMS_BLOCK_TEMPLATE.format(
        flow_display_name=flow_display_name,
        step_number=step.get("step_number", "?"),
        total_steps_in_flow=total_steps,
        timing=step.get("timing", "—"),
        segment=step.get("segment", "SMS-opted-in subscribers"),
        chars=len(sms_body),
        sms_body=sms_body,
        link=step.get("link", "(no link)"),
        merge_tags=merge_tags_str,
        reply_stop=_yes_no(compliance.get("reply_stop_present", False)),
        brand_id=_yes_no(compliance.get("brand_id_in_first_30", False)),
    )


def render(data: dict, output_dir: Path) -> dict[str, list[Path]]:
    """
    Returns dict mapping flow_name to list of file paths written for that flow.
    """
    output_dir = Path(output_dir)
    blocks_dir = output_dir / "klaviyo_blocks"
    blocks_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, list[Path]] = {}
    flows = data.get("flows", []) or []

    for flow in flows:
        flow_name = _slugify_for_filename(flow.get("flow_name", "flow"))
        results[flow_name] = []
        steps = flow.get("steps", []) or []

        email_step_counter = 0
        sms_step_counter = 0
        for step in steps:
            channel = step.get("channel", "email")
            if channel == "email":
                email_step_counter += 1
                filename = f"{flow_name}_{email_step_counter:02d}_email.txt"
                content = _render_email_step(flow, step)
            else:  # sms
                sms_step_counter += 1
                filename = f"{flow_name}_sms_{sms_step_counter:02d}.txt"
                content = _render_sms_step(flow, step)

            path = blocks_dir / filename
            path.write_text(content, encoding="utf-8")
            results[flow_name].append(path)

    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_klaviyo_blocks.py <brief_json> <output_dir>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    written = render(data, Path(sys.argv[2]))
    total_files = sum(len(paths) for paths in written.values())
    print(f"Wrote {total_files} Klaviyo paste-ready files across {len(written)} flows:")
    for flow_name, paths in written.items():
        print(f"  {flow_name}: {len(paths)} files")
        for p in paths:
            print(f"    {p.name}")
