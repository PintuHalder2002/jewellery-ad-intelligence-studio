import pandas as pd

from metrics import add_campaign_metrics, aggregate_metrics, validate_campaign_data


def example_data():
    return pd.DataFrame([{
        "campaign": "Test", "objective": "Leads", "spend_inr": 1000,
        "impressions": 10000, "clicks": 200, "enquiries": 20,
        "qualified_leads": 10, "appointments": 5, "store_visits": 3,
        "purchases": 1, "revenue_inr": 5000,
    }])


def test_validation_passes_for_complete_nonnegative_data():
    valid, message = validate_campaign_data(example_data())
    assert valid is True
    assert "passed" in message.lower()


def test_calculated_metrics_are_correct():
    calculated = add_campaign_metrics(example_data()).iloc[0]
    assert calculated["ctr_pct"] == 2.0
    assert calculated["cpc_inr"] == 5.0
    assert calculated["cpe_inr"] == 50.0
    assert calculated["roas"] == 5.0


def test_zero_denominators_do_not_crash():
    frame = example_data()
    frame.loc[0, "clicks"] = 0
    frame.loc[0, "impressions"] = 0
    calculated = add_campaign_metrics(frame).iloc[0]
    assert calculated["ctr_pct"] == 0
    assert calculated["cpc_inr"] == 0


def test_negative_values_are_rejected():
    frame = example_data()
    frame.loc[0, "spend_inr"] = -1
    valid, message = validate_campaign_data(frame)
    assert valid is False
    assert "negative" in message.lower()


def test_aggregate_roas_uses_totals():
    summary = aggregate_metrics(example_data())
    assert summary["roas"] == 5.0
