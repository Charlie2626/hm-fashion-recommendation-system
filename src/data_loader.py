import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data
def load_data():
    project_root = Path("/Users/charliebeverly/Desktop/H&M-Project")

    recommendations_path = "/Users/charliebeverly/Desktop/H&M-Project/phase5_final_recommendations.csv"
    detailed_path ="/Users/charliebeverly/Desktop/H&M-Project/phase5_final_recommendations_detailed.csv"
    articles_path ="/Users/charliebeverly/Desktop/H&M-Project/h-and-m-personalized-fashion-recommendations/articles.csv"

    recommendations_df = pd.read_csv(recommendations_path)
    detailed_df = pd.read_csv(detailed_path)
    articles_df = pd.read_csv(articles_path)

    recommendations_df.columns = recommendations_df.columns.str.strip()
    detailed_df.columns = detailed_df.columns.str.strip()
    articles_df.columns = articles_df.columns.str.strip()

    return recommendations_df, detailed_df, articles_df