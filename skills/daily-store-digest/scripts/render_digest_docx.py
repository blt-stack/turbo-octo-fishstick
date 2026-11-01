"""
Render the Daily Store Digest as a single .docx briefing.

Input JSON shape:
    {
      "brand_name": "...",
      "date_covered": "2026-05-22",
      "weekday": "Friday",
      "timezone": "America/New_York",
      "generated_at": "2026-05-23T07:00:00-04:00",
      "verdict": "needs_attention",
      "one_line_summary": "Mixed day - revenue down 18% DoD but within normal variance...",

      "yesterday_numbers": {
        "revenue_net_usd": 4500.50,
        "revenue_dod_pct": -0.18,
        "revenue_wow_pct": -0.09,
        "revenue_mom_pct": 0.04,
        "orders": 47,
        "orders_dod_pct": 0.12,
        "orders_wow_pct": 0.03,
        "aov_usd": 95.76,
        "aov_dod_pct": -0.27,
        "conversion_pct": 2.58,
        "conversion_dod_pts": -0.3,
        "sessions": 1820,
        "sessions_dod_pct": 0.04,
        "new_customer_pct": 0.38,
        "refunds_count": 1,
        "refunds_usd": 48.00
      },

      "anomalies": [
        {
          "metric": "AOV",
          "yesterday_value": 95.76,
          "baseline_mean": 108.20,
          "baseline_stdev": 5.40,
          "z_score": -2.3,
          "severity": "anomaly",
          "direction": "down",
          "likely_cause": "Yesterday's email push promoted a $24 filter pack..."
        }
      ],

      "channel_breakdown": [
        {"channel": "Email (Klaviyo)", "sessions": 220, "revenue_usd": 1280.00, "pct_of_revenue": 28.4, "conv_rate_pct": 5.9}
      ],

      "top_skus": {
        "movers": [{"sku_name": "...", "units_yesterday": 22, "revenue_usd": 264, "vs_baseline_pct": 0.45}],
        "decliners": [{"sku_name": "...", "units_yesterday": 8, "revenue_usd": 384, "vs_baseline_pct": -0.35}],
        "top_by_revenue": [{"sku_name": "...", "revenue_usd": 864}]
      },

      "email_section": {
        "campaigns_sent": [{"name": "...", "open_rate_pct": 32.4, "click_rate_pct": 4.1, "revenue_usd": 1280, "rps_usd": 0.092, "vs_baseline_note": "Strong send"}],
        "active_flows": [{"name": "Welcome Series", "sends": 142, "revenue_usd": 380, "open_rate_pct": 48.2, "vs_baseline_note": "normal"}],
        "email_pct_of_revenue": 28.4,
        "list_growth_net": 14,
        "watch_items": ["Browse Abandonment open rate dipped 4 pts"]
      },

      "ads_section": {
        "spend_usd": 480, "revenue_usd": 1450, "roas": 3.02,
        "roas_baseline": 3.18, "roas_z_score": -0.7,
        "campaigns": [
          {"name": "Retargeting - 30d", "spend_usd": 180, "revenue_usd": 720, "roas": 4.0, "frequency": 3.4, "flag": "scale_candidate", "note": "Increase budget 15-20%"}
        ],
        "top_creative": "Slow Morning Reel v3 - 5.2x ROAS",
        "worst_creative": "Direct UGC product shot - 0.4x ROAS (pause)"
      },

      "traffic_section": {
        "sessions": 1820, "sessions_dod_pct": 0.04, "new_users_pct": 0.70,
        "bounce_rate_pct": 31.9, "engagement_time_seconds": 142,
        "top_landing_pages": [{"page": "/products/river-stone-pour-over", "sessions": 480, "conversions": 18, "conv_rate_pct": 3.75, "vs_baseline_pct": 0.34}],
        "funnel": {"add_to_cart_pct": 8.4, "begin_checkout_pct": 4.2, "purchase_pct": 2.58},
        "funnel_flags": ["cart-to-checkout dropped 0.9 pts; single-day"]
      },

      "needs_attention": {
        "inventory": [{"description": "...", "days_to_stockout": 8, "tier": "critical_immediate"}],
        "suppliers": [{"description": "...", "days_overdue": 4}],
        "bundles": [{"description": "...", "composite_score": 84.3}],
        "influencers": [{"description": "...", "variant": "A"}]
      },

      "suggested_actions": [
        {"rank": 1, "description": "Pause Spring sale push...", "skill": "n/a"}
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


VERDICT_DISPLAY = {
    "healthy": "HEALTHY",
    "needs_attention": "NEEDS ATTENTION",
    "critical": "CRITICAL",
}
VERDICT_COLORS = {
    "healthy": RGBColor(0x1E, 0x7A, 0x2C),       # green
    "needs_attention": RGBColor(0xC0, 0x73, 0x00), # orange
    "critical": RGBColor(0xC0, 0x00, 0x00),       # red
}
SEVERITY_COLORS = {
    "critical": RGBColor(0xC0, 0x00, 0x00),
    "anomaly": RGBColor(0xC0, 0x73, 0x00),
    "notable": RGBColor(0x55, 0x55, 0x55),
    "low_volume_rule": RGBColor(0x55, 0x55, 0x55),
    "insufficient_data": RGBColor(0x88, 0x88, 0x88),
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


def _pct(value, places=0):
    if value is None:
        return "—"
    try:
        return f"{value * 100:.{places}f}%"
    except (TypeError, ValueError):
        return str(value)


def _pct_signed(value, places=0):
    if value is None:
        return "—"
    sign = "+" if value > 0 else ""
    return f"{sign}{value * 100:.{places}f}%"


def _money(value):
    if value is None:
        return "—"
    try:
        return f"${value:,.2f}"
    except (TypeError, ValueError):
        return str(value)


def _render_header(doc, data: dict):
    title = doc.add_paragraph()
    title_run = title.add_run(f"DAILY DIGEST — {data.get('brand_name', '?')}")
    title_run.bold = True
    title_run.font.size = Pt(18)

    sub_p = doc.add_paragraph()
    weekday = data.get("weekday", "")
    sub_run = sub_p.add_run(
        f"Yesterday: {data.get('date_covered', '?')} ({weekday}) — {data.get('timezone', '')}"
    )
    sub_run.italic = True
    sub_run.font.size = Pt(9)
    sub_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    verdict = data.get("verdict", "healthy")
    verdict_p = doc.add_paragraph()
    verdict_run = verdict_p.add_run(f"Verdict: {VERDICT_DISPLAY.get(verdict, verdict.upper())}")
    verdict_run.bold = True
    verdict_run.font.size = Pt(14)
    verdict_run.font.color.rgb = VERDICT_COLORS.get(verdict, RGBColor(0x1A, 0x1A, 0x1A))

    gen_p = doc.add_paragraph()
    gen_run = gen_p.add_run(f"Generated: {data.get('generated_at', '')}")
    gen_run.italic = True
    gen_run.font.size = Pt(8)
    gen_run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    summary = data.get("one_line_summary")
    if summary:
        _add_divider(doc)
        summary_p = doc.add_paragraph()
        summary_run = summary_p.add_run(summary)
        summary_run.italic = True
        summary_run.font.size = Pt(11)


def _render_yesterday_numbers(doc, ydata: dict):
    if not ydata:
        return
    _add_divider(doc)
    _add_section_header(doc, "YESTERDAY'S NUMBERS")

    rows = [
        ("Revenue (net)", _money(ydata.get("revenue_net_usd")),
         f"DoD {_pct_signed(ydata.get('revenue_dod_pct'))}, "
         f"WoW {_pct_signed(ydata.get('revenue_wow_pct'))}, "
         f"MoM {_pct_signed(ydata.get('revenue_mom_pct'))}"),
        ("Orders", ydata.get("orders"),
         f"DoD {_pct_signed(ydata.get('orders_dod_pct'))}, WoW {_pct_signed(ydata.get('orders_wow_pct'))}"),
        ("AOV", _money(ydata.get("aov_usd")),
         f"DoD {_pct_signed(ydata.get('aov_dod_pct'))}"),
        ("Conversion", f"{ydata.get('conversion_pct', 0):.2f}%" if ydata.get("conversion_pct") is not None else "—",
         f"DoD {ydata.get('conversion_dod_pts', 0):+.1f} pts" if ydata.get("conversion_dod_pts") is not None else ""),
        ("Sessions", f"{ydata.get('sessions', 0):,}",
         f"DoD {_pct_signed(ydata.get('sessions_dod_pct'))}"),
    ]
    for label, value, context in rows:
        p = doc.add_paragraph()
        label_run = p.add_run(f"{label}: ")
        label_run.bold = True
        p.add_run(f"{value}   ")
        if context:
            ctx_run = p.add_run(f"({context})")
            ctx_run.italic = True
            ctx_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            ctx_run.font.size = Pt(9)

    if ydata.get("new_customer_pct") is not None:
        _add_kv(doc, "Customer mix",
                f"{ydata['new_customer_pct'] * 100:.0f}% new / "
                f"{(1 - ydata['new_customer_pct']) * 100:.0f}% returning")
    if ydata.get("refunds_count"):
        _add_kv(doc, "Refunds",
                f"{ydata['refunds_count']} ({_money(ydata.get('refunds_usd', 0))})")


def _render_anomalies(doc, anomalies: list):
    _add_divider(doc)
    _add_section_header(doc, "ANOMALIES DETECTED")
    if not anomalies:
        doc.add_paragraph("No anomalies flagged. Metrics tracked within normal range.")
        return

    by_severity = {"critical": [], "anomaly": [], "notable": [], "low_volume_rule": [], "insufficient_data": []}
    for a in anomalies:
        sev = a.get("severity", "notable")
        by_severity.setdefault(sev, []).append(a)

    for sev_key, sev_label in [
        ("critical", "CRITICAL (≥3σ)"),
        ("anomaly", "ANOMALY (2-3σ)"),
        ("notable", "NOTABLE (1-2σ)"),
        ("low_volume_rule", "LOW-VOLUME RULE FLAG"),
    ]:
        items = by_severity.get(sev_key, [])
        if not items:
            continue
        sev_p = doc.add_paragraph()
        sev_run = sev_p.add_run(sev_label)
        sev_run.bold = True
        sev_run.font.color.rgb = SEVERITY_COLORS.get(sev_key, RGBColor(0x55, 0x55, 0x55))

        for a in items:
            arrow = "↓" if a.get("direction") == "down" else ("↑" if a.get("direction") == "up" else "→")
            z = a.get("z_score")
            z_str = f"z={z:+.1f}σ" if isinstance(z, (int, float)) else "z=n/a"
            line = (
                f"{a.get('metric', '?')}: yesterday {a.get('yesterday_value', '?')} "
                f"vs. baseline {a.get('baseline_mean', '?')} "
                f"(stdev {a.get('baseline_stdev', '?')}) — {z_str} {arrow}"
            )
            doc.add_paragraph(line, style="List Bullet")
            if a.get("likely_cause"):
                cause_p = doc.add_paragraph()
                cause_run = cause_p.add_run(f"   Likely cause: {a['likely_cause']}")
                cause_run.italic = True
                cause_run.font.size = Pt(9)
                cause_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def _render_channel_breakdown(doc, channels: list):
    if not channels:
        return
    _add_divider(doc)
    _add_section_header(doc, "CHANNEL BREAKDOWN")
    table = doc.add_table(rows=1, cols=5)
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(["Channel", "Sessions", "Revenue", "% of revenue", "Conv rate"]):
        hdr_cells[i].text = h
    for c in channels:
        row = table.add_row().cells
        row[0].text = str(c.get("channel", ""))
        row[1].text = f"{c.get('sessions', 0):,}"
        row[2].text = _money(c.get("revenue_usd"))
        row[3].text = f"{c.get('pct_of_revenue', 0):.1f}%"
        row[4].text = f"{c.get('conv_rate_pct', 0):.2f}%"


def _render_top_skus(doc, sku_data: dict):
    if not sku_data:
        return
    _add_divider(doc)
    _add_section_header(doc, "TOP SKUs YESTERDAY")

    movers = sku_data.get("movers", []) or []
    if movers:
        _add_subheader(doc, "Movers (up vs. 7-day average)")
        for m in movers:
            change = m.get("vs_baseline_pct")
            change_str = _pct_signed(change) if change is not None else ""
            doc.add_paragraph(
                f"{m.get('sku_name', '?')} — {m.get('units_yesterday', 0)} units, "
                f"{_money(m.get('revenue_usd'))} ({change_str})",
                style="List Bullet"
            )

    decliners = sku_data.get("decliners", []) or []
    if decliners:
        _add_subheader(doc, "Decliners (down vs. 7-day average)")
        for d in decliners:
            change = d.get("vs_baseline_pct")
            change_str = _pct_signed(change) if change is not None else ""
            doc.add_paragraph(
                f"{d.get('sku_name', '?')} — {d.get('units_yesterday', 0)} units, "
                f"{_money(d.get('revenue_usd'))} ({change_str})",
                style="List Bullet"
            )

    top_rev = sku_data.get("top_by_revenue", []) or []
    if top_rev:
        _add_subheader(doc, "Top 5 by revenue yesterday")
        for i, t in enumerate(top_rev[:5], 1):
            doc.add_paragraph(
                f"{i}. {t.get('sku_name', '?')} — {_money(t.get('revenue_usd'))}"
            )


def _render_email_section(doc, esec: dict):
    if not esec:
        return
    _add_divider(doc)
    _add_section_header(doc, "EMAIL + SMS PERFORMANCE")

    campaigns = esec.get("campaigns_sent", []) or []
    if campaigns:
        _add_subheader(doc, f"Campaigns sent: {len(campaigns)}")
        for c in campaigns:
            line = (
                f"{c.get('name', '?')} — Open {c.get('open_rate_pct', 0):.1f}%, "
                f"Click {c.get('click_rate_pct', 0):.1f}%, "
                f"Revenue {_money(c.get('revenue_usd'))} "
                f"(RPS ${c.get('rps_usd', 0):.3f})"
            )
            doc.add_paragraph(line, style="List Bullet")
            if c.get("vs_baseline_note"):
                note_p = doc.add_paragraph()
                note_run = note_p.add_run(f"   {c['vs_baseline_note']}")
                note_run.italic = True
                note_run.font.size = Pt(9)
                note_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    else:
        doc.add_paragraph("No campaigns sent yesterday.")

    flows = esec.get("active_flows", []) or []
    if flows:
        _add_subheader(doc, "Active flows")
        for f in flows:
            doc.add_paragraph(
                f"{f.get('name', '?')} — {f.get('sends', 0)} sends, "
                f"{_money(f.get('revenue_usd'))}, "
                f"open {f.get('open_rate_pct', 0):.1f}% ({f.get('vs_baseline_note', '')})",
                style="List Bullet"
            )

    if esec.get("email_pct_of_revenue") is not None:
        _add_kv(doc, "Email % of total revenue", f"{esec['email_pct_of_revenue']:.1f}%")
    if esec.get("list_growth_net") is not None:
        _add_kv(doc, "List growth (net)", f"{esec['list_growth_net']:+d} subscribers")

    watch = esec.get("watch_items", []) or []
    if watch:
        _add_subheader(doc, "Watch items")
        for w in watch:
            doc.add_paragraph(w, style="List Bullet")


def _render_ads_section(doc, asec: dict):
    if not asec:
        return
    _add_divider(doc)
    _add_section_header(doc, "PAID ADS (META)")

    line = (
        f"Spend: {_money(asec.get('spend_usd'))} | "
        f"Revenue: {_money(asec.get('revenue_usd'))} | "
        f"ROAS: {asec.get('roas', 0):.2f}x"
    )
    doc.add_paragraph(line)
    if asec.get("roas_baseline") is not None:
        baseline_p = doc.add_paragraph()
        baseline_run = baseline_p.add_run(
            f"Baseline ROAS: {asec['roas_baseline']:.2f}x  "
            f"(z={asec.get('roas_z_score', 0):+.1f}σ)"
        )
        baseline_run.italic = True
        baseline_run.font.size = Pt(9)
        baseline_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    campaigns = asec.get("campaigns", []) or []
    if campaigns:
        _add_subheader(doc, "By campaign")
        for c in campaigns:
            flag = c.get("flag", "")
            flag_str = f" [{flag.upper()}]" if flag else ""
            doc.add_paragraph(
                f"{c.get('name', '?')}{flag_str} — "
                f"Spend {_money(c.get('spend_usd'))}, "
                f"Revenue {_money(c.get('revenue_usd'))}, "
                f"ROAS {c.get('roas', 0):.2f}x, "
                f"Freq {c.get('frequency', 0):.1f}",
                style="List Bullet"
            )
            if c.get("note"):
                note_p = doc.add_paragraph()
                note_run = note_p.add_run(f"   {c['note']}")
                note_run.italic = True
                note_run.font.size = Pt(9)
                note_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    if asec.get("top_creative"):
        _add_kv(doc, "Top ad creative", asec["top_creative"])
    if asec.get("worst_creative"):
        _add_kv(doc, "Worst ad creative", asec["worst_creative"])


def _render_traffic_section(doc, tsec: dict):
    if not tsec:
        return
    _add_divider(doc)
    _add_section_header(doc, "TRAFFIC + ON-SITE")

    _add_kv(doc, "Sessions", f"{tsec.get('sessions', 0):,}  (DoD {_pct_signed(tsec.get('sessions_dod_pct'))})")
    if tsec.get("new_users_pct") is not None:
        _add_kv(doc, "New users", f"{tsec['new_users_pct'] * 100:.0f}%")
    if tsec.get("bounce_rate_pct") is not None:
        _add_kv(doc, "Bounce", f"{tsec['bounce_rate_pct']:.1f}%")
    if tsec.get("engagement_time_seconds") is not None:
        _add_kv(doc, "Avg engagement", f"{tsec['engagement_time_seconds']}s")

    pages = tsec.get("top_landing_pages", []) or []
    if pages:
        _add_subheader(doc, "Top landing pages")
        for p in pages:
            change = p.get("vs_baseline_pct")
            change_str = f" ({_pct_signed(change)} vs. baseline)" if change is not None else ""
            doc.add_paragraph(
                f"{p.get('page', '?')} — {p.get('sessions', 0)} sessions, "
                f"{p.get('conversions', 0)} conversions ({p.get('conv_rate_pct', 0):.2f}%){change_str}",
                style="List Bullet"
            )

    funnel = tsec.get("funnel") or {}
    if funnel:
        _add_subheader(doc, "Funnel")
        for step, label in [
            ("add_to_cart_pct", "Add-to-cart"),
            ("begin_checkout_pct", "Begin checkout"),
            ("purchase_pct", "Purchase"),
        ]:
            if funnel.get(step) is not None:
                doc.add_paragraph(f"{label}: {funnel[step]:.2f}%", style="List Bullet")

    flags = tsec.get("funnel_flags", []) or []
    if flags:
        _add_subheader(doc, "Funnel flags")
        for f in flags:
            doc.add_paragraph(f, style="List Bullet")


def _render_needs_attention(doc, attn: dict):
    _add_divider(doc)
    _add_section_header(doc, "NEEDS ATTENTION TODAY")

    sections = [
        ("INVENTORY", attn.get("inventory", []) or []),
        ("SUPPLIERS", attn.get("suppliers", []) or []),
        ("BUNDLES", attn.get("bundles", []) or []),
        ("INFLUENCERS", attn.get("influencers", []) or []),
    ]

    any_items = False
    for label, items in sections:
        sec_p = doc.add_paragraph()
        sec_run = sec_p.add_run(f"{label}:")
        sec_run.bold = True
        if items:
            any_items = True
            for it in items:
                desc = it.get("description") if isinstance(it, dict) else str(it)
                doc.add_paragraph(desc, style="List Bullet")
        else:
            empty_p = doc.add_paragraph()
            empty_run = empty_p.add_run("  (none — healthy)")
            empty_run.italic = True
            empty_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            empty_run.font.size = Pt(9)

    if not any_items:
        nothing_p = doc.add_paragraph()
        nothing_run = nothing_p.add_run("All four cross-skill caches show no immediate items. Quiet day.")
        nothing_run.italic = True


def _render_suggested_actions(doc, actions: list):
    _add_divider(doc)
    _add_section_header(doc, "SUGGESTED ACTIONS FOR TODAY")
    if not actions:
        doc.add_paragraph("No specific actions surfaced. Focus on normal operations today.")
        return
    for a in actions:
        p = doc.add_paragraph(style="List Number")
        rank_run = p.add_run(f"{a.get('description', '?')}")
        if a.get("skill"):
            skill_p = doc.add_paragraph()
            skill_run = skill_p.add_run(f"   Skill to use: {a['skill']}")
            skill_run.italic = True
            skill_run.font.size = Pt(9)
            skill_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def render(data: dict, output_path: Path) -> Path:
    doc = Document()
    _render_header(doc, data)
    _render_yesterday_numbers(doc, data.get("yesterday_numbers", {}))
    _render_anomalies(doc, data.get("anomalies", []) or [])
    _render_channel_breakdown(doc, data.get("channel_breakdown", []) or [])
    _render_top_skus(doc, data.get("top_skus", {}) or {})
    _render_email_section(doc, data.get("email_section", {}) or {})
    _render_ads_section(doc, data.get("ads_section", {}) or {})
    _render_traffic_section(doc, data.get("traffic_section", {}) or {})
    _render_needs_attention(doc, data.get("needs_attention", {}) or {})
    _render_suggested_actions(doc, data.get("suggested_actions", []) or [])

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_digest_docx.py <digest_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    out = render(data, Path(sys.argv[2]))
    print(f"Wrote {out}")
