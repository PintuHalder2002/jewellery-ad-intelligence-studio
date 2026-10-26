# Portfolio Case Study: Jewellery Ad Intelligence Studio

**Project status:** Independent demonstration project; no paid client work is claimed.
**Business type:** Local jewellery retail (hypothetical use case).
**Primary goal:** Demonstrate how a small retailer could structure ad reporting and the customer enquiry funnel.

## Business problem

A retailer may receive ad clicks and social messages but lack a consistent view of how paid activity connects to qualified enquiries, appointments, store visits and reported sales. Without consistent definitions and records, it is difficult to compare campaigns fairly.

## Proposed solution

This prototype provides an aggregated campaign dashboard with metric calculations, basic data validation, downloadable reporting, transparent review prompts and a separate educational ML experiment.

## What is implemented

- Campaign data validation for required columns and non-negative numeric values.
- CTR, CPC, cost per enquiry, cost per qualified lead, qualification rate, appointment show rate and reported revenue/ad-spend ratio.
- Aggregate ratios computed from totals rather than a simple average of campaign ratios.
- Campaign comparison charts and CSV export.
- Transparent rules-based prompts for manual review.
- A scikit-learn logistic-regression experiment evaluated against a majority-class baseline using synthetic data.
- Optional MobileNetV3 image-embedding experiment documented separately; not part of the core app and not jewellery-specific.

## Data and limitations

The included campaign dataset is fictional and exists only to test the UI. No real campaign was run, no ad account is connected, and all spend, lead, purchase and revenue values are illustrative. The ML experiment's target labels are algorithmically simulated; evaluation metrics cannot be interpreted as real-world predictive performance.

## Next steps for a real pilot

1. Define the retailer's business goal and lead qualification criteria.
2. Confirm advertising account ownership and written approval.
3. Test approved ad creative with a client-funded budget.
4. Track campaign and downstream sales outcomes with clear attribution notes.
5. Replace illustrative data with privacy-safe aggregated records after client permission.
6. Only consider ML using sufficient, representative historical labelled data and a proper evaluation design.

## How success would be assessed

For a real campaign, assess cost per qualified enquiry, appointment rate, store-visit rate, purchase conversion, attributable revenue, contribution margin and the completeness of sales tracking. Do not optimize for likes or low-cost messages alone.
