import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def show_score_chart(df):
    if "product_name" not in df.columns or "score" not in df.columns:
        st.info("No score column available.")
        return

    chart_df = df.copy()
    chart_df["score"] = pd.to_numeric(chart_df["score"], errors="coerce")
    chart_df = chart_df.dropna(subset=["score"])

    if chart_df.empty:
        st.info("No numeric scores available to plot.")
        return

    chart_df = chart_df.sort_values("score", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(chart_df["product_name"], chart_df["score"])
    ax.set_xlabel("Normalized Score")
    ax.set_ylabel("Product")
    ax.set_title("Recommendation Scores")
    ax.set_xlim(0, 1)

    st.pyplot(fig)


@st.cache_data
def build_image_index(image_root):
    image_root = Path(image_root)

    if not image_root.exists():
        return {}

    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    image_index = {}

    for path in image_root.rglob("*"):
        if path.is_file() and path.suffix.lower() in valid_exts:
            stem = path.stem.strip()
            image_index[stem] = str(path)

            stripped = stem.lstrip("0")
            if stripped:
                image_index[stripped] = str(path)

    return image_index


def get_product_image_path(
    article_id,
    image_root="/Users/charliebeverly/Desktop/H&M-Project/h-and-m-personalized-fashion-recommendations/images"
):
    article_id = str(article_id).strip()
    padded_id = article_id.zfill(10)
    stripped_id = article_id.lstrip("0")

    image_index = build_image_index(image_root)

    if padded_id in image_index:
        return image_index[padded_id]

    if stripped_id in image_index:
        return image_index[stripped_id]

    return None