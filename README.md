# Business Intelligence — CIB Client Intelligence Lab
### AI-assisted client & banking analytics · independent portfolio project

> **Important:** This is an independent educational project, not affiliated with HSBC. It does not use HSBC systems or confidential data. All default data and results are synthetic and illustrative.

## Business question
Given a fictional corporate and institutional banking portfolio, how can analytics help coverage teams decide which relationships to review, which product opportunities to investigate, and what evidence is needed before acting?

## Run locally
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
The dashboard works without an API key. Optional Groq analysis requires a key stored in environment variables or Streamlit Secrets. Never commit secrets. If a key was exposed previously, revoke it and use a newly rotated key.

## Dashboard
- **Portfolio overview:** synthetic portfolio KPIs, sector mix, propensity versus simulated wallet-gap proxy.
- **Client explorer:** filter and inspect synthetic records; export a filtered CSV.
- **RM action queue:** transparent review prioritisation and exportable prompts. No automatic contact occurs.
- **Evidence & model review:** holdout ROC-AUC and average precision plus limitations and data checks.
- **AI analyst:** optional Groq-assisted draft using aggregate synthetic metrics only.

## Methods and interpretation
- **Propensity:** logistic regression predicts a simulated adoption outcome. It is not causal impact.
- **Segmentation:** K-means provides descriptive clusters.
- **Wallet opportunity:** a simulated proxy, not a measured share of a real bank's wallet.
- **Priority:** a transparent review heuristic, not a credit, suitability, pricing, or client-treatment decision.
- **AI assistance:** LLM output is an unverified draft and must be checked. Human review remains mandatory.

## Repository layout
- `app.py` — Streamlit dashboard and reproducible synthetic data pipeline.
- `sql/` — illustrative SQL schema, client intelligence mart, and human-review queue.
- `docs/METHODOLOGY.md` — model design and metric interpretation.
- `docs/GOVERNANCE.md` — responsible-use boundaries and production gaps.
- `DEPLOY_STREAMLIT_CLOUD.md` — hosting instructions.
- `requirements.txt` — Python dependencies.

## Hosting
Deploy on [Streamlit Community Cloud](https://share.streamlit.io/) with repository `dipayandey1244/Business-Intelligence-`, branch `main`, main file `app.py`. Detailed instructions: [DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md).

## Public benchmark data
This demo generates all data itself. Do not describe its synthetic records or metrics as real banking data or as HSBC performance claims.

## Responsible-use boundary
This is a portfolio demonstration, not a production banking system. Before real use, require approved data access, legal basis, security and privacy review, fair-treatment review, independent model validation, monitoring, business sign-off, and documented human ownership.
