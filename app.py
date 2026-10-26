from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

from metrics import REQUIRED_COLUMNS, add_campaign_metrics, aggregate_metrics, validate_campaign_data

ROOT = Path(__file__).resolve().parent
PORTFOLIO_NAME = "Pintu Halder"  # Replace before publishing
PORTFOLIO_EMAIL = "pintubaksara@gmail.com"  # Replace before publishing
DEMO_FILE = ROOT / "data" / "demo_campaigns.csv"
CREATIVE_DIR = ROOT / "creative_samples"

st.set_page_config(
    page_title="Jewellery Ad Intelligence Studio",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {padding-top: 1.8rem; padding-bottom: 2.5rem; max-width: 1400px;}
    .eyebrow {font-size: .78rem; letter-spacing: .14em; text-transform: uppercase; color: #9A763D; font-weight: 700;}
    .disclaimer {padding: .85rem 1rem; border-left: 4px solid #C6A15B; background: rgba(198,161,91,.10); border-radius: 4px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="eyebrow">PORTFOLIO CONCEPT · DEMONSTRATION PROJECT</p>', unsafe_allow_html=True)
st.title("Jewellery Ad Intelligence Studio")
st.write("A transparent workflow for reviewing ad performance, monitoring enquiries, and documenting campaign decisions.")

with st.sidebar:
    st.header("Data source")
    uploaded_file = st.file_uploader("Upload aggregated campaign CSV", type=["csv"])
    use_demo = st.checkbox("Use illustrative demo data", value=uploaded_file is None)
    st.caption("Required columns are listed in README.md. Upload aggregate campaign data only; never upload customer names, phone numbers or private messages.")
    st.divider()
    st.header("Project status")
    st.write("**Live ad account:** Not connected")
    st.write("**Customer CRM:** Not connected")
    st.write("**Data mode:** Local demonstration")

if uploaded_file is not None:
    try:
        raw_data = pd.read_csv(uploaded_file)
        is_demo = False
    except Exception as exc:
        st.error(f"Could not read this CSV: {exc}")
        st.stop()
elif use_demo:
    raw_data = pd.read_csv(DEMO_FILE)
    is_demo = True
else:
    st.info("Upload an aggregated campaign CSV in the sidebar or select the illustrative demo dataset.")
    st.stop()

valid, validation_message = validate_campaign_data(raw_data)
if not valid:
    st.error(validation_message)
    st.markdown("Required columns: " + ", ".join(REQUIRED_COLUMNS))
    st.stop()

raw_data = raw_data[REQUIRED_COLUMNS].copy()
data = add_campaign_metrics(raw_data)

if is_demo:
    st.markdown('<div class="disclaimer"><b>Illustrative data only.</b> All campaign names, spend, enquiries, purchases and revenue in the built-in dataset are fictional examples created to demonstrate the interface. They are not client results, industry benchmarks or advertising forecasts.</div>', unsafe_allow_html=True)
else:
    st.success("Uploaded CSV passed basic validation. This dashboard does not transmit your data to an ad platform.")

with st.sidebar:
    campaign_options = data["campaign"].astype(str).tolist()
    selected_campaigns = st.multiselect("Filter campaigns", campaign_options, default=campaign_options)

filtered = data[data["campaign"].isin(selected_campaigns)].copy()
if filtered.empty:
    st.warning("Select at least one campaign in the sidebar.")
    st.stop()

# Overall metrics are computed from totals, not by averaging campaign ratios.
summary = aggregate_metrics(filtered)

overview_tab, analytics_tab, creatives_tab, ml_tab, plan_tab = st.tabs([
    "Overview", "Campaign analytics", "Creative concepts", "ML experiment", "Campaign plan"
])

with overview_tab:
    st.subheader("Performance snapshot")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Ad spend", f"₹{summary['spend_inr']:,.0f}")
    k2.metric("Enquiries", f"{summary['enquiries']:,.0f}")
    k3.metric("Cost per enquiry", f"₹{summary['cpe_inr']:,.0f}")
    k4.metric("Reported revenue / spend", f"{summary['roas']:.2f}×")

    k5, k6, k7, k8 = st.columns(4)
    k5.metric("Impressions", f"{summary['impressions']:,.0f}")
    k6.metric("Click-through rate", f"{summary['ctr_pct']:.2f}%")
    k7.metric("Qualified leads", f"{summary['qualified_leads']:,.0f}")
    k8.metric("Store visits", f"{summary['store_visits']:,.0f}")

    st.markdown("### What this dashboard is designed to answer")
    st.write("Which campaign is generating enquiries? How much does each enquiry cost? Which stages of the enquiry-to-visit funnel need attention? Are sales values being recorded separately from ad-platform metrics?")
    st.caption("ROAS here is calculated as the revenue value entered in the CSV divided by ad spend. It is not profit and may be inaccurate if revenue attribution is incomplete or delayed.")

with analytics_tab:
    st.subheader("Campaign comparison")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig = px.bar(filtered, x="campaign", y="enquiries", title="Enquiries by campaign", text_auto=True)
        fig.update_layout(xaxis_title="Campaign", yaxis_title="Enquiries")
        st.plotly_chart(fig, width="stretch")
    with chart_col2:
        funnel = filtered[["campaign", "enquiries", "qualified_leads", "appointments", "store_visits", "purchases"]].melt(
            id_vars="campaign", var_name="stage", value_name="count"
        )
        fig2 = px.bar(funnel, x="campaign", y="count", color="stage", barmode="group", title="Recorded funnel stages")
        st.plotly_chart(fig2, width="stretch")

    display_columns = [
        "campaign", "objective", "spend_inr", "impressions", "clicks", "ctr_pct",
        "cpc_inr", "enquiries", "cpe_inr", "qualified_leads", "cost_per_qualified_lead_inr",
        "appointments", "store_visits", "purchases", "revenue_inr", "roas",
    ]
    pretty = filtered[display_columns].rename(columns={
        "campaign": "Campaign", "objective": "Objective", "spend_inr": "Spend (₹)",
        "impressions": "Impressions", "clicks": "Clicks", "ctr_pct": "CTR (%)",
        "cpc_inr": "CPC (₹)", "enquiries": "Enquiries", "cpe_inr": "Cost/enquiry (₹)",
        "qualified_leads": "Qualified leads", "cost_per_qualified_lead_inr": "Cost/qualified lead (₹)",
        "appointments": "Appointments", "store_visits": "Store visits", "purchases": "Purchases",
        "revenue_inr": "Reported revenue (₹)", "roas": "ROAS (×)",
    })
    st.dataframe(pretty.round(2), width="stretch", hide_index=True)
    st.download_button(
        "Download filtered metrics CSV",
        data=pretty.to_csv(index=False).encode("utf-8"),
        file_name="jewellery_campaign_metrics.csv",
        mime="text/csv",
    )

    st.markdown("### Rules-based review prompts")
    st.caption("These are transparent internal review triggers for this demo—not industry benchmarks or automated claims about campaign quality.")
    for _, row in filtered.iterrows():
        prompts = []
        if row["ctr_pct"] < 1.0 and row["impressions"] > 0:
            prompts.append("Review the opening hook, product visibility and creative-message fit; CTR alone does not identify the cause.")
        if row["enquiries"] > 0 and row["qualified_lead_rate_pct"] < 25:
            prompts.append("Review targeting, offer clarity and the questions used to qualify enquiries.")
        if row["appointments"] > 0 and row["appointment_show_rate_pct"] < 50:
            prompts.append("Review appointment reminders, response speed and the store-visit booking flow.")
        if row["spend_inr"] > 0 and row["revenue_inr"] == 0:
            prompts.append("Check attribution delay and retailer sales records before deciding the campaign failed.")
        with st.expander(str(row["campaign"])):
            if prompts:
                for prompt in prompts:
                    st.write("- " + prompt)
            else:
                st.write("No preset review trigger fired. This is not proof of success; compare lead quality, margin, tracking completeness and the campaign goal.")

with creatives_tab:
    st.subheader("Three creative directions")
    st.write("Use these as concept pieces. Before a real campaign, replace the illustrative art or text-only visuals with product images the client owns or has licensed, and obtain approval for every offer and product claim.")
    creative_files = [
        ("01 · Festive collection", "Collection discovery", "The Festive Edit", "Explore designs for your celebrations.", "EXPLORE THE COLLECTION", "creative_01_festive.png"),
        ("02 · Wedding edit", "Occasion / gifting", "Made for the Moments", "Discover pieces for meaningful occasions.", "VIEW THE WEDDING EDIT", "creative_02_wedding.png"),
        ("03 · Store visit", "WhatsApp / appointment", "See It In Person", "Ask about designs and arrange a store visit.", "MESSAGE TO ARRANGE A VISIT", "creative_03_store_visit.png"),
    ]
    cols = st.columns(3)
    for col, (heading, angle, headline, body, cta, filename) in zip(cols, creative_files):
        with col:
            image_path = CREATIVE_DIR / filename
            if image_path.exists():
                st.image(str(image_path), width="stretch")
            st.markdown(f"**{heading}**")
            st.caption(f"Angle: {angle}")
            st.write(f"**Headline:** {headline}")
            st.write(body)
            st.write(f"**CTA:** {cta}")
    st.caption("Concept artwork only. No real client is represented and no actual campaign outcomes are claimed.")

with ml_tab:
    st.subheader("ML experiment: a reproducible evaluation workflow")
    st.markdown('<div class="disclaimer"><b>Simulation only.</b> This model is trained on synthetic leads and labels generated by a formula. Its scores do not describe real customers, do not establish predictive value, and must not be used to rank real people.</div>', unsafe_allow_html=True)
    st.write("The experiment demonstrates a train/test split, feature scaling, logistic regression, and comparison against a simple majority-class baseline. Real deployment would require appropriately collected historical outcomes, privacy review, leakage checks, class-imbalance review, and evaluation on later unseen data.")
    if st.button("Run synthetic ML experiment", type="primary"):
        try:
            sys.path.insert(0, str(ROOT / "experiments"))
            from ml_lead_quality_demo import train_demo_model
            results = train_demo_model()
            st.write(f"Synthetic rows: **{results['rows']}** · Training rows: **{results['train_rows']}** · Test rows: **{results['test_rows']}**")
            st.write(f"Simulated positive-label rate: **{results['positive_rate_pct']:.1f}%**")
            left, right = st.columns(2)
            with left:
                st.markdown("**Logistic regression**")
                st.json(results["model"])
            with right:
                st.markdown("**Majority-class baseline**")
                st.json(results["baseline"])
            st.write("Features used: " + ", ".join(results["features"]))
            st.success("Experiment ran. Record the method and limitations in your portfolio; do not describe these synthetic scores as business results.")
        except Exception as exc:
            st.error(f"ML experiment could not run. Confirm scikit-learn is installed. Details: {exc}")

with plan_tab:
    st.subheader("Example campaign plan")
    st.markdown("**Objective**  \nGenerate qualified product enquiries and store-appointment requests for a local jewellery retailer.")
    st.markdown("**Before launch**  \nConfirm service radius, products in stock, approved imagery, offer terms, business hours, WhatsApp response owner, budget ceiling, and what qualifies as a lead.")
    st.markdown("**Creative tests**")
    st.write("1. Product-led collection showcase.\n2. Occasion-led styling or gifting concept.\n3. Store-visit / availability message with a clear next step.")
    st.markdown("**Measurement**  \nTrack spend, impressions, clicks, enquiries, qualified leads, appointments, store visits, purchases, recorded revenue and attribution notes.")
    st.markdown("**Decision cadence**  \nReview delivery and tracking daily. Do not make strong conclusions from very small samples. Change one important variable at a time where possible. Obtain client approval before changing budget or claims.")
    st.markdown("**Not included by default**  \nGuaranteed sales, ad spend, photography, influencer fees, website development, CRM subscriptions or sales-staff duties. Define scope in writing before accepting payment.")

st.divider()
st.caption("Built as an independent portfolio demonstration. Replace contact placeholders and personalize the case study before publishing. Do not represent sample numbers or fictional creative concepts as client work.")
