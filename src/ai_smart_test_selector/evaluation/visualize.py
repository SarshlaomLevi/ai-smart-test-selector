import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()


def plot_feature_importance(model, X_test):
    importance = model.feature_importances_

    df = pd.DataFrame(
        {"feature": X_test.columns, "importance": importance}
    ).sort_values("importance", ascending=False)

    plt.figure(figsize=(6, 4))
    sns.barplot(data=df, x="importance", y="feature")
    plt.title("Feature Importance")
    plt.tight_layout()
    plt.show()
