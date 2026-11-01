"""
Forecast engine for the Inventory Forecaster skill.

Picks a forecasting method per SKU based on data depth + seasonal signal,
runs the forecast, and returns a structured result with point forecasts,
confidence band, and audit metadata.

Methods:
  - rolling_average_14d  — <60 days history
  - holt                 — 60-179 days history
  - holt_winters         — 180+ days history with seasonal signal detected
  - poisson_heuristic    — sporadic SKUs (>30% zero-sales days, mean velocity <0.5)
  - skipped              — drop-ship or discontinued

Dependencies:
  pip install statsmodels pandas numpy --break-system-packages

Usage:
    from forecast_engine import forecast_sku

    result = forecast_sku(
        sku="RS-POUR-OVER-001",
        sales_history=[
            {"date": "2025-01-15", "units_sold": 5},
            {"date": "2025-01-16", "units_sold": 7},
            ...
        ],
        on_hand=220,
        lead_time_days=45,
        moq=1500,
    )

    print(result["method_selected"])
    print(result["forecast"]["base_30d"])
    print(result["audit"]["confidence_assessment"])
"""

from __future__ import annotations

import math
import statistics
from datetime import date, datetime, timedelta
from typing import Any

try:
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.tsa.stattools import acf
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False


SEASONAL_CANDIDATE_PERIODS = [7, 14, 30, 60, 90, 180, 365]
SEASONAL_ACF_THRESHOLD = 0.30
LOW_VELOCITY_THRESHOLD = 0.5  # units/day below this is sporadic
SPORADIC_ZERO_FRACTION = 0.30  # >30% zero days = sporadic


def _to_daily_series(sales_history: list[dict]) -> "pd.Series":
    """
    Convert a list of {date, units_sold} into a daily-indexed pd.Series.
    Fills missing dates with 0 (assumes zero sales rather than missing data).
    """
    if not STATSMODELS_AVAILABLE:
        raise ImportError("pandas/numpy/statsmodels not available")

    df = pd.DataFrame(sales_history)
    df["date"] = pd.to_datetime(df["date"])
    df = df.groupby("date")["units_sold"].sum().reset_index()
    df = df.set_index("date").asfreq("D", fill_value=0)
    return df["units_sold"].astype(float)


def _detect_seasonal_period(series: "pd.Series") -> tuple[int | None, float]:
    """
    Returns (period, autocorrelation) for the strongest seasonal signal.
    Returns (None, 0) if no signal above threshold.
    """
    if len(series) < 14:
        return None, 0.0
    nlags = min(len(series) // 2, max(SEASONAL_CANDIDATE_PERIODS))
    try:
        acf_values = acf(series.values, nlags=nlags, fft=True)
    except Exception:
        return None, 0.0

    best_period: int | None = None
    best_corr = SEASONAL_ACF_THRESHOLD
    for p in SEASONAL_CANDIDATE_PERIODS:
        if p >= len(series) // 2:
            continue
        corr = abs(acf_values[p])
        if corr > best_corr:
            best_corr = corr
            best_period = p
    return best_period, best_corr


def _is_sporadic(series: "pd.Series") -> bool:
    if len(series) == 0:
        return True
    zero_fraction = (series == 0).sum() / len(series)
    mean_velocity = series.mean()
    return zero_fraction > SPORADIC_ZERO_FRACTION and mean_velocity < LOW_VELOCITY_THRESHOLD


def _classify_history_depth(days: int) -> str:
    if days < 60:
        return "short"
    if days < 180:
        return "medium"
    return "long"


def _rolling_average_forecast(series: "pd.Series", horizon_days: int, safety_multiplier: float = 1.2) -> dict[str, float]:
    last_n = min(14, len(series))
    if last_n == 0:
        return {"p10": 0.0, "p50": 0.0, "p90": 0.0, "per_day": 0.0}
    recent = series.iloc[-last_n:]
    mean = recent.mean()
    stdev = recent.std() if last_n > 1 else 0.0
    per_day = mean
    p50 = mean * horizon_days
    # Approximate confidence band via stdev × sqrt(horizon)
    band = stdev * math.sqrt(horizon_days)
    return {
        "p10": max(0.0, (p50 - 1.28 * band)),
        "p50": p50,
        "p90": p50 + 1.28 * band,
        "per_day": per_day,
    }


def _holt_forecast(series: "pd.Series", horizon_days: int) -> tuple[dict[str, float], dict[str, Any]]:
    """Returns (forecast, diagnostics). Raises on fit failure (caller handles fallback)."""
    model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal=None,
        initialization_method="estimated",
    )
    fit = model.fit(optimized=True)
    pred = fit.forecast(steps=horizon_days)
    p50_sum = float(pred.sum())
    # Residual variance for confidence band
    residuals = fit.resid.dropna()
    sigma = residuals.std() if len(residuals) > 1 else 0.0
    band = sigma * math.sqrt(horizon_days)
    per_day = p50_sum / horizon_days if horizon_days > 0 else 0.0
    forecast = {
        "p10": max(0.0, p50_sum - 1.28 * band),
        "p50": p50_sum,
        "p90": p50_sum + 1.28 * band,
        "per_day": per_day,
    }
    diagnostics = {
        "fit_aic": float(fit.aic) if hasattr(fit, "aic") else None,
        "residual_stdev": float(sigma),
    }
    return forecast, diagnostics


def _holt_winters_forecast(
    series: "pd.Series",
    horizon_days: int,
    seasonal_period: int,
) -> tuple[dict[str, float], dict[str, Any]]:
    model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal="add",
        seasonal_periods=seasonal_period,
        initialization_method="estimated",
    )
    fit = model.fit(optimized=True)
    pred = fit.forecast(steps=horizon_days)
    p50_sum = float(pred.sum())
    residuals = fit.resid.dropna()
    sigma = residuals.std() if len(residuals) > 1 else 0.0
    band = sigma * math.sqrt(horizon_days)
    per_day = p50_sum / horizon_days if horizon_days > 0 else 0.0
    forecast = {
        "p10": max(0.0, p50_sum - 1.28 * band),
        "p50": p50_sum,
        "p90": p50_sum + 1.28 * band,
        "per_day": per_day,
    }
    diagnostics = {
        "fit_aic": float(fit.aic) if hasattr(fit, "aic") else None,
        "residual_stdev": float(sigma),
        "seasonal_period_used": seasonal_period,
    }
    return forecast, diagnostics


def _poisson_heuristic_forecast(series: "pd.Series", horizon_days: int) -> dict[str, float]:
    """For sporadic SKUs — model based on inter-arrival times."""
    nonzero = series[series > 0]
    if len(nonzero) < 2:
        return {"p10": 0.0, "p50": 0.0, "p90": 0.0, "per_day": 0.0}
    mean_burst = float(nonzero.mean())
    # Approximate rate per day
    rate_per_day = nonzero.sum() / len(series)
    p50 = rate_per_day * horizon_days
    # Poisson stdev = sqrt(lambda × horizon)
    sigma = math.sqrt(rate_per_day * horizon_days) * mean_burst
    return {
        "p10": max(0.0, p50 - 1.28 * sigma),
        "p50": p50,
        "p90": p50 + 1.28 * sigma,
        "per_day": rate_per_day,
    }


def _classify_stockout_risk(
    on_hand: float,
    velocity_p50: float,
    velocity_p90: float,
    lead_time_days: int,
    safety_stock_days: int,
    reorder_window_days: int,
) -> tuple[str, float, float]:
    if velocity_p50 <= 0:
        return "healthy", 9999.0, 9999.0
    days_until_stockout_p50 = on_hand / velocity_p50
    days_until_stockout_p90 = on_hand / max(velocity_p90, 0.001)

    if days_until_stockout_p50 < lead_time_days:
        urgency = "stockout_imminent"
    elif days_until_stockout_p50 < (lead_time_days + safety_stock_days):
        urgency = "urgent"
    elif days_until_stockout_p50 < (lead_time_days + safety_stock_days + reorder_window_days):
        urgency = "reorder_soon"
    else:
        urgency = "healthy"

    return urgency, days_until_stockout_p50, days_until_stockout_p90


def _recommended_reorder_quantity(
    velocity_p50: float,
    velocity_p90: float,
    lead_time_days: int,
    transit_days: int,
    reorder_cycle_days: int,
    safety_stock_days: int,
    moq: int,
) -> int:
    coverage_days = lead_time_days + transit_days + reorder_cycle_days + safety_stock_days
    raw_quantity = velocity_p50 * coverage_days
    # Add demand-spike buffer for the lead time period
    spike_buffer = max(0.0, (velocity_p90 - velocity_p50) * lead_time_days)
    raw_quantity += spike_buffer
    return max(int(moq), int(math.ceil(raw_quantity)))


def forecast_sku(
    sku: str,
    sales_history: list[dict],
    on_hand: float = 0,
    lead_time_days: int = 30,
    transit_days: int = 14,
    moq: int = 100,
    reorder_cycle_days: int = 60,
    safety_stock_days: int = 14,
    reorder_window_days: int = 14,
    unit_price_usd: float = 0.0,
    payment_terms_in_force: str = "30_70_tt_before_shipping",
    horizons: tuple[int, ...] = (30, 60, 90),
    method_override: str | None = None,
    forecast_run_at: date | None = None,
) -> dict:
    """
    Forecast a single SKU. Returns a complete result with forecast, reorder calc, and audit.

    Raises ImportError if statsmodels/pandas not available; in that case the caller
    can fall back to rolling-average-only mode if needed.
    """
    if not STATSMODELS_AVAILABLE:
        raise ImportError("forecast_engine requires pandas + statsmodels — install via 'pip install pandas statsmodels --break-system-packages'")

    result: dict[str, Any] = {
        "sku": sku,
        "method_selected": None,
        "method_rationale": "",
        "forecast": {},
        "reorder_calc": {},
        "audit": {},
        "warnings": [],
    }

    if not sales_history:
        result["method_selected"] = "skipped"
        result["method_rationale"] = "No sales history provided"
        result["audit"]["confidence_assessment"] = "unreliable"
        result["warnings"].append("no_history")
        return result

    series = _to_daily_series(sales_history)
    history_days = len(series)

    # Audit data
    result["audit"]["history_days"] = history_days
    result["audit"]["first_sale_date"] = str(series.index.min().date()) if len(series) else None
    result["audit"]["last_sale_date"] = str(series.index.max().date()) if len(series) else None
    result["audit"]["total_units_sold_history"] = int(series.sum())
    result["audit"]["mean_velocity_units_per_day"] = float(series.mean()) if len(series) else 0.0

    # Sporadic detection
    sporadic = _is_sporadic(series)

    # Method selection
    method = method_override
    rationale_parts: list[str] = []

    if method is None:
        if sporadic:
            method = "poisson_heuristic"
            rationale_parts.append(f"Sporadic SKU: >{int(SPORADIC_ZERO_FRACTION*100)}% zero-sales days + mean velocity <{LOW_VELOCITY_THRESHOLD}/day")
        else:
            depth = _classify_history_depth(history_days)
            if depth == "short":
                method = "rolling_average_14d"
                rationale_parts.append(f"{history_days} days history (<60 threshold) — rolling average is robust")
            elif depth == "medium":
                method = "holt"
                rationale_parts.append(f"{history_days} days history (60-179) — Holt captures trend")
            else:
                seasonal_period, signal_strength = _detect_seasonal_period(series)
                if seasonal_period is not None:
                    method = "holt_winters"
                    rationale_parts.append(
                        f"{history_days} days history + seasonal signal at {seasonal_period}-day lag "
                        f"(autocorr {signal_strength:.2f} >= threshold {SEASONAL_ACF_THRESHOLD})"
                    )
                    result["audit"]["seasonal_period_detected"] = seasonal_period
                    result["audit"]["seasonal_signal_strength"] = float(signal_strength)
                else:
                    method = "holt"
                    rationale_parts.append(
                        f"{history_days} days history — no seasonal signal above threshold "
                        f"({SEASONAL_ACF_THRESHOLD}); using Holt"
                    )
    else:
        rationale_parts.append(f"Buyer-overridden method")

    # Run forecast per horizon
    fc_results: dict[str, dict[str, float]] = {}
    diagnostics: dict[str, Any] = {}
    fallback_applied = False

    try:
        for horizon in horizons:
            if method == "rolling_average_14d":
                fc = _rolling_average_forecast(series, horizon)
            elif method == "holt":
                fc, diag = _holt_forecast(series, horizon)
                diagnostics.update(diag)
            elif method == "holt_winters":
                seasonal_period = result["audit"].get("seasonal_period_detected", 7)
                fc, diag = _holt_winters_forecast(series, horizon, seasonal_period)
                diagnostics.update(diag)
            elif method == "poisson_heuristic":
                fc = _poisson_heuristic_forecast(series, horizon)
            elif method == "skipped":
                fc = {"p10": 0.0, "p50": 0.0, "p90": 0.0, "per_day": 0.0}
            else:
                fc = _rolling_average_forecast(series, horizon)
            fc_results[f"horizon_{horizon}d"] = fc
    except Exception as exc:
        # Fallback to rolling average
        fallback_applied = True
        rationale_parts.append(f"Fallback to rolling average due to fit failure: {type(exc).__name__}")
        method = "rolling_average_14d"
        for horizon in horizons:
            fc_results[f"horizon_{horizon}d"] = _rolling_average_forecast(series, horizon)

    result["method_selected"] = method
    result["method_rationale"] = "; ".join(rationale_parts)
    result["forecast"] = fc_results
    result["audit"]["fallback_applied"] = fallback_applied
    result["audit"].update(diagnostics)

    # Per-day velocity (use 30-day forecast)
    velocity_p50 = fc_results.get("horizon_30d", {}).get("per_day", 0.0)
    velocity_p90 = fc_results.get("horizon_30d", {}).get("p90", 0.0) / 30 if fc_results.get("horizon_30d") else 0.0
    result["audit"]["velocity_p50_units_per_day"] = velocity_p50
    result["audit"]["velocity_p90_units_per_day"] = velocity_p90

    # Stockout classification
    urgency, days_p50, days_p90 = _classify_stockout_risk(
        on_hand, velocity_p50, velocity_p90,
        lead_time_days, safety_stock_days, reorder_window_days
    )

    # Reorder quantity
    reorder_qty = _recommended_reorder_quantity(
        velocity_p50, velocity_p90,
        lead_time_days, transit_days,
        reorder_cycle_days, safety_stock_days, moq
    )

    # Dates
    run_date = forecast_run_at or date.today()
    deposit_date = run_date  # simplified for most payment terms
    arrive_date = deposit_date + timedelta(days=lead_time_days + transit_days)

    result["reorder_calc"] = {
        "current_on_hand": on_hand,
        "velocity_p50_units_per_day": velocity_p50,
        "velocity_p90_units_per_day": velocity_p90,
        "days_until_stockout_p50": days_p50,
        "days_until_stockout_p90": days_p90,
        "urgency": urgency,
        "lead_time_days": lead_time_days,
        "transit_days": transit_days,
        "moq": moq,
        "recommended_reorder_quantity": reorder_qty,
        "recommended_deposit_date": deposit_date.isoformat(),
        "expected_arrive_date": arrive_date.isoformat(),
        "estimated_reorder_cost_usd": round(reorder_qty * unit_price_usd, 2),
        "payment_terms_in_force": payment_terms_in_force,
        "days_short_before_arrival": max(0, (lead_time_days + transit_days) - days_p50) if days_p50 < (lead_time_days + transit_days) else 0,
    }

    # Confidence assessment
    if history_days < 30:
        confidence = "unreliable"
    elif history_days < 60 or fallback_applied:
        confidence = "low"
    elif history_days < 180:
        confidence = "medium"
    else:
        confidence = "high"
    result["audit"]["confidence_assessment"] = confidence

    # Warnings
    if history_days < 30:
        result["warnings"].append("low_history")
    if sporadic:
        result["warnings"].append("velocity_below_threshold")
    if fallback_applied:
        result["warnings"].append("fit_unstable")
    # Recent zero run check
    if len(series) >= 7 and (series.iloc[-7:] == 0).all() and series.mean() > 0.5:
        result["warnings"].append("recent_zero_run")
    # Recent outlier check (simple)
    if len(series) >= 14:
        recent = series.iloc[-14:]
        if recent.mean() > 3 * series.mean() and series.mean() > 0:
            result["warnings"].append("recent_outlier")

    return result


def forecast_catalog(
    skus_data: list[dict],
    forecast_run_at: date | None = None,
) -> list[dict]:
    """
    Run forecast_sku across a list of SKU dicts.

    Each dict in skus_data should have:
      - sku, sales_history, on_hand, lead_time_days, transit_days, moq,
        unit_price_usd, payment_terms_in_force, (optional) method_override
    """
    results = []
    for sku_data in skus_data:
        try:
            result = forecast_sku(
                sku=sku_data["sku"],
                sales_history=sku_data.get("sales_history", []),
                on_hand=sku_data.get("on_hand", 0),
                lead_time_days=sku_data.get("lead_time_days", 30),
                transit_days=sku_data.get("transit_days", 14),
                moq=sku_data.get("moq", 100),
                reorder_cycle_days=sku_data.get("reorder_cycle_days", 60),
                safety_stock_days=sku_data.get("safety_stock_days", 14),
                reorder_window_days=sku_data.get("reorder_window_days", 14),
                unit_price_usd=sku_data.get("unit_price_usd", 0.0),
                payment_terms_in_force=sku_data.get("payment_terms_in_force", "30_70_tt_before_shipping"),
                method_override=sku_data.get("method_override"),
                forecast_run_at=forecast_run_at,
            )
            result["product_name"] = sku_data.get("product_name", "")
            result["supplier_id"] = sku_data.get("supplier_id", "")
            results.append(result)
        except Exception as exc:
            results.append({
                "sku": sku_data.get("sku", "?"),
                "method_selected": "failed",
                "method_rationale": f"Forecast failed: {type(exc).__name__}: {exc}",
                "audit": {"confidence_assessment": "unreliable"},
                "warnings": ["forecast_failed"],
            })
    return results


if __name__ == "__main__":
    # Quick smoke test
    import json
    import random

    random.seed(42)
    base_velocity = 10
    history = []
    for i in range(200):
        d = (date(2025, 1, 1) + timedelta(days=i)).isoformat()
        # Add weekly seasonality + slight trend
        seasonal = 3 * math.sin(2 * math.pi * i / 7)
        trend = i * 0.02
        noise = random.uniform(-2, 2)
        units = max(0, round(base_velocity + seasonal + trend + noise))
        history.append({"date": d, "units_sold": units})

    result = forecast_sku(
        sku="SMOKE-TEST-001",
        sales_history=history,
        on_hand=200,
        lead_time_days=45,
        transit_days=30,
        moq=1500,
        unit_price_usd=4.20,
    )
    print(json.dumps(result, indent=2, default=str))
