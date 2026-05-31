import pytest
from ai_smart_test_selector.pipeline.data import prepare_data
from ai_smart_test_selector.models.ml_model import train_model
from fastapi.testclient import TestClient
from ai_smart_test_selector.api.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def df():
    return prepare_data()


@pytest.fixture
def df_features():
    return prepare_data()


@pytest.fixture
def model_bundle(df_features):
    model, X_test, y_test = train_model(df_features)
    return model, X_test, y_test
