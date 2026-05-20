import pytest

@pytest.mark.smoke
def test_package_import():
    import ai_smart_test_selector
    assert ai_smart_test_selector.__name__ == "ai_smart_test_selector"


@pytest.mark.smoke
def test_core_imports():
    from ai_smart_test_selector.data.loader import load_data
    from ai_smart_test_selector.models.ml_model import train_model
    assert callable(load_data)
    assert callable(train_model)