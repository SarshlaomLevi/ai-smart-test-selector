import pytest
from ai_smart_test_selector.data.loader import load_data
from ai_smart_test_selector.models.feature_engineering import add_features
from ai_smart_test_selector.models.ml_model import train_model


# raw dataset (loaded once)
@pytest.fixture(scope="session")
def df():
    return load_data()


# engineered dataset (depends on df)
@pytest.fixture(scope="session")
def df_features(df):
    return add_features(df)


# trained model bundle (depends on df)
@pytest.fixture(scope="session")
def model_bundle(df):
    return train_model(df)