# Today's Build Plan: From Empty Folder to a Shareable Portfolio

The goal is a credible first version today, not a fully production-ready ad agency platform.

## Block 1 — Setup and run the starter (45–75 minutes)

1. Extract the ZIP.
2. Open PowerShell in the project folder.
3. Create a Python virtual environment and install `requirements.txt` as documented in the root README.
4. Run `python -m streamlit run app.py`.
5. Open the local URL and click each tab. Read the disclaimer; the figures and campaigns are illustrative.
6. Run `python -m pytest -q` in a second terminal using the same environment.

**Done when:** the dashboard opens and the tests pass.

## Block 2 — Learn the metrics and customize (45–60 minutes)

1. Read `docs/metric_definitions.md`.
2. Be able to explain CTR, CPC, cost/enquiry, cost/qualified lead, qualified-lead rate, appointment show rate, and ROAS without looking them up.
3. Change the title/tagline or campaign-plan wording to your own natural language.
4. Add your actual email / portfolio contact details only after deciding what you want to make public.

**Done when:** you can explain every KPI and where the number comes from.

## Block 3 — Review creative samples (60–90 minutes)

1. Inspect the three PNGs in `creative_samples/`.
2. For each, write down: target intent, hook, product value, CTA, and what must be changed for a real retailer.
3. If you can use Canva Free, recreate each with a distinct layout and replace vector jewelry illustrations with licensed or client-approved product photos.
4. Use no false claims about gold purity, certifications, discounts, stock or product prices.
5. Keep the disclosure that these are portfolio concepts until actual client work exists.

**Done when:** you can show three visibly distinct directions and explain why each exists.

## Block 4 — Write the case-study narrative (45 minutes)

Read and customize `docs/portfolio_case_study.md`.

Write this sequence in your own words:

- Problem: campaign clicks and messages are not the same as store visits or sales.
- Approach: collect aggregate data, calculate consistent KPIs, inspect stages of the funnel, and document decisions.
- What you built: dashboard, validation, charts, export, rule-based prompts and ML experiment.
- Limitations: fictional sample data, no ad account connected, no verified campaign outcomes.
- Next steps: first consented pilot, client-paid ad spend, real attribution and client-approved case study.

**Done when:** a business owner can understand the project in under two minutes.

## Block 5 — Run the ML experiment (30–45 minutes)

1. Open the `ML experiment` tab and click its button, or run `python experiments/ml_lead_quality_demo.py`.
2. Read the code and identify where data is generated, where the train/test split occurs, what model is trained, and which metrics are evaluated.
3. Compare logistic regression to the majority-class baseline.
4. In your case study, say it is a workflow demonstration on synthetic data—not a validated lead-scoring product.

**Done when:** you can explain precision, recall and why a synthetic test score is not evidence of real business performance.

## Block 6 — Test and publish the repository (60–90 minutes)

1. Run `python -m py_compile app.py metrics.py experiments/ml_lead_quality_demo.py experiments/dl_image_similarity.py`.
2. Run `python -m pytest -q`.
3. Check `.gitignore`; never add `.venv`, tokens, client files or private data.
4. Create a GitHub repo and push your project using the root README instructions.
5. Deploy to Streamlit Community Cloud if time permits. Test the link in a private/incognito window.
6. Capture screenshots of the Overview, Campaign analytics and Creative concepts tabs for your case study.

**Done when:** your public repo has source code, README, sample data, clear disclosures, and screenshots or a deployed demo.

## Block 7 — Prepare to contact prospects (30–45 minutes)

1. Complete the campaign brief template for one real jeweller you have researched.
2. Write a personalized first message using `docs/outreach_templates.md`.
3. Do not say you have improved ROAS or generated leads. Say that you have built a demonstration workflow and would like to discuss a small, measured pilot.
4. Ask for a discovery call first. Do not launch ads or spend client money before written approval, agreed scope and access permissions.

## If running out of time

Keep the order: local dashboard → three creative samples → case-study copy → tests → public repository. Skip the optional deep-learning installation today. You can add the image-similarity experiment later; it is not a reason to delay an honest, usable portfolio.
