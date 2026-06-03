# 💊📊🤖 Drug Review Insights & Summarization Tool

An end-to-end AI-powered pipeline that analyzes hundreds of thousands of patient drug reviews and generates plain-language summaries for pharmacists and healthcare researchers — no data science background required.

---

## Overview

Pharmacists and healthcare researchers need to understand how patients actually experience medications at scale. With hundreds of thousands of patient reviews across thousands of drugs and conditions, manual analysis is impossible. This tool ingests, cleans, and analyzes patient drug review data, then uses the Google Gemini API to generate plain-language summaries at the overall dataset, per-drug, and per-condition levels. The combined output gives healthcare stakeholders actionable insights from large volumes of unstructured patient feedback.

---

## Dataset

**UCI ML Drug Review Dataset (Drugs.com)**
- 219,206 patient reviews across 4,211 unique drugs and 2,724 conditions
- 10-point rating scale, free-text reviews, and helpfulness votes spanning 2008–2017
- Sources:
  - Kaggle: https://www.kaggle.com/datasets/jessicali9530/kuc-hackathon-winter-2018
  - UCI Repository: https://archive.ics.uci.edu/dataset/461/drug+review+dataset+druglib+com

---

## Pipeline Architecture

The project is organized as five sequential notebooks:

| Notebook | Description |
|---|---|
| `01_drug_review_preprocessing.ipynb` | Data ingestion, cleaning, feature engineering |
| `02_api_integration_prompt_engineering.ipynb` | Gemini API integration and prompt engineering |
| `03_drug_review_eda.ipynb` | Exploratory data analysis and visualizations |
| `04_pdf_and_evaluation.ipynb` | PDF report generation and AI evaluation |
| `05_main_pipeline.ipynb` | Master orchestration script — runs all notebooks end to end |

---

## Repository Structure

    ADS-509-Final-Project/
    │
    ├── preprocessing/
    │   └── 01_drug_review_preprocessing.ipynb
    │
    ├── api/
    │   └── 02_api_integration_prompt_engineering.ipynb
    │
    ├── eda/
    │   ├── 03_drug_review_eda.ipynb
    │   ├── fig1_rating_sentiment.png
    │   ├── fig2_top_drugs_conditions.png
    │   ├── fig3_sentiment_by_condition.png
    │   ├── fig4_avg_rating_condition.png
    │   ├── fig5_temporal_trends.png
    │   ├── fig6_correlation_heatmap.png
    │   ├── fig7_rating_vs_length.png
    │   ├── fig8_anova_boxplot.png
    │   ├── fig9_drug_quadrant.png
    │   ├── fig10_condition_share.png
    │   ├── fig11_condition_trends.png
    │   ├── fig12_review_length_sentiment.png
    │   ├── fig13_top_words.png
    │   ├── fig14_wordclouds.png
    │   ├── fig15_helpfulness.png
    │   └── eda_summary_stats.csv
    │
    ├── evaluation/
    │   ├── 04_pdf_and_evaluation.ipynb
    │   ├── fig16_ai_evaluation.png
    │   ├── fig17_ai_evaluation_table.png
    │   ├── evaluation_summary.csv
    │   └── drug_review_insights_report.pdf
    │
    ├── pipeline/
    │   ├── 05_main_pipeline.ipynb
    │   └── pipeline_outputs/
    │       ├── 01_executed.ipynb
    │       ├── 02_executed.ipynb
    │       ├── 03_executed.ipynb
    │       └── 04_executed.ipynb
    │
    ├── data/
    │   └── final/
    │       ├── ai_summaries.json
    │       └── drug_review_profile.csv
    │
    ├── .gitignore
    ├── README.md
    └── requirements.txt

---

## How to Run

### Prerequisites
- Google Colab (recommended) or a local Python 3.10+ environment
- A Google Gemini API key — get one free at https://aistudio.google.com
- Kaggle account to download the raw dataset files

### Step 1 — Download the raw dataset
Download the following two files from Kaggle and save them locally:
- `drugsComTrain_raw.csv`
- `drugsComTest_raw.csv`

### Step 2 — Set up your Gemini API key
In Google Colab, click the key icon in the left sidebar and add a new secret:
- Name: `GEMINI_API_KEY`
- Value: your Gemini API key
- Toggle Notebook access to on

### Step 3 — Upload files to Colab
Upload the following files to `/content/` in your Colab session:
- `drugsComTrain_raw.csv`
- `drugsComTest_raw.csv`
- `01_drug_review_preprocessing.ipynb`
- `02_api_integration_prompt_engineering.ipynb`
- `03_drug_review_eda.ipynb`
- `04_pdf_and_evaluation.ipynb`
- `05_main_pipeline.ipynb`

### Step 4 — Run the pipeline
Open `05_main_pipeline.ipynb` in Colab and run all cells from top to bottom. The pipeline will automatically:
1. Install all dependencies
2. Patch notebooks for Colab compatibility
3. Run all four notebooks in sequence
4. Validate all output files were produced
5. Print a final pipeline summary

### Step 5 — Access outputs
All output files will be available in `/content/` after the pipeline completes:
- `drug_review_insights_report.pdf` — the final combined report
- `ai_summaries.json` — all AI-generated narrative summaries
- `eda_summary_stats.csv` — EDA summary statistics
- `fig1` through `fig17` — all chart images

### Using cached summaries
To skip the live Gemini API call and use pre-generated summaries, set the following in `05_main_pipeline.ipynb` Step 2:

```python
USE_CACHED_SUMMARIES = True
```

Then upload `ai_summaries.json` to `/content/` before running.

---

## Pipeline Outputs

| Output File | Description |
|---|---|
| `cleaned_drug_reviews.csv` | Fully cleaned and enriched dataset (219,206 rows) — generated at runtime |
| `drug_review_profile.csv` | Dataset summary statistics |
| `ai_summaries.json` | AI-generated summaries for overall dataset, top 5 drugs, and top 5 conditions |
| `eda_summary_stats.csv` | EDA summary statistics |
| `drug_review_insights_report.pdf` | Final combined report with AI narratives and visualizations |
| `evaluation_summary.csv` | AI accuracy evaluation table |
| `fig1–fig15` | EDA chart images |
| `fig16_ai_evaluation.png` | AI qualitative evaluation bar chart |
| `fig17_ai_evaluation_table.png` | AI qualitative evaluation comparison table |

---

## Team

| Team Member | Role |
|---|---|
| Nancy Walker | Data ingestion and preprocessing |
| Alexander Zhuk | API integration and prompt engineering |
| Michael Ha | Exploratory data analysis and visualizations |
| Mark Henry Villanueva | Pipeline integration, testing, and documentation |

---

## Dependencies

All dependencies are installed automatically by `05_main_pipeline.ipynb`. To install manually:

```bash
pip install -r requirements.txt
```

---

## GitHub

https://github.com/mvillanueva00/ADS-509-Final-Project
