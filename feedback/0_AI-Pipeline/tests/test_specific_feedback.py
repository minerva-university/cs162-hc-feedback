import pytest
from unittest.mock import MagicMock, patch
from specific_feedback import (
    generate_checklist,
    generate_specific_feedback_for_criterion,
)


@pytest.fixture
def mock_model():
    """
    Fixture to mock the analysis model.
    """
    mock_model = MagicMock()
    mock_model.generate_content.return_value = MagicMock(text="Mocked response")
    with patch("specific_feedback.ANALYSIS_MODEL", mock_model):
        yield mock_model


@pytest.fixture
def mock_criteria_and_pitfalls():
    """
    Fixture to mock criteria and pitfalls evaluations.
    """
    with patch(
        "specific_feedback.evaluate_all_criteria", return_value=[False, True]
    ), patch("specific_feedback.evaluate_pitfall", return_value=False), patch(
        "specific_feedback.get_criteria", return_value=["Criterion 1", "Criterion 2"]
    ), patch(
        "specific_feedback.get_pitfalls", return_value=["Pitfall 1"]
    ):
        yield


def test_generate_checklist_success(mock_model, mock_criteria_and_pitfalls):
    """
    Test generate_checklist for a thesis text with failing criteria or pitfalls.
    """
    thesis_text = "This is a sample thesis text."
    feedback = generate_checklist(thesis_text)

    # Assert feedback contains the mocked response
    assert "Mocked response" in feedback, "Feedback should include the mocked response."


def test_generate_checklist_no_changes(mock_model):
    """
    Test generate_checklist for a thesis text with all passing criteria and no pitfalls.
    """
    with patch(
        "specific_feedback.evaluate_all_criteria", return_value=[True, True]
    ), patch("specific_feedback.evaluate_pitfall", return_value=True):
        thesis_text = "This is a perfect thesis text."
        feedback = generate_checklist(thesis_text)

        # Assert feedback indicates no changes are needed
        assert feedback == "No specific changes needed."


def test_generate_specific_feedback_for_criterion(mock_model):
    """
    Test generate_specific_feedback_for_criterion with a mocked model.
    """
    criterion = "The thesis should be concise."
    thesis_text = "This is a verbose thesis text."
    feedback = generate_specific_feedback_for_criterion(thesis_text, criterion)

    # Assert feedback matches the mocked response
    assert feedback == "Mocked response", "Feedback should match the mocked response."
