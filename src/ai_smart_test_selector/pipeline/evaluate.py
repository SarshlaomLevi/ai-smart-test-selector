from ai_smart_test_selector.evaluation.evaluate_model import evaluate_model


def evaluate_pipeline(model, X_test, y_test):
    return evaluate_model(model, X_test, y_test)
