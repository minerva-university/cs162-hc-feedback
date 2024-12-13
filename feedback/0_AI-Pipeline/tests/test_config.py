import pytest
from pipeline_config import (
    get_criteria,
    get_pitfalls,
    get_single_criterion,
    initialize_model,
)
from google.generativeai import GenerativeModel


def test_get_criteria():
    """
    Test that get_criteria returns the correct list of criteria.
    """
    criteria = get_criteria()
    assert isinstance(criteria, list), "Criteria should be a list."
    assert len(criteria) > 0, "Criteria list should not be empty."
    assert all(
        isinstance(c, str) for c in criteria
    ), "Each criterion should be a string."


def test_get_pitfalls():
    """
    Test that get_pitfalls returns the correct list of pitfalls.
    """
    pitfalls = get_pitfalls()
    assert isinstance(pitfalls, list), "Pitfalls should be a list."
    assert len(pitfalls) > 0, "Pitfalls list should not be empty."
    assert all(isinstance(p, str) for p in pitfalls), "Each pitfall should be a string."


@pytest.mark.parametrize(
    "index, expected_result",
    [
        (
            0,
            "Ensure your thesis is substantial, precise, relevant, arguable, concise, and sets up the forthcoming evidence.",
        ),
        (1, "Ensure your thesis is appropriate in terms of scope."),
        (10, None),  # Out-of-range index
    ],
)
def test_get_single_criterion(index, expected_result):
    """
    Test that get_single_criterion returns the correct criterion or None for invalid indices.
    """
    result = get_single_criterion(index)
    if expected_result is None:
        assert result is None, f"Expected None for index {index}, but got {result}."
    else:
        assert (
            result == expected_result
        ), f"Expected '{expected_result}' but got '{result}'."


def test_initialize_evaluation_model(monkeypatch):
    """
    Test that initialize_model initializes an evaluation model correctly.
    """
    # Mock API key
    monkeypatch.setenv("CARL_API_KEY", "fake-api-key")

    model = initialize_model(model_type="evaluation")
    assert model is not None, "Evaluation model should be initialized."


def test_initialize_analysis_model(monkeypatch):
    """
    Test that initialize_model initializes an analysis model correctly.
    """
    # Mock API key
    monkeypatch.setenv("CARL_API_KEY", "fake-api-key")

    model = initialize_model(model_type="analysis")
    assert model is not None, "Analysis model should be initialized."


def test_initialize_model_missing_api_key(monkeypatch):
    """
    Test that initialize_model fails gracefully when API key is missing.
    """
    # Ensure the environment variable is not set
    monkeypatch.delenv("CARL_API_KEY", raising=False)

    with pytest.raises(ValueError, match="API Key is missing"):
        initialize_model(model_type="evaluation")


def test_initialize_model_invalid_type(monkeypatch):
    """
    Test that initialize_model handles an invalid model type gracefully.
    """
    # Mock API key
    monkeypatch.setenv("CARL_API_KEY", "fake-api-key")

    with pytest.raises(ValueError, match="Invalid model type"):
        initialize_model(model_type="invalid_type")
