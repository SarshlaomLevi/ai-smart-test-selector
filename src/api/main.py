from fastapi import FastAPI
import pandas as pd

from src.data.loader import load_data
from src.models.feature_engineering import add_features
from src.models.ml_model import train_model
from src.models.ranking import rank_tests
from pydantic import BaseModel

app = FastAPI(
    title="AI Smart Test Selector API"
)

class TestInput(BaseModel):
    runtime_sec: int
    previous_failures: int
    run_count: int
    severity_score: int

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


# -----------------------------
# PREDICT TEST RISK
# -----------------------------
@app.post("/predict")
def predict(test: TestInput):

    input_df = pd.DataFrame(
        [{
            "runtime_sec": test.runtime_sec,
            "previous_failures": test.previous_failures,
            "run_count": test.run_count,
            "severity_score": test.severity_score
        }]
    )

    probability = model.predict_proba(input_df)[0][1]

    return {
        "failure_probability": round(float(probability), 2)
    }