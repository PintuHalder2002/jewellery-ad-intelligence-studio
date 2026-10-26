"""Educational ML workflow using synthetic data only; not for real lead scoring.

Run from the project root:
    python experiments/ml_lead_quality_demo.py

The labels are simulated from a known formula. Metrics only demonstrate a
train/test/evaluation workflow; they are not evidence that this predicts real
jewellery customers or increases sales.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "product_interest_score",
    "budget_fit_score",
    "response_minutes",
    "asked_for_appointment",
    "replied_after_followup",
]


def make_synthetic_leads(n_rows: int = 800, random_state: int = 42) -> tuple[pd.DataFrame, pd.Series]:
    """Create reproducible fictional examples with a deliberately simulated label."""
    rng = np.random.default_rng(random_state)
    X = pd.DataFrame({
        "product_interest_score": rng.integers(1, 11, n_rows),
        "budget_fit_score": rng.integers(1, 11, n_rows),
        "response_minutes": rng.integers(1, 241, n_rows),
        "asked_for_appointment": rng.binomial(1, 0.38, n_rows),
        "replied_after_followup": rng.binomial(1, 0.58, n_rows),
    })
    latent = (
        0.42 * (X["product_interest_score"] - 5.5)
        + 0.48 * (X["budget_fit_score"] - 5.5)
        + 0.85 * X["asked_for_appointment"]
        + 0.55 * X["replied_after_followup"]
        - 0.008 * (X["response_minutes"] - 30)
        + rng.normal(0, 1.25, n_rows)
    )
    probability = 1 / (1 + np.exp(-latent))
    y = pd.Series(rng.binomial(1, probability), name="qualified_lead_simulated")
    return X, y


def train_demo_model(random_state: int = 42) -> dict:
    """Train logistic regression and compare it with a majority-class baseline."""
    X, y = make_synthetic_leads(random_state=random_state)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=random_state, stratify=y
    )
    model = Pipeline([
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=1000, random_state=random_state)),
    ])
    baseline = DummyClassifier(strategy="most_frequent")
    model.fit(X_train, y_train)
    baseline.fit(X_train, y_train)

    model_pred = model.predict(X_test)
    model_prob = model.predict_proba(X_test)[:, 1]
    baseline_pred = baseline.predict(X_test)
    return {
        "rows": len(X),
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "positive_rate_pct": float(y.mean() * 100),
        "model": {
            "accuracy_pct": float(accuracy_score(y_test, model_pred) * 100),
            "precision_pct": float(precision_score(y_test, model_pred, zero_division=0) * 100),
            "recall_pct": float(recall_score(y_test, model_pred, zero_division=0) * 100),
            "f1_pct": float(f1_score(y_test, model_pred, zero_division=0) * 100),
            "roc_auc": float(roc_auc_score(y_test, model_prob)),
        },
        "baseline": {
            "accuracy_pct": float(accuracy_score(y_test, baseline_pred) * 100),
            "f1_pct": float(f1_score(y_test, baseline_pred, zero_division=0) * 100),
        },
        "features": FEATURES,
        "label_source": "Simulated from a formula; not real customer outcomes.",
    }


if __name__ == "__main__":
    from pprint import pprint
    print("EDUCATIONAL DEMO ONLY — metrics are not evidence of real-world performance.\n")
    pprint(train_demo_model())
