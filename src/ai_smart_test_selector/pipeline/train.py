from ai_smart_test_selector.models.ml_model import train_model
from ai_smart_test_selector.pipeline.data import prepare_data


def train_pipeline():
    df = prepare_data()
    model, X_test, y_test = train_model(df)
    return model, X_test, y_test
