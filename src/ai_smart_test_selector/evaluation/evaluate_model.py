from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report,
)


def evaluate_model(model, X_test, y_test):
    """
    Runs model evaluation and returns metrics only.
    No printing, no visualization (clean production design).
    """

    # -------------------------
    # 1. Predictions
    # -------------------------
    predictions = model.predict(X_test)

    # -------------------------
    # 2. Metrics calculation
    # -------------------------
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)

    matrix = confusion_matrix(y_test, predictions)
    report = classification_report(y_test, predictions)

    # -------------------------
    # 3. Return structured results
    # -------------------------
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "confusion_matrix": matrix,
        "report": report,
    }
