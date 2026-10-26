"""Small, testable marketing metric calculations for the portfolio demo."""
from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = [
    "campaign", "objective", "spend_inr", "impressions", "clicks", "enquiries",
    "qualified_leads", "appointments", "store_visits", "purchases", "revenue_inr",
]
NUMERIC_COLUMNS = [
    "spend_inr", "impressions", "clicks", "enquiries", "qualified_leads",
    "appointments", "store_visits", "purchases", "revenue_inr",
]


def validate_campaign_data(frame: pd.DataFrame) -> tuple[bool, str]:
    """Validate required columns, numeric fields, and non-negative values."""
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        return False, "Missing required columns: " + ", ".join(missing)
    if frame.empty:
        return False, "The CSV has no campaign rows."
    for column in NUMERIC_COLUMNS:
        converted = pd.to_numeric(frame[column], errors="coerce")
        if converted.isna().any():
            return False, f"Column '{column}' must contain numeric values with no blanks."
        if (converted < 0).any():
            return False, f"Column '{column}' cannot contain negative values."
    if frame["campaign"].astype(str).str.strip().eq("").any():
        return False, "Campaign names cannot be blank."
    return True, "Data checks passed."


def add_campaign_metrics(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of campaign rows with transparent derived metrics.

    Ratios whose denominator is zero are set to zero for display. Interpret
    those rows carefully; zero here means 'not calculable', not 'no performance'.
    """
    data = frame.copy()
    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="raise")

    def safe_ratio(numerator: str, denominator: str) -> pd.Series:
        denom = data[denominator].where(data[denominator] != 0)
        return (data[numerator] / denom).fillna(0)

    data["ctr_pct"] = safe_ratio("clicks", "impressions") * 100
    data["cpc_inr"] = safe_ratio("spend_inr", "clicks")
    data["cpe_inr"] = safe_ratio("spend_inr", "enquiries")
    data["cost_per_qualified_lead_inr"] = safe_ratio("spend_inr", "qualified_leads")
    data["qualified_lead_rate_pct"] = safe_ratio("qualified_leads", "enquiries") * 100
    data["appointment_show_rate_pct"] = safe_ratio("store_visits", "appointments") * 100
    data["roas"] = safe_ratio("revenue_inr", "spend_inr")
    return data


def aggregate_metrics(frame: pd.DataFrame) -> dict[str, float]:
    """Calculate overall ratios from totals, rather than averaging row ratios."""
    data = frame.copy()
    totals = {column: float(pd.to_numeric(data[column], errors="raise").sum()) for column in NUMERIC_COLUMNS}

    def ratio(numerator: str, denominator: str) -> float:
        return totals[numerator] / totals[denominator] if totals[denominator] else 0.0

    return {
        **totals,
        "ctr_pct": ratio("clicks", "impressions") * 100,
        "cpc_inr": ratio("spend_inr", "clicks"),
        "cpe_inr": ratio("spend_inr", "enquiries"),
        "cost_per_qualified_lead_inr": ratio("spend_inr", "qualified_leads"),
        "qualified_lead_rate_pct": ratio("qualified_leads", "enquiries") * 100,
        "appointment_show_rate_pct": ratio("store_visits", "appointments") * 100,
        "roas": ratio("revenue_inr", "spend_inr"),
    }
