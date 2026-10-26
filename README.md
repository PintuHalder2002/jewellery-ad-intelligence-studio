# Jewellery Ad Intelligence Studio

**An independent portfolio demonstration for jewellery advertising, enquiry tracking and campaign analytics.**

This is a starter project you can customize and publish as a portfolio. The built-in campaign data and all performance values are fictional and illustrative. No real ad account is connected, no campaign was run, and no client results are claimed.

## What is included

- A Streamlit dashboard with campaign filters, KPI calculations, charts and CSV export.
- Three original visual concept ads for a hypothetical jewellery campaign. They are graphic mockups, not photos of real products.
- A campaign brief template and outreach templates.
- A transparent scikit-learn experiment using synthetic lead data, with a train/test split and a majority-class baseline.
- An optional MobileNetV3 image-similarity experiment. This is a stretch task and not required for the first portfolio publish.
- Unit tests for calculations and input validation.

## Recommended build order for today

1. Run this project locally exactly as it is.
2. Understand and test the dashboard metrics.
3. Replace the generic contact details / wording with your own details.
4. Review the three creative mockups and rewrite the copy in your own voice.
5. Run the ML simulation and document why it is not evidence of real-world performance.
6. Run the tests, capture clean screenshots, and publish the repository.
7. Deploy the app if time permits.
8. Add deep learning only after the core site works and is publishable.

## 1. Requirements

- Windows 10/11 and PowerShell.
- Python 3.10–3.14 supported by current PyTorch releases if you later run the optional deep-learning experiment. For the core dashboard, use a Python version supported by Streamlit and scikit-learn.
- Internet access for installing Python packages and optional cloud deployment.
- Git is useful for publishing, but not required to run locally.

## 2. Start on Windows PowerShell

If you extracted this ZIP into Downloads, change into its folder first. Example:

```powershell
cd "$HOME\Downloads\jewellery-ad-intelligence-studio"
```

If it is in another location, use that location instead. Then run:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks environment activation, use this for the current PowerShell session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Then launch the app:

```powershell
python -m streamlit run app.py
```

Streamlit should display a local address, usually `http://localhost:8501`. Keep the terminal open while using the app. To stop it, press `Ctrl+C` in that terminal.

### If you use Anaconda

You can also create an environment with Conda, then install the requirements:

```powershell
conda create -n jewellery-portfolio python=3.12 -y
conda activate jewellery-portfolio
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Do not mix packages across the base Conda environment and a separate `.venv`; choose one environment path for this project.

## 3. What to inspect in the dashboard

Open these tabs in order:

1. **Overview** — aggregated spend, enquiries, cost/enquiry and recorded-revenue/ad-spend ratio.
2. **Campaign analytics** — compare campaign counts and examine calculated metrics.
3. **Creative concepts** — inspect the three mockups, hooks and calls to action.
4. **ML experiment** — run the synthetic modelling pipeline and compare it to a majority-class baseline.
5. **Campaign plan** — review the brief and operational steps before launching a real test.

The figures are deliberately labelled illustrative. They are not market benchmarks. A revenue/ad-spend ratio (ROAS) is not profit and can be wrong when sales attribution is incomplete or delayed.

## 4. Use the CSV template

The application expects these exact columns:

```text
campaign, objective, spend_inr, impressions, clicks, enquiries, qualified_leads, appointments, store_visits, purchases, revenue_inr
```

Copy `data/demo_campaigns.csv` to create your own aggregated dataset. Keep values non-negative and use one row per campaign or reporting period. For real client data, agree on consistent definitions for an enquiry, qualified lead, appointment, visit, purchase and attributed revenue.

**Privacy rule:** do not put customer names, phone numbers, private WhatsApp text, payment details, or other personally identifiable information in the portfolio dataset. For public screenshots, use only the illustrative data or client-approved aggregated data.

## 5. Run the tests

With the project environment active:

```powershell
python -m pytest -q
```

The tests cover basic input validation, KPI arithmetic, zero denominators and the aggregate ROAS formula.

Run the ML experiment separately if you want to see terminal output:

```powershell
python experiments/ml_lead_quality_demo.py
```

This experiment creates synthetic data from a simulated formula. Its scores are only evidence that the code executes a train/test/evaluation workflow; they are not a claim that the model identifies valuable real customers.

## 6. Publish to GitHub

1. Create a GitHub account if you do not have one.
2. Create a new public repository named `jewellery-ad-intelligence-studio` (or a name you choose).
3. Keep `.gitignore` in the repository. Do not upload `.venv`, credentials, secrets, private client records or unlicensed images.
4. From the project root, run:

```powershell
git init
git add .
git commit -m "Build jewellery ad intelligence portfolio demo"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/jewellery-ad-intelligence-studio.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username. If Git asks you to authenticate, follow GitHub's current sign-in flow; do not put a password or token in source code.

## 7. Deploy the app (optional if you're short on time)

Use the current official Streamlit Community Cloud instructions at https://docs.streamlit.io/deploy/streamlit-community-cloud. The usual flow is to connect GitHub, select your repository and `app.py`, then deploy. The repository includes `requirements.txt` for dependency installation.

After deploy, open the public URL in a private/incognito window to test it. Do not upload private customer data to a public app. A public demo must not be described as a secure client workspace.

## 8. Optional deep-learning image similarity

This experiment is not required to publish the main portfolio today. It uses a pretrained MobileNetV3 model to extract image embeddings and rank pairs by cosine similarity; it does not train the model, and general ImageNet features may not align with jewellery design similarity.

1. Copy at least two images you own or are permitted to use into `assets/jewellery_images/`.
2. Use the official PyTorch selector to choose Windows + Pip + Python + CPU (unless you have verified compatible GPU hardware): https://pytorch.org/get-started/locally/.
3. Install the command generated by the selector, then install Pillow and scikit-learn if needed.
4. Run:

```powershell
python experiments/dl_image_similarity.py
```

The first run may download pretrained weights. Skip it if installation is slow or your disk space / internet is limited. Clearly label the output as exploratory and manually check the matches.

## 9. What to say in your portfolio

Use wording like:

> I built a demonstration dashboard for jewellery campaign reporting, with transparent KPI calculations, campaign comparison, lead-funnel tracking, data validation and an evaluated ML workflow on synthetic data. I also explored pretrained computer-vision embeddings for image similarity. The built-in dataset is illustrative; I have not represented it as client results.

Do not call yourself an experienced media buyer if you have not managed real campaigns. Your first real case study should be added only after completing a paid or explicitly authorized pilot and obtaining permission to share the results.

## Official references

- Streamlit getting started: https://docs.streamlit.io/get-started
- Streamlit Community Cloud deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud
- scikit-learn model evaluation: https://scikit-learn.org/stable/modules/model_evaluation.html
- scikit-learn train/test split: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- PyTorch local install selector: https://pytorch.org/get-started/locally/
- Meta Ad Library for researching visible competitor creatives: https://www.facebook.com/ads/library/
