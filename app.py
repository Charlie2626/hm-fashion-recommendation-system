import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.recommender import get_customer_recommendations
from src.formatting import prepare_display_df, build_customer_segment_summary
from src.visuals import show_score_chart, get_product_image_path

st.set_page_config(
    page_title="H&M Personalized Recommendations",
    layout="wide"
)

st.markdown("""
<style>
/* Main page spacing */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* App background */
[data-testid="stAppViewContainer"] {
    background-color: #f7f8fc;
}

/* Section titles */
.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 0.75rem;
    color: #1f2937;
}

/* Hero / summary card */
.summary-card {
    background: white;
    padding: 1.25rem 1.5rem;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    border: 1px solid #eceff5;
    margin-bottom: 1rem;
}

/* KPI cards */
.kpi-card {
    background: white;
    padding: 1rem 1.2rem;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    border: 1px solid #eceff5;
    text-align: center;
}

.kpi-label {
    font-size: 0.9rem;
    color: #6b7280;
    margin-bottom: 0.35rem;
}

.kpi-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #111827;
}

/* Recommendation card */
.rec-card {
    background: white;
    border-radius: 18px;
    padding: 1rem;
    border: 1px solid #eceff5;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
    min-height: 100%;
}

.rec-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #111827;
    margin-top: 0.6rem;
    margin-bottom: 0.25rem;
}

.rec-meta {
    font-size: 0.9rem;
    color: #6b7280;
    margin-bottom: 0.6rem;
}

.rec-badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    background: #eef2ff;
    color: #4338ca;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 0.35rem;
    margin-bottom: 0.5rem;
}

/* Score area */
.score-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 0.35rem;
}
</style>
""", unsafe_allow_html=True)


def render_recommendation_card(row, image_root):
    article_id = row.get("article_id", "Unknown")
    product_name = row.get("product_name", f"Product {article_id}")
    garment_group = row.get("garment_group_name", "N/A")
    product_type = row.get("product_type_name", "N/A")
    display_color = row.get("display_color", "N/A")
    why_recommended = row.get("why_recommended", "Recommended for you")
    score = row.get("score", None)
    score_pct = row.get("score_pct", None)

    image_path = get_product_image_path(article_id)

    st.markdown('<div class="rec-card">', unsafe_allow_html=True)

    if image_path:
        st.image(image_path, use_container_width=True)
    else:
        st.info("No image found")

    st.markdown(
        f'<div class="rec-title">{product_name}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="rec-meta">{garment_group} • {product_type} • {display_color}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<span class="rec-badge">{why_recommended}</span>',
        unsafe_allow_html=True
    )

    if pd.notna(score_pct):
        st.markdown(
            f'<div class="score-label">Recommendation Strength: {float(score_pct):.1f}%</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="score-label">Recommendation Strength: N/A</div>',
            unsafe_allow_html=True
        )

    if pd.notna(score):
        st.progress(float(score))

    st.caption(f"Article ID: {article_id}")
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
st.title("H&M Personalized Fashion Recommendations")
st.caption("A cleaner recommendation dashboard with customer summary, KPIs, cards, and score visuals.")

# -----------------------------
# Load data
# -----------------------------
recommendations_df, detailed_df, articles_df = load_data()

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Customer Selection")

data_source = st.sidebar.selectbox(
    "Recommendation source",
    ["Detailed Recommendations", "Final Recommendations"]
)

active_df = detailed_df if data_source == "Detailed Recommendations" else recommendations_df

customer_ids = sorted(active_df["customer_id"].astype(str).unique().tolist())
selected_customer = st.sidebar.selectbox("Select customer", customer_ids)

# Pull enough rows first, then do in-page filtering/sorting
customer_recs = get_customer_recommendations(
    df=active_df,
    customer_id=selected_customer,
    top_n=None
)

display_df = prepare_display_df(customer_recs, articles_df)
segment_summary = build_customer_segment_summary(display_df)

# -----------------------------
# In-page controls
# -----------------------------
st.markdown('<div class="section-title">Controls</div>', unsafe_allow_html=True)

control1, control2, control3 = st.columns([1, 1, 2])

with control1:
    top_n = st.slider("Top N Recommendations", min_value=1, max_value=12, value=6)

with control2:
    sort_option = st.selectbox("Sort By", ["Score", "Product Name", "Category"])

with control3:
    category_options = ["All"]
    if "product_type_name" in display_df.columns:
        valid_categories = (
            display_df["product_type_name"]
            .dropna()
            .astype(str)
            .loc[lambda s: s.str.strip() != ""]
            .unique()
            .tolist()
        )
        category_options += sorted(valid_categories)

    selected_category = st.selectbox("Filter Category", category_options)

filtered_df = display_df.copy()

if selected_category != "All" and "product_type_name" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["product_type_name"] == selected_category]

if sort_option == "Score" and "score" in filtered_df.columns:
    filtered_df = filtered_df.sort_values("score", ascending=False)
elif sort_option == "Product Name" and "product_name" in filtered_df.columns:
    filtered_df = filtered_df.sort_values("product_name", ascending=True)
elif sort_option == "Category" and "product_type_name" in filtered_df.columns:
    filtered_df = filtered_df.sort_values(["product_type_name", "product_name"], ascending=True)

filtered_df = filtered_df.head(top_n).reset_index(drop=True)

# -----------------------------
# Summary card
# -----------------------------
st.markdown(
    f"""
    <div class="summary-card">
        <div style="font-size:1.35rem; font-weight:700; color:#111827;">
            Customer {selected_customer}
        </div>
        <div style="margin-top:0.55rem; color:#4b5563; font-size:1rem; line-height:1.7;">
            <b>Segment:</b> {segment_summary["segment_name"]}<br>
            <b>Top Garment Group:</b> {segment_summary["top_garment_group"]} &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>Top Product Type:</b> {segment_summary["top_product_type"]} &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>Top Color:</b> {segment_summary["top_color"]} &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>Avg Match Score:</b> {segment_summary["avg_match_score"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# KPI cards
# -----------------------------
st.markdown('<div class="section-title">Recommendation Snapshot</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

top_score = round(filtered_df["score"].max(), 3) if not filtered_df.empty and "score" in filtered_df.columns else 0
avg_score = round(filtered_df["score"].mean(), 3) if not filtered_df.empty and "score" in filtered_df.columns else 0
num_recs = len(filtered_df)
unique_categories = filtered_df["product_type_name"].nunique() if "product_type_name" in filtered_df.columns else 0

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Top Score</div>
        <div class="kpi-value">{top_score}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Average Score</div>
        <div class="kpi-value">{avg_score}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Recommendations</div>
        <div class="kpi-value">{num_recs}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Categories</div>
        <div class="kpi-value">{unique_categories}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Main content
# -----------------------------
left_col, right_col = st.columns([2.2, 1])

with left_col:
    st.markdown('<div class="section-title">Top Recommendations</div>', unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("No recommendations found for this customer.")
    else:
        for i in range(0, len(filtered_df), 2):
            pair = filtered_df.iloc[i:i + 2]
            cols = st.columns(2)

            for idx, (_, row) in enumerate(pair.iterrows()):
                with cols[idx]:
                    render_recommendation_card(
                        row=row,
                    )

with right_col:
    st.markdown('<div class="section-title">Score Chart</div>', unsafe_allow_html=True)

    if not filtered_df.empty and "score" in filtered_df.columns:
        show_score_chart(filtered_df)
    else:
        st.info("No score data available.")

# -----------------------------
# Optional detailed table
# -----------------------------
with st.expander("Show recommendation table"):
    if filtered_df.empty:
        st.info("No rows to display.")
    else:
        table_df = filtered_df.copy()

        if "score_pct" in table_df.columns:
            table_df["score_pct"] = table_df["score_pct"].apply(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
            )

        columns_to_show = [
            "article_id",
            "product_name",
            "garment_group_name",
            "product_type_name",
            "display_color",
            "score_pct",
            "why_recommended"
        ]
        existing_cols = [col for col in columns_to_show if col in table_df.columns]
        st.dataframe(table_df[existing_cols], use_container_width=True)
