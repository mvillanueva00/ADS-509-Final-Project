"""
Drug Review Insights & Summarization Tool
Streamlit Application — Interactive Demo

This application demonstrates a proof-of-concept pipeline for automated
patient drug review analysis and AI-assisted summarization at scale.

Usage:
    streamlit run app.py

Requirements:
    pip install streamlit pillow
"""

import json
import os
import re
import streamlit as st
from PIL import Image

# ── Page configuration ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Drug Review Insights",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.8rem;
        color: #0f2b4e;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }

    .main-subtitle {
        font-size: 1.05rem;
        color: #4a6585;
        font-weight: 300;
        margin-bottom: 0.5rem;
    }

    .demo-banner {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        font-size: 0.88rem;
        color: #1e40af;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }

    .demo-banner strong {
        color: #1e3a8a;
    }

    .section-header {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #0f2b4e;
        border-bottom: 2px solid #e8f0fe;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }

    .ai-summary-box {
        background: linear-gradient(135deg, #f0f6ff 0%, #e8f4f8 100%);
        border-left: 4px solid #1a56db;
        border-radius: 0 8px 8px 0;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #1e3a5f;
    }

    .stat-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }

    .stat-value {
        font-family: 'DM Serif Display', serif;
        font-size: 1.8rem;
        color: #1a56db;
        margin: 0;
    }

    .stat-label {
        font-size: 0.78rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0;
    }

    .tag-drug {
        background: #dbeafe;
        color: #1e40af;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    .tag-condition {
        background: #d1fae5;
        color: #065f46;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    .sidebar-note {
        font-size: 0.8rem;
        color: #4a5568;
        line-height: 1.5;
    }

    .disclaimer {
        background: #fffbeb;
        border: 1px solid #fcd34d;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.82rem;
        color: #92400e;
        margin-top: 1.5rem;
    }

    .chart-note {
        font-size: 0.78rem;
        color: #718096;
        font-style: italic;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stSelectbox"] label {
        font-weight: 600;
        color: #0f2b4e;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# ── Load data ──────────────────────────────────────────────────────────────
@st.cache_data
def load_summaries():
    """Load AI summaries from JSON file."""
    paths = [
        'data/final/ai_summaries.json',
        '../data/final/ai_summaries.json',
        'ai_summaries.json',
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    return None


def find_chart(name):
    """Search common paths for a chart image."""
    search_paths = [
        f'eda/{name}',
        f'evaluation/{name}',
        f'../eda/{name}',
        f'../evaluation/{name}',
        name,
    ]
    for path in search_paths:
        if os.path.exists(path):
            return path
    return None


def clean_markdown(text):
    """Strip markdown headers and bold for clean display."""
    text = re.sub(r'#{1,4}\s*', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    return text.strip()


def extract_stats_from_profile(profile_text):
    """Extract key stats from the data profile string."""
    stats = {}
    patterns = {
        'total_reviews': r'Total reviews:\s*([\d,]+)',
        'avg_rating':    r'Average rating:\s*([\d.]+)',
        'pct_positive':  r'Positive reviews:\s*\d+\s*\(([\d.]+)%\)',
        'pct_negative':  r'Negative reviews:\s*\d+\s*\(([\d.]+)%\)',
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, profile_text)
        if match:
            val = match.group(1).replace(',', '')
            stats[key] = float(val)
    return stats


# ── Load summaries ─────────────────────────────────────────────────────────
summaries = load_summaries()

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💊 Drug Review Insights")
    st.markdown("---")
    st.markdown("""
    <p class='sidebar-note'>
    This tool analyzes patient drug reviews using AI to generate plain-language summaries
    for pharmacists and healthcare researchers.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("**Dataset**")
    st.markdown("""
    <p class='sidebar-note'>
    UCI ML Drug Review Dataset<br>
    219,206 reviews · 4,211 drugs · 2,724 conditions · 2008–2017
    </p>
    """, unsafe_allow_html=True)

    st.markdown("**Available in this demo**")
    st.markdown("""
    <p class='sidebar-note'>
    💊 <strong>Drugs:</strong> Levonorgestrel, Etonogestrel, Ethinyl estradiol / norethindrone, Nexplanon, Ethinyl estradiol / norgestimate<br><br>
    🏥 <strong>Conditions:</strong> Birth Control, Depression, Pain, Anxiety, Acne
    </p>
    """, unsafe_allow_html=True)

    st.markdown("**Powered by**")
    st.markdown("""
    <p class='sidebar-note'>
    Google Gemini API · Python · pandas · matplotlib · Streamlit
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <p class='sidebar-note'>
    ADS-509 Final Project<br>
    University of San Diego
    </p>
    """, unsafe_allow_html=True)


# ── Main content ───────────────────────────────────────────────────────────
st.markdown("<p class='main-title'>Drug Review Insights<br>&amp; Summarization Tool</p>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>AI-powered patient experience summaries for pharmacists and healthcare researchers</p>", unsafe_allow_html=True)

# Demo banner
st.markdown("""
<div class='demo-banner'>
    <strong>📌 Demo Notice:</strong> This application demonstrates a proof-of-concept pipeline for automated
    patient drug review analysis and AI-assisted summarization at scale. Summaries are currently available
    for the <strong>top 5 most reviewed drugs</strong> and <strong>top 5 most reviewed conditions</strong>
    from the dataset. The underlying pipeline is designed to scale across all 4,211 drugs and 2,724 conditions
    in a production environment.
</div>
""", unsafe_allow_html=True)

if summaries is None:
    st.error("Could not load AI summaries. Make sure `ai_summaries.json` is in the correct path.")
    st.stop()

# ── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Search by Drug or Condition", "📊 Overall Dataset", "📋 About"])


# ── TAB 1: Search ──────────────────────────────────────────────────────────
with tab1:
    st.markdown("### Search Drug or Condition")
    st.markdown("Select a drug or medical condition to view AI-generated patient experience summaries and analytics.")

    drug_options = [f"💊 {drug}" for drug in summaries['drugs'].keys()]
    condition_options = [f"🏥 {condition}" for condition in summaries['conditions'].keys()]
    all_options = ["— Select a drug or condition —"] + drug_options + condition_options

    selection = st.selectbox(
        "Type to search or scroll to select:",
        options=all_options,
        index=0
    )

    if selection != "— Select a drug or condition —":
        is_drug = selection.startswith("💊")
        name = selection.replace("💊 ", "").replace("🏥 ", "").strip()
        entry_type = "Drug" if is_drug else "Condition"
        data = summaries['drugs'].get(name) or summaries['conditions'].get(name)

        if data:
            st.markdown("---")

            tag_html = f"<span class='tag-drug'>{entry_type}</span>" if is_drug else f"<span class='tag-condition'>{entry_type}</span>"
            st.markdown(f"## {name} &nbsp; {tag_html}", unsafe_allow_html=True)

            # Stat cards
            stats = extract_stats_from_profile(data['data_profile'])
            if stats:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class='stat-card'>
                        <p class='stat-value'>{int(stats.get('total_reviews', 0)):,}</p>
                        <p class='stat-label'>Total Reviews</p>
                    </div>""", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class='stat-card'>
                        <p class='stat-value'>{stats.get('avg_rating', 0):.1f}<span style='font-size:1rem;color:#718096'>/10</span></p>
                        <p class='stat-label'>Avg Rating</p>
                    </div>""", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class='stat-card'>
                        <p class='stat-value' style='color:#16a34a'>{stats.get('pct_positive', 0):.1f}%</p>
                        <p class='stat-label'>Positive Reviews</p>
                    </div>""", unsafe_allow_html=True)
                with col4:
                    st.markdown(f"""
                    <div class='stat-card'>
                        <p class='stat-value' style='color:#dc2626'>{stats.get('pct_negative', 0):.1f}%</p>
                        <p class='stat-label'>Negative Reviews</p>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # AI Summary + Sentiment chart
            col_left, col_right = st.columns([3, 2])

            with col_left:
                st.markdown("<p class='section-header'>AI-Generated Summary</p>", unsafe_allow_html=True)
                summary_text = clean_markdown(data['summary'])
                st.markdown(f"<div class='ai-summary-box'>{summary_text}</div>", unsafe_allow_html=True)

                st.markdown("""
                <div class='disclaimer'>
                ⚠️ <strong>Clinical Disclaimer:</strong> These summaries are derived from patient-reported reviews,
                not clinical trial data. They should not be used as a substitute for clinical guidance or professional medical advice.
                </div>
                """, unsafe_allow_html=True)

            with col_right:
                st.markdown("<p class='section-header'>Sentiment by Condition</p>", unsafe_allow_html=True)
                st.markdown("<p class='chart-note'>Dataset-wide context — sentiment mix across top 10 conditions</p>", unsafe_allow_html=True)
                chart = find_chart('fig3_sentiment_by_condition.png')
                if chart:
                    st.image(chart, use_container_width=True)
                else:
                    st.info("Chart not found. Make sure EDA images are in the `/eda` folder.")

        st.markdown("---")
        st.markdown("<p class='section-header'>Dataset-Wide Text Analysis</p>", unsafe_allow_html=True)
        st.markdown("<p class='chart-note'>The following charts reflect patterns across the full dataset of 219,206 reviews — not specific to the selected drug or condition.</p>", unsafe_allow_html=True)

        viz_col1, viz_col2 = st.columns(2)
        with viz_col1:
            chart = find_chart('fig13_top_words.png')
            if chart:
                st.image(chart, caption="Most Frequent Words — Positive vs. Negative Reviews", use_container_width=True)
        with viz_col2:
            chart = find_chart('fig14_wordclouds.png')
            if chart:
                st.image(chart, caption="Word Clouds — Positive vs. Negative Reviews", use_container_width=True)


# ── TAB 2: Overall Dataset ─────────────────────────────────────────────────
with tab2:
    st.markdown("<p class='section-header'>Overall Dataset Summary</p>", unsafe_allow_html=True)

    overall_summary = clean_markdown(summaries['overall']['summary'])
    st.markdown(f"<div class='ai-summary-box'>{overall_summary}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-header'>Dataset Visualizations</p>", unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        chart = find_chart('fig1_rating_sentiment.png')
        if chart:
            st.image(chart, caption="Figure 1: Overall Rating Distribution & Sentiment Breakdown", use_container_width=True)
    with row1_col2:
        chart = find_chart('fig3_sentiment_by_condition.png')
        if chart:
            st.image(chart, caption="Figure 3: Sentiment Mix Across Top 10 Conditions", use_container_width=True)

    chart = find_chart('fig2_top_drugs_conditions.png')
    if chart:
        st.image(chart, caption="Figure 2: Top 15 Most Reviewed Drugs and Conditions", use_container_width=True)

    chart = find_chart('fig5_temporal_trends.png')
    if chart:
        st.image(chart, caption="Figure 5: Review Volume & Average Rating by Year (2008–2017)", use_container_width=True)

    st.markdown("<p class='section-header'>AI Evaluation</p>", unsafe_allow_html=True)
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        chart = find_chart('fig16_ai_evaluation.png')
        if chart:
            st.image(chart, caption="Figure 16: AI Qualitative Evaluation — Narrative Accuracy by Category", use_container_width=True)
    with row2_col2:
        chart = find_chart('fig17_ai_evaluation_table.png')
        if chart:
            st.image(chart, caption="Figure 17: AI Qualitative Evaluation Table", use_container_width=True)


# ── TAB 3: About ───────────────────────────────────────────────────────────
with tab3:
    st.markdown("<p class='section-header'>About This Tool</p>", unsafe_allow_html=True)

    st.markdown("""
    **Drug Review Insights & Summarization Tool** is an end-to-end AI-powered pipeline that analyzes
    patient drug reviews and generates plain-language summaries for pharmacists and healthcare researchers.

    #### How It Works
    1. **Data Ingestion & Preprocessing** — 219,206 patient reviews ingested from the UCI ML Drug Review Dataset,
    cleaned, and enriched with engineered features including sentiment labels and review length metrics.
    2. **Exploratory Data Analysis** — Rating distributions, sentiment patterns, temporal trends, word frequency
    analysis, and statistical testing across drugs and conditions.
    3. **AI Summarization** — Structured data profiles sent to the Google Gemini API to generate plain-language
    summaries at the overall, per-drug, and per-condition levels.
    4. **Evaluation** — AI narrative accuracy assessed qualitatively across three dimensions: sentiment tone,
    key themes, and drug comparison accuracy.
    5. **Pipeline Orchestration** — All four stages run end to end via a single master pipeline script.

    #### Dataset
    - **Source:** UCI ML Drug Review Dataset (Drugs.com) via Kaggle
    - **Size:** 219,206 reviews · 4,211 unique drugs · 2,724 conditions
    - **Date range:** 2008–2017
    - **Kaggle:** https://www.kaggle.com/datasets/jessicali9530/kuc-hackathon-winter-2018

    #### Team
    | Member | Contribution |
    |---|---|
    | Nancy Walker | Data ingestion and preprocessing |
    | Alexander Zhuk | API integration and prompt engineering |
    | Michael Ha | Exploratory data analysis and visualizations |
    | Mark Henry Villanueva | Pipeline integration, testing, and documentation |

    #### GitHub
    https://github.com/mvillanueva00/ADS-509-Final-Project

    ---
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='disclaimer'>
    ⚠️ <strong>Clinical Disclaimer:</strong> All summaries are derived from patient-reported reviews,
    not clinical trial data. This tool is intended for research and informational purposes only
    and should not be used as a substitute for professional medical advice or clinical guidance.
    </div>
    """, unsafe_allow_html=True)
