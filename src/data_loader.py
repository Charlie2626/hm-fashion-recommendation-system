from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_data():
    recommendations_path = DATA_DIR / "recommendations_demo.csv"
    detailed_path = DATA_DIR / "recommendations_detailed_demo.csv"
    articles_path = DATA_DIR / "articles_demo.csv"

    recommendations_df = pd.read_csv(recommendations_path)
    detailed_df = pd.read_csv(detailed_path)
    articles_df = pd.read_csv(articles_path)

    return recommendations_df, detailed_df, articles_df
