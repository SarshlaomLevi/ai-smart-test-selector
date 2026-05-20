import pytest


@pytest.mark.unit
def test_feature_engineering_output(df_features):
    assert len(df_features) > 0

@pytest.mark.unit
def test_feature_engineering_adds_columns(df_features):
    assert "runtime_sec" in df_features.columns

# @pytest.mark.unit
# def test_risk_score_exists(df_features):
#     assert "risk_score" in df_features.columns

# @pytest.mark.unit
# def test_failure_ratio_exists(df_features):
#     assert "failure_ratio" in df_features.columns