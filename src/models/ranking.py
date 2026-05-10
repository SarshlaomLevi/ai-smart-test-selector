def rank_tests(model, df):

    X = df[
        [
            "runtime_sec",
            "previous_failures",
            "run_count",
            "severity_score"
        ]
    ]

    probabilities = model.predict_proba(X)[:, 1]

    df = df.copy()
    df["failure_probability"] = probabilities

    # 🧠 הוספת הסבר (MVP explainability)
    def explain(row):
        if row["failure_probability"] > 0.7:
            return "High risk: frequent failures + high severity"
        elif row["failure_probability"] > 0.4:
            return "Medium risk: some instability detected"
        else:
            return "Low risk: stable test history"

    df["explanation"] = df.apply(explain, axis=1)

    return df.sort_values("failure_probability", ascending=False)