from ai_smart_test_selector.data.loader import load_data
from ai_smart_test_selector.models.feature_engineering import add_features
from ai_smart_test_selector.models.ml_model import train_model
from ai_smart_test_selector.evaluation.evaluate_model import evaluate_model

import argparse

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix


def main():
    parser = argparse.ArgumentParser(description="AI Smart Test Selector")

    parser.add_argument("--train", action="store_true", help="Train model pipeline")

    parser.add_argument("--evaluate", action="store_true", help="Run evaluation only")

    parser.add_argument(
        "--run-all", action="store_true", help="Run full pipeline (train + evaluate)"
    )

    args, _ = parser.parse_known_args()

    # -------------------------
    # 1. LOAD DATA
    # -------------------------
    df = load_data()
    df = add_features(df)

    model = None
    X_test = None
    y_test = None

    # -------------------------
    # 2. TRAIN MODEL
    # -------------------------
    if args.train or args.run_all or (not args.train and not args.evaluate):
        print("🚀 Training model...")
        model, X_test, y_test = train_model(df)

    # -------------------------
    # 3. EVALUATION
    # -------------------------
    if args.evaluate or args.run_all or (not args.train):
        print("📊 Evaluating model...")

        if model is None:
            model, X_test, y_test = train_model(df)

        evaluate_model(model, X_test, y_test)

        # -------------------------
        # 4. CONFUSION MATRIX
        # -------------------------
        cm = confusion_matrix(y_test, model.predict(X_test))

        plt.figure(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.tight_layout()
        plt.show()

        # -------------------------
        # 5. FEATURE IMPORTANCE
        # -------------------------
        importance = model.feature_importances_
        features = X_test.columns

        df_importance = pd.DataFrame(
            {"feature": features, "importance": importance}
        ).sort_values("importance", ascending=False)

        plt.figure(figsize=(6, 4))

        sns.barplot(data=df_importance, x="importance", y="feature")

        plt.title("Feature Importance")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
