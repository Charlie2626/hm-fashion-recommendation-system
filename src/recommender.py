import pandas as pd


def get_customer_recommendations(df: pd.DataFrame, customer_id: str, top_n=None) -> pd.DataFrame:
    temp = df.copy()
    temp.columns = temp.columns.str.strip()

    if "customer_id" not in temp.columns:
        return pd.DataFrame()

    temp["customer_id"] = temp["customer_id"].astype(str)
    customer_recs = temp[temp["customer_id"] == str(customer_id)].copy()

    if customer_recs.empty:
        return pd.DataFrame()

    possible_score_cols = [
        "score",
        "recommendation_score",
        "final_score",
        "similarity_score",
        "rank_score"
    ]
    score_col = next((col for col in possible_score_cols if col in customer_recs.columns), None)

    if score_col:
        customer_recs[score_col] = pd.to_numeric(customer_recs[score_col], errors="coerce")
        customer_recs = customer_recs.sort_values(by=score_col, ascending=False)

    customer_recs = customer_recs.reset_index(drop=True)

    if top_n is not None:
        return customer_recs.head(top_n)

    return customer_recs