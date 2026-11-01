"""
Anomaly detector for the Daily Store Digest.

Computes a z-score for each numeric metric against a 7-day rolling baseline
(mean + population stdev). Classifies anomalies by severity. Supports a
weekday-aware baseline mode and a low-volume rule-based fallback.

Usage:
    from anomaly_detector import detect, classify_severity, severity_label

    history = [
        {"date": "2026-05-15", "metric": 4500},
        {"date": "2026-05-16", "metric": 4600},
        ...
    ]
    yesterday_value = 2840
    result = detect(history, yesterday_value, low_volume_threshold=100)
    # result = {"z_score": -2.6, "severity": "anomaly", "baseline_mean": 4520,
    #          "baseline_stdev": 320, "direction": "down", "low_volume": false}
"""

import math
import statistics
import sys
from datetime import datetime
from typing import Optional


SEVERITY_NORMAL = "normal"
SEVERITY_NOTABLE = "notable"
SEVERITY_ANOMALY = "anomaly"
SEVERITY_CRITICAL = "critical"
SEVERITY_LOW_VOLUME = "low_volume_rule"
SEVERITY_INSUFFICIENT_DATA = "insufficient_data"


def classify_severity(z_score: Optional[float], reduced_confidence: bool = False) -> str:
    """Bucket a z-score into a severity label.

    With reduced_confidence True (sparse-data mode), tier boundaries loosen
    by 0.5 sigma each.
    """
    if z_score is None or math.isnan(z_score) or math.isinf(z_score):
        return SEVERITY_INSUFFICIENT_DATA
    az = abs(z_score)
    if reduced_confidence:
        if az >= 3.5:
            return SEVERITY_CRITICAL
        if az >= 2.5:
            return SEVERITY_ANOMALY
        if az >= 1.5:
            return SEVERITY_NOTABLE
        return SEVERITY_NORMAL
    if az >= 3.0:
        return SEVERITY_CRITICAL
    if az >= 2.0:
        return SEVERITY_ANOMALY
    if az >= 1.0:
        return SEVERITY_NOTABLE
    return SEVERITY_NORMAL


def severity_label(severity: str) -> str:
    return {
        SEVERITY_NORMAL: "Normal",
        SEVERITY_NOTABLE: "Notable",
        SEVERITY_ANOMALY: "Anomaly",
        SEVERITY_CRITICAL: "Critical",
        SEVERITY_LOW_VOLUME: "Low-volume rule",
        SEVERITY_INSUFFICIENT_DATA: "Insufficient data",
    }.get(severity, severity)


def detect(
    baseline_values: list[float],
    yesterday_value: float,
    *,
    low_volume_threshold: float = 5.0,
    low_volume_drop_pct: float = 0.50,
    low_volume_flag_zero: bool = True,
) -> dict:
    """
    Run anomaly detection for one metric.

    baseline_values: list of float values from the prior N days (excluding yesterday)
    yesterday_value: the target-date value to evaluate
    low_volume_threshold: when baseline mean is below this, switch to rule-based detection
    low_volume_drop_pct: rule-based threshold for low-volume metrics (drop fraction triggers flag)
    low_volume_flag_zero: flag if yesterday is 0 while baseline > 0

    Returns dict with z_score, severity, baseline_mean, baseline_stdev,
    direction, reduced_confidence, low_volume.
    """
    n = len(baseline_values)
    reduced_confidence = n < 7
    insufficient_data = n < 3

    if insufficient_data:
        return {
            "z_score": None,
            "severity": SEVERITY_INSUFFICIENT_DATA,
            "baseline_mean": statistics.mean(baseline_values) if baseline_values else None,
            "baseline_stdev": None,
            "baseline_n": n,
            "direction": _direction(yesterday_value, statistics.mean(baseline_values) if baseline_values else 0),
            "reduced_confidence": True,
            "low_volume": False,
            "yesterday_value": yesterday_value,
        }

    mean = statistics.mean(baseline_values)
    # Population stdev (pstdev) - matches our methodology (the 7 days ARE the baseline)
    try:
        stdev = statistics.pstdev(baseline_values) if n >= 2 else 0.0
    except statistics.StatisticsError:
        stdev = 0.0

    # Low-volume fallback
    if mean < low_volume_threshold:
        severity = SEVERITY_NORMAL
        if low_volume_flag_zero and yesterday_value == 0 and mean > 0:
            severity = SEVERITY_ANOMALY
        elif mean > 0:
            drop_pct = (mean - yesterday_value) / mean
            if drop_pct >= low_volume_drop_pct:
                severity = SEVERITY_ANOMALY
        return {
            "z_score": None,
            "severity": severity if severity != SEVERITY_NORMAL else SEVERITY_LOW_VOLUME,
            "baseline_mean": mean,
            "baseline_stdev": stdev,
            "baseline_n": n,
            "direction": _direction(yesterday_value, mean),
            "reduced_confidence": reduced_confidence,
            "low_volume": True,
            "yesterday_value": yesterday_value,
        }

    if stdev == 0:
        # No variation in baseline -- treat any change as flagged
        if yesterday_value == mean:
            severity = SEVERITY_NORMAL
            z_score = 0.0
        else:
            severity = SEVERITY_ANOMALY
            z_score = math.inf if yesterday_value > mean else -math.inf
        return {
            "z_score": z_score if math.isfinite(z_score) else None,
            "severity": severity,
            "baseline_mean": mean,
            "baseline_stdev": 0.0,
            "baseline_n": n,
            "direction": _direction(yesterday_value, mean),
            "reduced_confidence": reduced_confidence,
            "low_volume": False,
            "yesterday_value": yesterday_value,
        }

    z_score = (yesterday_value - mean) / stdev
    severity = classify_severity(z_score, reduced_confidence=reduced_confidence)
    return {
        "z_score": z_score,
        "severity": severity,
        "baseline_mean": mean,
        "baseline_stdev": stdev,
        "baseline_n": n,
        "direction": _direction(yesterday_value, mean),
        "reduced_confidence": reduced_confidence,
        "low_volume": False,
        "yesterday_value": yesterday_value,
    }


def _direction(value: float, baseline: float) -> str:
    if value > baseline:
        return "up"
    if value < baseline:
        return "down"
    return "flat"


def weekday_baseline(
    history_by_date: dict[str, float],
    target_date: str,
    min_samples: int = 4,
) -> list[float]:
    """
    Return the last N same-weekday values from history_by_date prior to target_date.

    Used for weekday-aware baseline mode (better for stores with strong weekly
    seasonality).
    """
    try:
        target_dt = datetime.fromisoformat(target_date).date()
    except ValueError:
        return []
    target_weekday = target_dt.weekday()
    same_weekday_values = []
    for date_str, value in history_by_date.items():
        try:
            d = datetime.fromisoformat(date_str).date()
        except ValueError:
            continue
        if d == target_dt:
            continue
        if d > target_dt:
            continue
        if d.weekday() == target_weekday:
            same_weekday_values.append((d, value))
    same_weekday_values.sort(key=lambda x: x[0], reverse=True)
    selected = [v for _, v in same_weekday_values[:7]]  # last 7 same-weekday
    if len(selected) < min_samples:
        return []  # caller should fall back to calendar baseline
    return selected


def detect_metric_panel(
    metric_panel: dict[str, dict],
    yesterday: dict[str, float],
    low_volume_thresholds: dict[str, float] | None = None,
) -> dict[str, dict]:
    """
    Run detection across a panel of metrics.

    metric_panel: {metric_name: {"baseline": [values], "config": {...}}}
    yesterday: {metric_name: value}
    low_volume_thresholds: per-metric override of low_volume_threshold

    Returns: {metric_name: detection_result_dict}
    """
    results = {}
    low_volume_thresholds = low_volume_thresholds or {}
    for metric_name, slot in metric_panel.items():
        baseline = slot.get("baseline", [])
        if metric_name not in yesterday:
            continue
        threshold = low_volume_thresholds.get(metric_name, 5.0)
        results[metric_name] = detect(
            baseline_values=baseline,
            yesterday_value=yesterday[metric_name],
            low_volume_threshold=threshold,
        )
    return results


if __name__ == "__main__":
    # CLI smoke usage
    import json
    if len(sys.argv) >= 3:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            panel = json.load(f)
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            ytd = json.load(f)
        out = detect_metric_panel(panel, ytd)
        print(json.dumps(out, indent=2, default=str))
    else:
        # Self-test
        history = [4400, 4500, 4600, 4500, 4520, 4550, 4480]
        result = detect(history, 2840, low_volume_threshold=100)
        print("Self-test result:")
        print(json.dumps(result, indent=2, default=str))
