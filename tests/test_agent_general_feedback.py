import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

# Configure logging for tests
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from app.ai.agent_general_feedback import generate_general_feedback

class TestAgentGeneralFeedback(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up test case")

    def tearDown(self):
        logger.info("Tearing down test case")

    @patch('app.ai.agent_general_feedback.model')
    def test_generate_general_feedback(self, mock_model):
        logger.info("Testing general feedback generation")
        mock_response = MagicMock()
        mock_response.text = "This is general feedback"
        mock_model.generate_content.return_value = mock_response

        context = {
            "assignmentDescription": "Test assignment",
            "existingContext": "Test context"
        }
        
        result = generate_general_feedback("test text", ["criterion1"], context)
        logger.info(f"Generated feedback: {result}")
        self.assertEqual(result, "This is general feedback")
        mock_model.generate_content.assert_called_once()

    @patch('app.ai.agent_general_feedback.model')
    def test_generate_general_feedback_no_context(self, mock_model):
        logger.info("Testing general feedback generation without context")
        mock_response = MagicMock()
        mock_response.text = "General feedback without context"
        mock_model.generate_content.return_value = mock_response

        result = generate_general_feedback("test text", ["criterion1"])
        logger.info(f"Generated feedback: {result}")
        self.assertEqual(result, "General feedback without context")

if __name__ == '__main__':
    logger.info("Starting test execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAgentGeneralFeedback)
    test_result = unittest.TextTestRunner().run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
