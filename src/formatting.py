import pandas as pd


def clean_article_id(article_id):
    try:
        return str(int(float(article_id)))
    except Exception:
        return str(article_id)


def make_reason_label(score):
    try:
        score = float(score)
        if score >= 0.80:
            return "Very strong match"
        elif score >= 0.60:
            return "Strong match"
        elif score >= 0.40:
            return "Good match"
        else:
            return "Potential interest"
    except Exception:
        return "Recommended for you"


def prepare_display_df(recs_df: pd.DataFrame, articles_df: pd.DataFrame) -> pd.DataFrame:
    if recs_df.empty:
        return pd.DataFrame()

    df = recs_df.copy()
    articles = articles_df.copy()

    df.columns = df.columns.str.strip()
    articles.columns = articles.columns.str.strip()

    if "article_id" in df.columns:
        df["article_id"] = df["article_id"].apply(clean_article_id)

    if "article_id" in articles.columns:
        articles["article_id"] = articles["article_id"].apply(clean_article_id)

    possible_score_cols = [
        "score",
        "recommendation_score",
        "final_score",
        "similarity_score",
        "rank_score"
    ]
    score_col = next((col for col in possible_score_cols if col in df.columns), None)

    if score_col:
        df["raw_score"] = pd.to_numeric(df[score_col], errors="coerce")
    else:
        df["raw_score"] = pd.NA

    if df["raw_score"].notna().any():
        min_score = df["raw_score"].min()
        max_score = df["raw_score"].max()

        if max_score != min_score:
            df["score"] = (df["raw_score"] - min_score) / (max_score - min_score)
        else:
            df["score"] = 1.0
    else:
        df["score"] = pd.NA

    df["score_pct"] = df["score"].apply(
        lambda x: round(x * 100, 1) if pd.notna(x) else pd.NA
    )
    df["why_recommended"] = df["score"].apply(
        lambda x: make_reason_label(x) if pd.notna(x) else "Recommended for you"
    )

    article_fields = ["article_id"]
    possible_fields = [
        "prod_name",
        "product_type_name",
        "product_group_name",
        "graphical_appearance_name",
        "colour_group_name",
        "perceived_colour_value_name",
        "perceived_colour_master_name",
        "department_name",
        "index_name",
        "index_group_name",
        "section_name",
        "garment_group_name",
        "detail_desc"
    ]

    for col in possible_fields:
        if col in articles.columns:
            article_fields.append(col)

    article_lookup = articles[article_fields].drop_duplicates(subset=["article_id"])
    df = df.merge(article_lookup, on="article_id", how="left")

    if "prod_name" in df.columns:
        df["product_name"] = df["prod_name"].fillna("Unknown Product")
    else:
        df["product_name"] = df["article_id"].apply(lambda x: f"Product {x}")

    if "garment_group_name" not in df.columns:
        df["garment_group_name"] = "N/A"
    else:
        df["garment_group_name"] = df["garment_group_name"].fillna("N/A")

    if "product_type_name" not in df.columns:
        df["product_type_name"] = "N/A"
    else:
        df["product_type_name"] = df["product_type_name"].fillna("N/A")

    if "perceived_colour_master_name" in df.columns:
        df["display_color"] = df["perceived_colour_master_name"].fillna("N/A")
    elif "colour_group_name" in df.columns:
        df["display_color"] = df["colour_group_name"].fillna("N/A")
    else:
        df["display_color"] = "N/A"

    return df


def build_customer_segment_summary(display_df: pd.DataFrame) -> dict:
    if display_df.empty:
        return {
            "segment_name": "No profile available",
            "top_garment_group": "Mixed Style",
            "top_product_type": "Fashion Items",
            "top_color": "Varied Colors",
            "avg_match_score": "N/A"
        }

    def cleaned_mode(series, fallback):
        if series is None:
            return fallback

        series = series.dropna().astype(str)
        series = series[series.str.strip() != ""]
        series = series[series.str.upper() != "N/A"]

        if series.empty:
            return fallback

        mode_vals = series.mode()
        if mode_vals.empty:
            return fallback

        return mode_vals.iloc[0]

    top_garment_group = cleaned_mode(
        display_df["garment_group_name"] if "garment_group_name" in display_df.columns else None,
        "Mixed Style"
    )

    top_product_type = cleaned_mode(
        display_df["product_type_name"] if "product_type_name" in display_df.columns else None,
        "Fashion Items"
    )

    top_color = cleaned_mode(
        display_df["display_color"] if "display_color" in display_df.columns else None,
        "Varied Colors"
    )

    if "score_pct" in display_df.columns and display_df["score_pct"].notna().any():
        avg_match_score = f"{display_df['score_pct'].dropna().mean():.1f}%"
    else:
        avg_match_score = "N/A"

    segment_name = f"{top_color} {top_garment_group} Shopper"

    return {
        "segment_name": segment_name,
        "top_garment_group": top_garment_group,
        "top_product_type": top_product_type,
        "top_color": top_color,
        "avg_match_score": avg_match_score
    }