from ai_smart_test_selector.evaluation.evaluate_model import evaluate_model
from ai_smart_test_selector.pipeline.train import train_pipeline


def evaluate_pipeline():
    model, X_test, y_test = train_pipeline()
    evaluate_model(model, X_test, y_test)
