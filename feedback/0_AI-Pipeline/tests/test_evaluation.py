import pytest
from evaluation import evaluate_all_criteria, evaluate_pitfall


@pytest.fixture(autouse=True)
def mock_api_key(monkeypatch):
    """Mock the CARL_API_KEY environment variable."""
    monkeypatch.setenv("CARL_API_KEY", "fake-api-key")


def test_evaluate_all_criteria():
    thesis = "Climate change is the biggest challenge of our time."
    results = evaluate_all_criteria(thesis)
    assert isinstance(results, list)
    assert all(isinstance(res, bool) for res in results)


def test_evaluate_pitfall():
    thesis = "Climate change is bad."
    pitfalls = ["The thesis is too vague or open-ended."]
    result = evaluate_pitfall(thesis, pitfalls)
    assert result in pitfalls or result is None
