from ai_smart_test_selector.models.ml_model import train_model
from ai_smart_test_selector.pipeline.data import prepare_data


def train_pipeline():
    df = prepare_data()
    return train_model(df)
