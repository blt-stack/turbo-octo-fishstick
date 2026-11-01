"""
Render a single bundle to a .docx file.

Single mode deliverable. Includes:
- Header (name, type, score, generated date)
- SKUs included (table)
- Pricing tiers (conservative / standard / aggressive)
- Discovery evidence
- Positioning copy (3 variants)
- Shopify setup recommendation
- Next steps

Requires python-docx (pip install python-docx --break-system-packages).
"""

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor


TYPE_DISPLAY = {
    "fbt": "Frequently-Bought-Together",
    "complementary": "Complementary Category",
    "aov_lift": "AOV-Lift",
    "gift_set": "Gift Set",
    "starter_kit": "Starter Kit",
}

SCORE_COLORS = {
    "high": RGBColor(0x1E, 0x7A, 0x2C),     # 80+
    "medium": RGBColor(0xB8, 0x86, 0x0B),   # 60-79
    "low": RGBColor(0xC0, 0x55, 0x00),      # 40-59
    "weak": RGBColor(0xC0, 0x00, 0x00),     # <40
}


def _score_color(score: float) -> RGBColor:
    if score >= 80:
        return SCORE_COLORS["high"]
    if score >= 60:
        return SCORE_COLORS["medium"]
    if score >= 40:
        return SCORE_COLORS["low"]
    return SCORE_COLORS["weak"]


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


def _render_header(doc, bundle: dict):
    title_p = doc.add_paragraph()
    name_evocative = bundle.get("bundle_name_evocative", "")
    name_descriptive = bundle.get("bundle_name_descriptive", "")
    title_run = title_p.add_run(f"Bundle: {name_evocative}")
    title_run.bold = True
    title_run.font.size = Pt(18)

    meta_p = doc.add_paragraph()
    primary = TYPE_DISPLAY.get(bundle.get("bundle_type_primary", ""), bundle.get("bundle_type_primary", ""))
    secondary = ", ".join([TYPE_DISPLAY.get(t, t) for t in bundle.get("bundle_type_secondary", [])])
    type_text = primary + (f" (+ {secondary})" if secondary else "")
    meta_run = meta_p.add_run(f"Aka: {name_descriptive}  ·  Type: {type_text}  ·  Generated: {bundle.get('generated_at', '')}")
    meta_run.italic = True
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    score = bundle.get("discovery_evidence", {}).get("composite_score", 0)
    score_p = doc.add_paragraph()
    score_run = score_p.add_run(f"Composite score: {score}/100")
    score_run.bold = True
    score_run.font.color.rgb = _score_color(score)


def _render_skus(doc, bundle: dict):
    _add_divider(doc)
    _add_section_header(doc, "SKUS INCLUDED")
    skus = bundle.get("skus_included", [])
    for s in skus:
        line = f"{s.get('qty', 1)} × {s.get('product_name', s.get('sku', ''))} ({s.get('sku', '')}) — ${(s.get('individual_price_usd') or 0):.2f}"
        if s.get("cost_usd"):
            line += f"  [cost ${s['cost_usd']:.2f}]"
        if not s.get("is_in_stock", True):
            line += "  ⚠ STOCKOUT RISK"
        doc.add_paragraph(line, style="List Bullet")

    retail_total = sum((s.get("individual_price_usd") or 0) for s in skus)
    cost_total = sum((s.get("cost_usd") or 0) for s in skus) if all(s.get("cost_usd") is not None for s in skus) else None
    _add_kv(doc, "Individual price total", f"${retail_total:.2f}")
    if cost_total is not None:
        _add_kv(doc, "Cost total", f"${cost_total:.2f}")


def _render_pricing_tiers(doc, bundle: dict):
    _add_divider(doc)
    _add_section_header(doc, "PRICING TIERS")
    tiers = bundle.get("pricing_tiers", {})
    recommended = bundle.get("recommended_tier", "standard")
    for name in ("conservative", "standard", "aggressive"):
        t = tiers.get(name, {})
        if not t:
            continue
        marker = " ← Recommended" if name == recommended else ""
        line = (
            f"{name.capitalize():14s}: "
            f"${t.get('bundle_price_usd', 0):.2f}  "
            f"({t.get('discount_pct', 0) * 100:.1f}% off, "
            f"save ${t.get('savings_usd', 0):.2f})"
        )
        margin = t.get("blended_margin_pct")
        if margin is not None:
            line += f"  — margin {margin * 100:.1f}%"
            if t.get("passes_margin_floor") is False:
                line += " ✗ BELOW FLOOR"
        line += marker
        p = doc.add_paragraph(line)
        if name == recommended:
            for run in p.runs:
                run.bold = True


def _render_discovery_evidence(doc, bundle: dict):
    _add_divider(doc)
    _add_section_header(doc, "DISCOVERY EVIDENCE")
    ev = bundle.get("discovery_evidence", {})
    _add_kv(doc, "Source layer", ev.get("source_layer"))
    if ev.get("apriori_support") is not None:
        _add_kv(doc, "Co-purchase support", f"{ev['apriori_support'] * 100:.2f}% of orders")
    if ev.get("apriori_confidence_max") is not None:
        _add_kv(doc, "Co-purchase confidence", f"{ev['apriori_confidence_max'] * 100:.1f}%")
    if ev.get("apriori_lift") is not None:
        _add_kv(doc, "Co-purchase lift", f"{ev['apriori_lift']:.2f}×")
    if ev.get("co_occurrence_count") is not None:
        _add_kv(doc, "Co-occurrence count", ev["co_occurrence_count"])
    if ev.get("categorical_use_case"):
        _add_kv(doc, "Categorical use-case", ev["categorical_use_case"])
    _add_kv(doc, "Margin score", f"{ev.get('margin_score', 0)}/100")
    _add_kv(doc, "In-stock velocity score", f"{ev.get('in_stock_velocity_score', 0)}/100")
    if not ev.get("has_cost_data"):
        p = doc.add_paragraph()
        run = p.add_run("Note: cost data missing — margin analysis approximated.")
        run.italic = True
        run.font.color.rgb = RGBColor(0xB8, 0x86, 0x0B)


def _render_positioning_copy(doc, bundle: dict):
    _add_divider(doc)
    _add_section_header(doc, "POSITIONING COPY (3 variants)")
    pos = bundle.get("positioning_copy", {})

    _add_subheader(doc, f"Names")
    doc.add_paragraph(f"Descriptive: {pos.get('names', {}).get('descriptive', '')}", style="List Bullet")
    doc.add_paragraph(f"Evocative: {pos.get('names', {}).get('evocative', '')}", style="List Bullet")

    variants = pos.get("variants", {})
    for label, key in [
        ("Variant A — Benefit-led", "benefit_led"),
        ("Variant B — Story-led", "story_led"),
        ("Variant C — Social-proof-led", "social_proof_led"),
    ]:
        v = variants.get(key, {})
        if not v:
            continue
        _add_subheader(doc, label)
        if v.get("tagline"):
            doc.add_paragraph(v["tagline"])
        if v.get("body"):
            doc.add_paragraph(v["body"])
        if v.get("attribution"):
            p = doc.add_paragraph()
            run = p.add_run(f"— {v['attribution']}")
            run.italic = True
        _add_kv(doc, "CTA", v.get("cta", ""))

    if pos.get("ad_headlines"):
        _add_subheader(doc, "Ad headlines")
        for h in pos["ad_headlines"]:
            doc.add_paragraph(h, style="List Bullet")
    if pos.get("ad_primary_text"):
        _add_subheader(doc, "Ad primary text variants")
        for t in pos["ad_primary_text"]:
            doc.add_paragraph(t, style="List Bullet")


def _render_shopify_setup(doc, bundle: dict):
    _add_divider(doc)
    _add_section_header(doc, "SHOPIFY SETUP RECOMMENDATION")
    s = bundle.get("shopify_setup", {})
    _add_kv(doc, "Structure", s.get("structure"))
    _add_kv(doc, "Parent SKU", s.get("parent_sku"))
    _add_kv(doc, "Variant SKUs", ", ".join(s.get("variant_skus", [])))
    apps = s.get("recommended_apps", [])
    if apps:
        _add_kv(doc, "Recommended bundle apps", ", ".join(apps))


def _render_next_steps(doc, bundle: dict):
    _add_divider(doc)
    _add_section_header(doc, "NEXT STEPS")
    doc.add_paragraph("1. Create the parent bundle SKU in Shopify with the recommended apps.", style="List Number")
    doc.add_paragraph("2. Set the bundle price at the recommended tier.", style="List Number")
    doc.add_paragraph("3. Pick a positioning variant and apply it to the PDP.", style="List Number")
    doc.add_paragraph("4. Run Landing Page Copywriter (skill #3) to build the bundle landing page — bundle cache is already populated.", style="List Number")
    doc.add_paragraph("5. Re-evaluate after 30 days based on sales performance.", style="List Number")


def render(bundle: dict, output_path: Path) -> Path:
    doc = Document()
    _render_header(doc, bundle)
    _render_skus(doc, bundle)
    _render_pricing_tiers(doc, bundle)
    _render_discovery_evidence(doc, bundle)
    _render_positioning_copy(doc, bundle)
    _render_shopify_setup(doc, bundle)
    _render_next_steps(doc, bundle)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_bundle_docx.py <bundle_json> <output_path>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        bundle = json.load(f)
    out = render(bundle, Path(sys.argv[2]))
    print(f"Wrote {out}")
