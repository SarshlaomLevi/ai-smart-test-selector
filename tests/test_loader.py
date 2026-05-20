import pytest

EXPECTED_COLUMNS = {
    "runtime_sec",
    "previous_failures",
    "run_count",
    "severity_score",
    "failed"
}

@pytest.mark.unit
def test_data_not_empty(df):
    assert len(df) > 0


@pytest.mark.unit
def test_expected_columns_exist(df):
    missing = EXPECTED_COLUMNS - set(df.columns)
    assert not missing, f"Missing columns: {missing}"