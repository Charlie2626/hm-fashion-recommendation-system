from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_data():
    recommendations_df = pd.read_csv(DATA_DIR / "recommendations_demo.csv")
    articles_df = pd.read_csv(DATA_DIR / "articles_demo.csv")

    detailed_df = recommendations_df.copy()

    return recommendations_df, detailed_df, articles_df
