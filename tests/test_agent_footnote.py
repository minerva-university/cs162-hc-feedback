import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from app.ai.agent_footnote import (
    generate_footnote,
    get_score_threshold,
    check_score_threshold
)

class TestAgentFootnote(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up TestAgentFootnote class")

    def setUp(self):
        logger.info(f"Setting up test: {self._testMethodName}")
        # Reset environment variables before each test
        if 'SCORE_THRESHOLD' in os.environ:
            del os.environ['SCORE_THRESHOLD']

    def tearDown(self):
        logger.info(f"Tearing down test: {self._testMethodName}")

    def test_get_score_threshold_default(self):
        logger.info("Testing get_score_threshold with default value")
        threshold = get_score_threshold()
        self.assertEqual(threshold, 0.01)
        logger.info(f"Default threshold verified: {threshold}")

    def test_get_score_threshold_env_var(self):
        logger.info("Testing get_score_threshold with environment variable")
        os.environ['SCORE_THRESHOLD'] = '0.05'
        threshold = get_score_threshold()
        self.assertEqual(threshold, 0.05)
        logger.info(f"Environment variable threshold verified: {threshold}")

    def test_get_score_threshold_invalid_env_var(self):
        logger.info("Testing get_score_threshold with invalid environment variable")
        os.environ['SCORE_THRESHOLD'] = 'invalid'
        threshold = get_score_threshold()
        self.assertEqual(threshold, 0.01)  # Should fall back to default
        logger.info("Invalid threshold handled correctly")

    def test_check_score_threshold_pass(self):
        logger.info("Testing check_score_threshold with passing score")
        os.environ['SCORE_THRESHOLD'] = '0.5'
        result = check_score_threshold(0.7)
        self.assertTrue(result)
        logger.info("Score threshold check passed as expected")

    def test_check_score_threshold_fail(self):
        logger.info("Testing check_score_threshold with failing score")
        os.environ['SCORE_THRESHOLD'] = '0.5'
        result = check_score_threshold(0.3)
        self.assertFalse(result)
        logger.info("Score threshold check failed as expected")

    @patch('app.ai.agent_footnote.model')
    def test_generate_footnote_success(self, mock_model):
        logger.info("Testing footnote generation - success case")
        mock_response = MagicMock()
        mock_response.text = "In this essay, I consciously applied..."
        mock_model.generate_content.return_value = mock_response

        result = generate_footnote(
            assignment_text="Sample text",
            hc_name="Test HC",
            context={"assignmentDescription": "Test assignment"}
        )
        
        logger.info(f"Generated footnote: {result}")
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, str))
        mock_model.generate_content.assert_called_once()

    @patch('app.ai.agent_footnote.model')
    def test_generate_footnote_with_context(self, mock_model):
        logger.info("Testing footnote generation with full context")
        mock_response = MagicMock()
        mock_response.text = "Context-aware footnote"
        mock_model.generate_content.return_value = mock_response

        context = {
            "assignmentDescription": "Test assignment",
            "existingContext": "Additional context"
        }
        
        result = generate_footnote("Sample text", "Test HC", context)
        logger.info(f"Generated footnote with context: {result}")
        self.assertIn("Context-aware footnote", result)

    @patch('app.ai.agent_footnote.model')
    def test_generate_footnote_error(self, mock_model):
        logger.info("Testing footnote generation - error case")
        mock_model.generate_content.side_effect = Exception("API Error")

        result = generate_footnote("Sample text", "Test HC")
        logger.info("Verified error handling")
        self.assertIsNone(result)

if __name__ == '__main__':
    logger.info("Starting test suite execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAgentFootnote)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
