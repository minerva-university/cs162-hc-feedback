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

from app.ai.agent_precheck import check_input_quality

class TestAgentPrecheck(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up test case")

    def tearDown(self):
        logger.info("Tearing down test case")

    @patch('app.ai.agent_precheck.model')
    def test_check_input_quality_pass(self, mock_model):
        logger.info("Testing input quality check with PASS response")
        mock_response = MagicMock()
        mock_response.text = "VERDICT: PASS\nFEEDBACK: Good quality input"
        mock_model.generate_content.return_value = mock_response

        is_meaningful, feedback = check_input_quality("This is a meaningful text")
        logger.info(f"Check result - meaningful: {is_meaningful}, feedback: {feedback}")
        self.assertTrue(is_meaningful)
        self.assertEqual(feedback, "Good quality input")

    @patch('app.ai.agent_precheck.model')
    def test_check_input_quality_fail(self, mock_model):
        logger.info("Testing input quality check with FAIL response")
        mock_response = MagicMock()
        mock_response.text = "VERDICT: FAIL\nFEEDBACK: Input too short"
        mock_model.generate_content.return_value = mock_response

        is_meaningful, feedback = check_input_quality("test")
        logger.info(f"Check result - meaningful: {is_meaningful}, feedback: {feedback}")
        self.assertFalse(is_meaningful)
        self.assertEqual(feedback, "Input too short")

    @patch('app.ai.agent_precheck.model')
    def test_check_input_quality_error(self, mock_model):
        logger.info("Testing input quality check with error")
        mock_model.generate_content.side_effect = Exception("API Error")

        is_meaningful, feedback = check_input_quality("test")
        logger.info(f"Check result - meaningful: {is_meaningful}, feedback: {feedback}")
        self.assertFalse(is_meaningful)
        self.assertEqual(feedback, "Unable to evaluate input quality. Please try again.")

if __name__ == '__main__':
    logger.info("Starting test execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAgentPrecheck)
    test_result = unittest.TextTestRunner().run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
