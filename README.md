# E-commerce Price Intelligence

End-to-end product price intelligence pipeline for data collection, historical tracking, machine-learning prediction, and Buy/Wait decision support through a Streamlit dashboard.

## What It Does

```text
Product listings
→ collection
→ cleaning and transformation
→ SQLite history
→ exploratory analysis
→ feature engineering
→ ML price prediction
→ Buy / Wait classification
→ Streamlit dashboard
```

## Current Scope

| Area | Status |
| --- | --- |
| Data cleaning and transformation | Implemented |
| Historical price storage | Implemented |
| EDA and price trend analysis | Implemented |
| Price prediction | Implemented on available/demo history |
| Buy/Wait classifier | Implemented on available/demo history |
| Streamlit dashboard | Implemented |
| Automated tests | Included |
| Live Daraz collection | Adapter included; selectors should be re-verified before relying on live data |

The project includes a synthetic-data workflow so the analytics, model-training, prediction, and dashboard layers can be explored without depending on a live retailer page.

## Tech Stack

| Layer | Tools |
| --- | --- |
| Collection | Requests, BeautifulSoup, Selenium |
| Data | Pandas, NumPy, SQLite |
| Machine learning | scikit-learn, Random Forest, joblib |
| Visualization | Matplotlib, Plotly |
| Application | Streamlit |
| Testing | Pytest |

## Project Structure

```text
.
├── analysis/
├── app/
├── data/
│   ├── raw/
│   ├── processed/
│   └── historical/
├── data_pipeline/
├── database/
├── models/
│   └── saved_models/
├── scraper/
├── scripts/
├── tests/
├── requirements.txt
└── README.md
```

## Quick Start

```bash
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate demo history, train the models, and launch the dashboard:

```bash
python -m scripts.generate_synthetic_data
python -m models.train
streamlit run app/app.py
```

## Live Data Collection

A live collection adapter is included for experimentation:

```bash
python -m scripts.scrape_and_store "laptop" --pages 2
```

Retailer markup and access rules can change. Before using live collection, re-verify selectors and follow the site's current terms, robots directives, and access controls. Do not use the collector to bypass restrictions.

## Model Design

### Price Prediction

`models/train.py::train_price_model` trains a `RandomForestRegressor` on history-derived features such as rolling price statistics, rating, discount, and review count to estimate the next observed price.

### Buy / Wait

`models/train.py::train_buy_wait_model` trains a `RandomForestClassifier`. The current labeling logic aligns the recommendation with the price forecast: a sufficiently lower predicted price maps to `WAIT`; otherwise the recommendation is `BUY`.

Meaningful price forecasting requires repeated historical observations. A single scrape is not enough to evaluate future-price behavior reliably.

## Engineering Focus

- Web data ingestion
- Data cleaning and feature engineering
- Historical data modeling
- Regression and classification workflows
- Model persistence and inference
- Interactive ML application design
- Automated testing

## Run Tests

```bash
pytest tests/ -v
```
