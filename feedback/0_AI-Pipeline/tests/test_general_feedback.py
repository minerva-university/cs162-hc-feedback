import pytest
from general_feedback import generate_general_feedback
from pipeline_config import initialize_model


class MockAnalysisModel:
    """Mock class for the analysis model."""

    def generate_content(self, prompt):
        if "empty" in prompt:
            return None  # Simulate no response
        return MockResponse("This is mock feedback.")


class MockResponse:
    """Mock class for the model response."""

    def __init__(self, text):
        self.text = text


@pytest.fixture(autouse=True)
def mock_initialize_model(monkeypatch):
    """
    Mock the initialize_model function to return a mock analysis model.
    """

    def mock_model_initializer(model_type):
        assert model_type == "analysis", f"Unexpected model type: {model_type}"
        return MockAnalysisModel()

    monkeypatch.setattr("general_feedback.initialize_model", mock_model_initializer)


def test_generate_general_feedback_success():
    """
    Test that generate_general_feedback successfully returns feedback.
    """
    hc_text = "This is a valid HC statement for evaluation."
    feedback = generate_general_feedback(hc_text)
    assert feedback is not None, "Feedback should not be None for a valid HC text."
    assert isinstance(feedback, str), "Feedback should be a string."
    assert len(feedback) > 0, "Feedback should not be empty."


def test_generate_general_feedback_error_handling():
    """
    Test error handling when the HC text is invalid or empty.
    """
    invalid_hc_text = "   "  # Empty string with only whitespace
    feedback = generate_general_feedback(invalid_hc_text)
    assert feedback is None, "Feedback should be None for invalid HC text."


def test_generate_general_feedback_no_response(monkeypatch):
    """
    Test error handling when the model fails to generate a response.
    """

    class NoResponseModel:
        """Mock model that generates no response."""

        def generate_content(self, prompt):
            return None

    # Mock the model to simulate no response
    monkeypatch.setattr(
        "general_feedback.initialize_model", lambda model_type: NoResponseModel()
    )

    hc_text = "This is a valid HC statement for evaluation."
    feedback = generate_general_feedback(hc_text)
    assert (
        feedback is None
    ), "Feedback should be None if the model fails to generate a response."
