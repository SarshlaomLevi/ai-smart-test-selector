import sys
import os

# Allows import from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix

from src.data.loader import load_data
from src.models.feature_engineering import add_features
from src.models.ml_model import train_model
from src.models.ranking import rank_tests


# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="AI Smart Test Selector",
    layout="wide"
)

st.title("🧠 AI Smart Test Selector for Firmware Validation")


# -------------------------
# LOAD + PREPROCESS
# -------------------------
df = load_data()
df = add_features(df)


# -------------------------
# TRAIN MODEL
# -------------------------
model, X_test, y_test = train_model(df)


# -------------------------
# RANKING
# -------------------------
ranked_df = rank_tests(model, df)


# -------------------------
# KPI SECTION
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Tests", len(ranked_df))
col2.metric(
    "High Risk Tests",
    len(ranked_df[ranked_df["failure_probability"] > 0.7])
)
col3.metric(
    "Avg Risk",
    f"{ranked_df['failure_probability'].mean():.2f}"
)

st.divider()


# -------------------------
# FILTERS
# -------------------------
st.sidebar.header("🎯 Filters")

min_risk = st.sidebar.slider("Min Risk", 0.0, 1.0, 0.0)
max_risk = st.sidebar.slider("Max Risk", 0.0, 1.0, 1.0)

filtered_df = ranked_df[
    (ranked_df["failure_probability"] >= min_risk) &
    (ranked_df["failure_probability"] <= max_risk)
]


# -------------------------
# SELECT TEST
# -------------------------
selected_test = st.sidebar.selectbox(
    "Select Test",
    filtered_df["test_name"].tolist()
)

selected_row = filtered_df[
    filtered_df["test_name"] == selected_test
]

st.subheader("📌 Selected Test")
st.dataframe(selected_row)


# -------------------------
# RANKING TABLE
# -------------------------
# st.subheader("📊 Ranked Tests")

# for _, row in filtered_df.iterrows():

#     col1, col2, col3 = st.columns([2, 2, 4])

#     with col1:
#         st.write(row["test_name"])

#     with col2:
#         st.write(f"{row['failure_probability']:.2f}")

#     with col3:
#         st.write(row.get("explanation", "No explanation"))

#     st.divider()

# -------------------------
# INTERACTIVE RANKING
# -------------------------
st.subheader("📊 AI Test Ranking")

for _, row in filtered_df.iterrows():

    risk = row["failure_probability"]

    # Risk classification
    if risk > 0.85:
        risk_label = "🔥 CRITICAL RISK"

    elif risk > 0.7:
        risk_label = "🔴 HIGH RISK"

    elif risk > 0.4:
        risk_label = "🟡 MEDIUM RISK"

    else:
        risk_label = "🟢 LOW RISK"

    with st.expander(
        f"{row['test_name']} | Risk: {risk:.2f} | {risk_label}"
    ):

        st.write("### 🧠 AI Explanation")
        st.info(row.get("explanation", "No explanation available"))

        st.write("### 📊 Test Data")

        st.dataframe(
            pd.DataFrame({
                "Metric": [
                    "Runtime (sec)",
                    "Previous Failures",
                    "Run Count",
                    "Severity Score"
                ],
                "Value": [
                    row["runtime_sec"],
                    row["previous_failures"],
                    row["run_count"],
                    row["severity_score"]
                ]
            }),
            use_container_width=True
        )

        st.write("### 🎯 Recommended Action")

        if risk > 0.85:

            st.error(
                "🔥 Critical risk detected.\n\n"
                "- Run immediately in smoke testing\n"
                "- Monitor logs closely\n"
                "- Notify firmware owner if failed"
            )

        elif risk > 0.7:

            st.warning(
                "⚠️ High-risk test.\n\n"
                "- Run early in regression\n"
                "- Prioritize in validation cycle\n"
                "- Recommended for daily execution"
            )

        elif risk > 0.4:

            st.info(
                "🟡 Medium-risk test.\n\n"
                "- Monitor stability trends\n"
                "- Include in standard regression\n"
                "- Investigate if failure frequency increases"
            )

        else:

            st.success(
                "✅ Stable low-risk test.\n\n"
                "- Safe for nightly execution\n"
                "- Lower execution priority\n"
                "- Minimal monitoring required"
            ) 


# -------------------------
# SIMULATION
# -------------------------
st.subheader("🧪 Test Simulation")

if st.button(f"Run {selected_test}"):

    prob = float(selected_row["failure_probability"])

    if prob > 0.7:
        st.error("❌ Test FAILED (High risk detected)")
    elif prob > 0.4:
        st.warning("⚠️ Test unstable")
    else:
        st.success("✅ Test PASSED")


# -------------------------
# RISK DISTRIBUTION
# -------------------------
st.subheader("📈 Risk Distribution")

st.bar_chart(
    filtered_df.set_index("test_name")["failure_probability"]
)


# -------------------------
# TOP RISKY TESTS
# -------------------------
st.subheader("🔥 Top Risky Tests")

st.dataframe(
    filtered_df.sort_values(
        "failure_probability",
        ascending=False
    ).head(5)
)


# -------------------------
# EXPORT CSV
# -------------------------
st.subheader("📦 Generate Release Test Suite")

release_df = filtered_df.sort_values(
    "failure_probability",
    ascending=False
).head(5)

csv = release_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Release Test Suite CSV",
    data=csv,
    file_name="release_test_suite.csv",
    mime="text/csv"
)


# -------------------------
# CONFUSION MATRIX
# -------------------------
st.subheader("📊 Confusion Matrix")

cm = confusion_matrix(y_test, model.predict(X_test))

fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)

ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")

st.pyplot(fig)


# -------------------------
# FEATURE IMPORTANCE
# -------------------------
st.subheader("📈 Feature Importance")

importance = model.feature_importances_
features = X_test.columns

df_imp = pd.DataFrame({
    "feature": features,
    "importance": importance
}).sort_values("importance", ascending=False)

fig2, ax2 = plt.subplots()

sns.barplot(
    data=df_imp,
    x="importance",
    y="feature",
    ax=ax2
)

st.pyplot(fig2)