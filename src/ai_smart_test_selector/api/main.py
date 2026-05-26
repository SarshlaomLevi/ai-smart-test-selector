from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd

from ai_smart_test_selector.data.loader import load_data
from ai_smart_test_selector.models.feature_engineering import add_features
from ai_smart_test_selector.models.ml_model import train_model
from ai_smart_test_selector.models.ranking import rank_tests


# =========================================================
# APP INIT
# =========================================================
app = FastAPI(title="AI Smart Test Selector API")


# =========================================================
# STATE INITIALIZATION (PRODUCTION SAFE)
# =========================================================
@app.on_event("startup")
def startup_event():
    """
    Load data + train model once when server starts
    """
    df = load_data()
    df = add_features(df)

    model, X_test, y_test = train_model(df)
    ranked_df = rank_tests(model, df)

    # store globally in app state (production pattern)
    app.state.model = model
    app.state.ranked_df = ranked_df


# =========================================================
# INPUT SCHEMA
# =========================================================
class TestInput(BaseModel):
    runtime_sec: int = Field(example=600)
    previous_failures: int = Field(example=5)
    run_count: int = Field(example=10)
    severity_score: int = Field(example=9)


# =========================================================
# HELPERS
# =========================================================
def get_ranked_df():
    return app.state.ranked_df


def get_model():
    return app.state.model


# =========================================================
# ENDPOINTS
# =========================================================


@app.get("/")
def root():
    return {"message": "AI Smart Test Selector API is running"}


@app.get("/rank-tests")
def rank_all_tests():
    df = get_ranked_df()

    return df[["test_name", "failure_probability", "explanation"]].to_dict(
        orient="records"
    )


@app.get("/available-tests")
def available_tests():
    df = get_ranked_df()

    return {"tests": df["test_name"].tolist()}


@app.get("/top-risky")
def top_risky_tests():
    df = get_ranked_df()

    top_df = df.sort_values("failure_probability", ascending=False).head(5)

    return top_df[["test_name", "failure_probability", "explanation"]].to_dict(
        orient="records"
    )


@app.get("/critical-tests")
def critical_tests():
    df = get_ranked_df()

    critical_df = df[df["failure_probability"] > 0.7]

    return critical_df[["test_name", "failure_probability", "explanation"]].to_dict(
        orient="records"
    )


@app.get("/simulate-test/{test_name}")
def simulate_test(test_name: str):
    df = get_ranked_df()

    selected = df[df["test_name"] == test_name]

    if selected.empty:
        return {"error": "Test not found"}

    row = selected.iloc[0]
    risk = float(row["failure_probability"])

    if risk > 0.85:
        result = "CRITICAL"
    elif risk > 0.7:
        result = "FAILED"
    elif risk > 0.4:
        result = "UNSTABLE"
    else:
        result = "PASSED"

    return {
        "test_name": row["test_name"],
        "risk": round(risk, 2),
        "result": result,
        "explanation": row["explanation"],
    }


@app.post("/predict")
def predict(test: TestInput):
    model = get_model()

    input_df = pd.DataFrame(
        [
            {
                "runtime_sec": test.runtime_sec,
                "previous_failures": test.previous_failures,
                "run_count": test.run_count,
                "severity_score": test.severity_score,
            }
        ]
    )

    probability = model.predict_proba(input_df)[0][1]

    if probability > 0.85:
        explanation = "Critical risk due to severe instability"
    elif probability > 0.7:
        explanation = "High risk due to frequent failures"
    elif probability > 0.4:
        explanation = "Medium risk due to unstable behavior"
    else:
        explanation = "Low risk and stable history"

    return {
        "failure_probability": round(float(probability), 2),
        "explanation": explanation,
    }
