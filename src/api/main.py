from fastapi import FastAPI
import pandas as pd

from src.data.loader import load_data
from src.models.feature_engineering import add_features
from src.models.ml_model import train_model
from src.models.ranking import rank_tests

app = FastAPI(
    title="AI Smart Test Selector API"
)

# Load system once
df = load_data()
df = add_features(df)

model = train_model(df)

ranked_df = rank_tests(model, df)

# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "AI Smart Test Selector API Running"
    }

# -----------------------------
# GET ALL TESTS
# -----------------------------
@app.get("/tests")
def get_tests():

    return ranked_df[
        [
            "test_name",
            "failure_probability",
            "explanation"
        ]
    ].to_dict(orient="records")

# -----------------------------
# GET TOP RISKY TESTS
# -----------------------------
@app.get("/top_risky")
def top_risky():

    top_df = ranked_df.sort_values(
        "failure_probability",
        ascending=False
    ).head(5)

    return top_df[
        [
            "test_name",
            "failure_probability",
            "explanation"
        ]
    ].to_dict(orient="records")