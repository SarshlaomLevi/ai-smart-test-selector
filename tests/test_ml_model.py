# Ensures the training pipeline runs successfully without errors.
def test_model_training(model_bundle):
    model, X_test, y_test = model_bundle
    
    assert model is not None
    assert len(X_test) > 0
    assert len(y_test) > 0

# Ensures the trained model can make predictions.
def test_model_prediction(model_bundle):
    model, X_test, y_test = model_bundle

    predictions = model.predict(X_test)

    assert len(predictions) == len(y_test)
    assert set(predictions).issubset({0, 1})

def test_model_has_feature_importance(model_bundle):
    model, _, _ = model_bundle

    assert hasattr(model, "feature_importances_")