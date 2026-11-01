"""
Bundle Engine — orchestrates the 3 discovery layers + scoring + pricing + positioning.

Layer 1: Apriori co-purchase mining
Layer 2: Categorical complementarity (use-case mapping)
Layer 3: Margin optimization (filter + score)

Pipeline:
    sales_data + product_catalog
        → Apriori candidates (data-driven)
        → Categorical candidates (use-case-driven)
        → Merge + dedupe candidates
        → Apply margin scoring
        → Compute pricing tiers per bundle
        → Generate positioning copy
        → Score + rank
        → Return bundles

Usage:
    from bundle_engine import build_bundles

    bundles = build_bundles(
        sales_rows=canonical_sales,
        product_catalog={sku: {...}, ...},
        config=plugin_config,
        inventory_data=optional_forecast_data,
        testimonial_cache_dir=optional_path,
    )
"""

from __future__ import annotations

import math
import re
from typing import Any

# Built-in use-case mappings (subset; full map lives in templates/use-case-mappings.md)
USE_CASES = {
    "coffee_brewing_complete": {
        "required_categories": ["pour_over_device", "filters"],
        "optional_categories": ["carafe", "grinder", "kettle", "scale", "beans"],
        "min_skus": 3,
        "max_skus": 4,
        "name_descriptive": "Complete Coffee Brewing Set",
        "name_evocative": "The Slow Morning Bundle",
    },
    "tea_setup": {
        "required_categories": ["teapot", "tea_loose_leaf"],
        "optional_categories": ["tea_infuser", "mug", "kettle", "tea_storage"],
        "min_skus": 3,
        "max_skus": 4,
        "name_descriptive": "Tea Ritual Set",
        "name_evocative": "The Tea Hour Bundle",
    },
    "skincare_routine_am": {
        "required_categories": ["cleanser", "moisturizer"],
        "optional_categories": ["toner", "serum", "spf", "eye_cream"],
        "min_skus": 3,
        "max_skus": 5,
        "name_descriptive": "Morning Skincare Routine",
        "name_evocative": "Wake Up Glowing",
    },
    "candle_ritual": {
        "required_categories": ["candle"],
        "optional_categories": ["wick_trimmer", "snuffer", "matches", "candle_tray"],
        "min_skus": 2,
        "max_skus": 3,
        "name_descriptive": "Candle Care Set",
        "name_evocative": "The Slow Burn Set",
    },
    "cocktail_home_bar": {
        "required_categories": ["shaker", "jigger"],
        "optional_categories": ["strainer", "bar_spoon", "glasses", "bitters"],
        "min_skus": 3,
        "max_skus": 5,
        "name_descriptive": "Home Bar Kit",
        "name_evocative": "The Mixologist's Set",
    },
    "desk_setup_basic": {
        "required_categories": ["notebook", "pen"],
        "optional_categories": ["pencil_set", "sharpener", "desk_pad"],
        "min_skus": 2,
        "max_skus": 4,
        "name_descriptive": "Desk Set",
        "name_evocative": "The Workspace Trio",
    },
}


def slugify(text: str, max_len: int = 80) -> str:
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled-bundle"


def _build_categorical_candidates(
    product_catalog: dict[str, dict],
    use_cases: dict = USE_CASES,
) -> list[dict]:
    """
    Generate bundle candidates from category use-case mappings.

    product_catalog[sku] should include 'category' (one or more strings).
    """
    # Index SKUs by category
    skus_by_category: dict[str, list[str]] = {}
    for sku, info in product_catalog.items():
        cats = info.get("categories") or [info.get("category", "")]
        for c in cats:
            if c:
                skus_by_category.setdefault(c, []).append(sku)

    candidates = []
    for uc_name, uc in use_cases.items():
        required = uc["required_categories"]
        optional = uc.get("optional_categories", [])
        # Check we have at least one SKU in each required category
        required_skus = []
        for cat in required:
            if cat in skus_by_category and skus_by_category[cat]:
                # Pick the highest-velocity SKU for the required category (or first if no velocity data)
                required_skus.append(skus_by_category[cat][0])
            else:
                # Missing a required category — skip this use-case
                required_skus = None
                break
        if not required_skus:
            continue

        # Add optional SKUs up to max
        bundle_skus = list(required_skus)
        for cat in optional:
            if len(bundle_skus) >= uc.get("max_skus", 4):
                break
            if cat in skus_by_category and skus_by_category[cat]:
                bundle_skus.append(skus_by_category[cat][0])

        if len(bundle_skus) < uc.get("min_skus", 2):
            continue

        candidates.append({
            "skus": bundle_skus,
            "bundle_type_primary": "complementary",
            "use_case_label": uc_name,
            "name_descriptive_hint": uc.get("name_descriptive"),
            "name_evocative_hint": uc.get("name_evocative"),
            "source_layer": "categorical",
        })

    return candidates


def _apriori_to_candidates(apriori_pairs: list[dict]) -> list[dict]:
    """Convert Apriori pair results into candidate bundles."""
    candidates = []
    for p in apriori_pairs:
        skus = p.get("skus") or [p["sku_a"], p["sku_b"]]
        candidates.append({
            "skus": skus,
            "bundle_type_primary": "fbt",
            "use_case_label": None,
            "source_layer": "apriori",
            "apriori_evidence": {
                "support": p["support"],
                "confidence_max": p["confidence_max"],
                "lift": p["lift"],
                "co_occurrence_count": p["co_occurrence_count"],
            },
        })
    return candidates


def _dedupe_candidates(candidates: list[dict]) -> list[dict]:
    """Merge candidates with identical SKU sets, combining evidence."""
    by_key: dict[frozenset, dict] = {}
    for c in candidates:
        key = frozenset(c["skus"])
        if key not in by_key:
            by_key[key] = dict(c)
            by_key[key]["bundle_type_secondary"] = []
        else:
            # Merge — collect secondary type info
            existing = by_key[key]
            if c["bundle_type_primary"] != existing["bundle_type_primary"]:
                if c["bundle_type_primary"] not in existing["bundle_type_secondary"]:
                    existing["bundle_type_secondary"].append(c["bundle_type_primary"])
            # Merge evidence
            if "apriori_evidence" in c and "apriori_evidence" not in existing:
                existing["apriori_evidence"] = c["apriori_evidence"]
            if c.get("use_case_label") and not existing.get("use_case_label"):
                existing["use_case_label"] = c["use_case_label"]
                existing["name_descriptive_hint"] = c.get("name_descriptive_hint")
                existing["name_evocative_hint"] = c.get("name_evocative_hint")
            if c.get("source_layer") not in existing.get("source_layer", "").split("+"):
                existing["source_layer"] = existing.get("source_layer", "") + "+" + c.get("source_layer", "")
    return list(by_key.values())


def _compute_margin_score(skus: list[str], product_catalog: dict[str, dict], discount_pct: float = 0.15) -> dict:
    """
    Score the bundle from a margin perspective.
    Returns dict with retail_total, cost_total, blended_margin_pct, margin_score (0-100).
    """
    retail_total = 0.0
    cost_total = 0.0
    have_costs = True
    for sku in skus:
        info = product_catalog.get(sku, {})
        retail = info.get("retail_price_usd") or info.get("price_usd") or 0
        cost = info.get("cost_usd")
        retail_total += retail
        if cost is None:
            have_costs = False
        else:
            cost_total += cost

    bundle_price = retail_total * (1 - discount_pct)
    if not have_costs:
        return {
            "retail_total": round(retail_total, 2),
            "cost_total": None,
            "bundle_price_at_discount": round(bundle_price, 2),
            "blended_margin_pct": None,
            "margin_score": 50,  # neutral score when cost data missing
            "has_cost_data": False,
        }

    margin_usd = bundle_price - cost_total
    margin_pct = margin_usd / bundle_price if bundle_price > 0 else 0
    # Score: 0-100 normalized; 50% margin → 50, 80% margin → 80
    score = min(100, max(0, margin_pct * 100))
    return {
        "retail_total": round(retail_total, 2),
        "cost_total": round(cost_total, 2),
        "bundle_price_at_discount": round(bundle_price, 2),
        "blended_margin_pct": round(margin_pct, 3),
        "margin_score": round(score, 1),
        "has_cost_data": True,
    }


def _compute_pricing_tiers(retail_total: float, cost_total: float | None, margin_floor: float = 0.25) -> dict:
    """Compute the 3 pricing tiers + margin status per tier."""
    tiers_config = {
        "conservative": 0.075,
        "standard": 0.15,
        "aggressive": 0.22,
    }
    tiers = {}
    for name, disc in tiers_config.items():
        bundle_price = retail_total * (1 - disc)
        savings = retail_total - bundle_price
        if cost_total is not None:
            margin_usd = bundle_price - cost_total
            margin_pct = margin_usd / bundle_price if bundle_price > 0 else 0
            passes = margin_pct >= margin_floor
        else:
            margin_pct = None
            passes = None
        tiers[name] = {
            "discount_pct": disc,
            "bundle_price_usd": round(bundle_price, 2),
            "savings_usd": round(savings, 2),
            "blended_margin_pct": round(margin_pct, 3) if margin_pct is not None else None,
            "passes_margin_floor": passes,
        }
    return tiers


def _classify_aov_lift(retail_total: float, free_shipping_threshold: float | None) -> bool:
    """Check if bundle is an AOV-Lift candidate."""
    if not free_shipping_threshold:
        return False
    return free_shipping_threshold <= retail_total <= free_shipping_threshold * 1.20


def _build_positioning_copy(
    bundle_skus: list[dict],
    candidate: dict,
    pricing_tiers: dict,
    testimonial_cache_dir=None,
) -> dict:
    """Build the 3-variant positioning copy + names."""
    descriptive = candidate.get("name_descriptive_hint") or "Bundle"
    evocative = candidate.get("name_evocative_hint") or descriptive

    sku_names = [s.get("product_name", s.get("sku", "")) for s in bundle_skus]
    sku_list = ", ".join(sku_names[:-1]) + (" and " if len(sku_names) > 1 else "") + (sku_names[-1] if sku_names else "")

    standard_tier = pricing_tiers.get("standard", {})
    savings = standard_tier.get("savings_usd", 0)

    return {
        "names": {
            "descriptive": descriptive,
            "evocative": evocative,
        },
        "variants": {
            "benefit_led": {
                "tagline": f"Save ${savings:.0f} when you buy {sku_list} together.",
                "body": f"These pieces work together — bundled at a lower price than buying separately.",
                "cta": "Add the Bundle",
            },
            "story_led": {
                "tagline": f"{evocative}: the way we use these pieces ourselves.",
                "body": f"We picked these because they fit together — the curated set we'd reach for first.",
                "cta": "Try the Set",
            },
            "social_proof_led": {
                "tagline": "What our customers buy together — now in one bundle.",
                "body": "The pieces customers reach for most often, curated and priced together.",
                "attribution": None,
                "testimonial_source": None,
                "cta": "See the Bundle",
            },
        },
        "ad_headlines": [
            f"{evocative}",
            f"Save ${savings:.0f} on the bundle.",
            f"What our customers buy together.",
        ],
        "ad_primary_text": [
            f"The set we'd give a friend to try first. Bundled at ${savings:.0f} off.",
            f"{descriptive}: curated pieces that work together.",
            f"Our most-bundled combination. Now in one click.",
        ],
        "ad_cta_options": [
            "Shop the Bundle",
            "See What's Included",
            f"Get {evocative}",
        ],
    }


def _composite_score(margin_score: float, apriori_evidence: dict | None, in_stock_velocity_score: float = 50) -> float:
    """0-100 composite score."""
    if apriori_evidence:
        # Strong data signal
        support_score = min(100, apriori_evidence.get("support", 0) * 1000)  # 0.05 support → 50
        lift_score = min(100, (apriori_evidence.get("lift", 1.0) - 1.0) * 30)  # lift 2.0 → 30, lift 5.0 → 90
    else:
        # Categorical-only — moderate score
        support_score = 50
        lift_score = 50

    score = (
        0.30 * support_score +
        0.25 * lift_score +
        0.20 * margin_score +
        0.15 * 50 +  # AOV-lift potential placeholder
        0.10 * in_stock_velocity_score
    )
    return round(min(100, max(0, score)), 1)


def build_bundles(
    apriori_pairs: list[dict],
    product_catalog: dict[str, dict],
    config: dict | None = None,
    inventory_data: dict | None = None,
    testimonial_cache_dir=None,
    max_bundles: int = 30,
) -> list[dict]:
    """
    Top-level orchestrator. Returns a sorted list of bundle dicts.
    """
    config = config or {}
    bb_config = config.get("bundle_builder", {}) or {}
    margin_floor = bb_config.get("margin_floor_pct", 0.25)
    free_shipping_threshold = bb_config.get("free_shipping_threshold_usd")

    # Layer 1: Apriori candidates
    apriori_candidates = _apriori_to_candidates(apriori_pairs)

    # Layer 2: Categorical candidates
    categorical_candidates = _build_categorical_candidates(product_catalog)

    # Merge + dedupe
    all_candidates = _dedupe_candidates(apriori_candidates + categorical_candidates)

    # Layer 3: Apply margin + build full bundle dicts
    final_bundles = []
    for candidate in all_candidates:
        skus = candidate["skus"]
        # Filter: require at least 2 SKUs, all present in catalog
        if len(skus) < 2:
            continue
        if not all(sku in product_catalog for sku in skus):
            continue

        # Margin
        margin = _compute_margin_score(skus, product_catalog, discount_pct=0.15)
        retail_total = margin["retail_total"]
        cost_total = margin["cost_total"]

        # Pricing tiers
        tiers = _compute_pricing_tiers(retail_total, cost_total, margin_floor)

        # Determine bundle type primary + secondary
        bundle_type_primary = candidate.get("bundle_type_primary", "fbt")
        bundle_type_secondary = candidate.get("bundle_type_secondary", []) or []

        # AOV-Lift?
        if _classify_aov_lift(retail_total, free_shipping_threshold):
            if "aov_lift" not in bundle_type_secondary and bundle_type_primary != "aov_lift":
                bundle_type_secondary.append("aov_lift")

        # Build SKU details
        sku_details = []
        for sku in skus:
            info = product_catalog.get(sku, {})
            sku_details.append({
                "sku": sku,
                "product_name": info.get("product_name", sku),
                "qty": 1,
                "individual_price_usd": info.get("retail_price_usd") or info.get("price_usd"),
                "cost_usd": info.get("cost_usd"),
                "category": (info.get("categories") or [info.get("category", "")])[0],
                "is_in_stock": info.get("is_in_stock", True),
                "velocity_units_per_day": (
                    inventory_data.get(sku, {}).get("velocity_p50_units_per_day")
                    if inventory_data else None
                ),
            })

        # Score
        in_stock_score = 50
        if inventory_data:
            stock_count = sum(1 for s in skus if inventory_data.get(s, {}).get("urgency") == "healthy")
            in_stock_score = (stock_count / max(len(skus), 1)) * 100

        composite = _composite_score(
            margin_score=margin["margin_score"],
            apriori_evidence=candidate.get("apriori_evidence"),
            in_stock_velocity_score=in_stock_score,
        )

        # Recommended tier
        if bundle_type_primary == "starter_kit":
            recommended_tier = "aggressive"
        elif bundle_type_primary in ("gift_set", "aov_lift"):
            recommended_tier = "conservative"
        else:
            recommended_tier = "standard"

        # Positioning copy
        positioning = _build_positioning_copy(sku_details, candidate, tiers, testimonial_cache_dir)

        bundle_id = slugify(positioning["names"]["descriptive"])

        bundle = {
            "bundle_id": bundle_id,
            "bundle_name_descriptive": positioning["names"]["descriptive"],
            "bundle_name_evocative": positioning["names"]["evocative"],
            "bundle_type_primary": bundle_type_primary,
            "bundle_type_secondary": bundle_type_secondary,
            "use_case_label": candidate.get("use_case_label"),
            "skus_included": sku_details,
            "pricing_tiers": tiers,
            "recommended_tier": recommended_tier,
            "positioning_copy": positioning,
            "discovery_evidence": {
                "source_layer": candidate.get("source_layer", "unknown"),
                "apriori_support": (candidate.get("apriori_evidence") or {}).get("support"),
                "apriori_confidence_max": (candidate.get("apriori_evidence") or {}).get("confidence_max"),
                "apriori_lift": (candidate.get("apriori_evidence") or {}).get("lift"),
                "co_occurrence_count": (candidate.get("apriori_evidence") or {}).get("co_occurrence_count"),
                "categorical_use_case": candidate.get("use_case_label"),
                "margin_score": margin["margin_score"],
                "in_stock_velocity_score": in_stock_score,
                "composite_score": composite,
                "has_cost_data": margin["has_cost_data"],
            },
            "shopify_setup": {
                "structure": "fixed_bundle",
                "parent_sku": f"BUNDLE-{bundle_id.upper()[:30]}",
                "variant_skus": [s["sku"] for s in sku_details],
                "recommended_apps": ["Shopify Bundles", "Fast Bundle", "Bold Bundles"],
            },
            "tags": [],
            "occasion": None,
            "is_seasonal": False,
            "is_starter_kit": bundle_type_primary == "starter_kit",
            "is_active": True,
        }
        final_bundles.append(bundle)

    # Sort by composite score
    final_bundles.sort(key=lambda b: b["discovery_evidence"]["composite_score"], reverse=True)
    return final_bundles[:max_bundles]


if __name__ == "__main__":
    # Smoke test with synthetic catalog
    catalog = {
        "RS-POUR-OVER": {"product_name": "River Stone Pour-Over", "retail_price_usd": 48.0, "cost_usd": 14.0, "categories": ["pour_over_device"], "is_in_stock": True},
        "FILTER-100PK": {"product_name": "Filter Pack (100)", "retail_price_usd": 12.0, "cost_usd": 3.0, "categories": ["filters"], "is_in_stock": True},
        "CARAFE-1L": {"product_name": "Glass Carafe 1L", "retail_price_usd": 32.0, "cost_usd": 10.0, "categories": ["carafe"], "is_in_stock": True},
        "STUDIO-MUG": {"product_name": "Studio Mug", "retail_price_usd": 28.0, "cost_usd": 9.0, "categories": ["mug"], "is_in_stock": True},
        "CANDLE-001": {"product_name": "Forest Candle", "retail_price_usd": 38.0, "cost_usd": 12.0, "categories": ["candle"], "is_in_stock": True},
        "WICK-TRIMMER": {"product_name": "Wick Trimmer", "retail_price_usd": 14.0, "cost_usd": 4.0, "categories": ["wick_trimmer"], "is_in_stock": True},
        "SNUFFER": {"product_name": "Snuffer", "retail_price_usd": 16.0, "cost_usd": 5.0, "categories": ["snuffer"], "is_in_stock": True},
    }
    fake_apriori = [{
        "sku_a": "RS-POUR-OVER", "sku_b": "FILTER-100PK", "skus": ["RS-POUR-OVER", "FILTER-100PK"],
        "support": 0.05, "confidence_max": 0.40, "confidence_ab": 0.40, "confidence_ba": 0.65,
        "lift": 3.2, "co_occurrence_count": 25, "basket_total": 500, "order": 2
    }]
    bundles = build_bundles(fake_apriori, catalog, config={"bundle_builder": {"free_shipping_threshold_usd": 75}})
    print(f"Built {len(bundles)} bundles")
    for b in bundles:
        print(f"  {b['bundle_name_descriptive']:42s} type={b['bundle_type_primary']:15s} score={b['discovery_evidence']['composite_score']:5.1f}")
