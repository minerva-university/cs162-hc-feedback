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

from app.ai.agent_evaluation import evaluate_criterion, evaluate_all_criteria

class TestAgentEvaluation(unittest.TestCase):
    def setUp(self):
        logger.info("Setting up test case")

    def tearDown(self):
        logger.info("Tearing down test case")

    @patch('app.ai.agent_evaluation.model')
    def test_evaluate_criterion_pass(self, mock_model):
        logger.info("Testing criterion evaluation with PASS response")
        # Mock the model's generate_content method to return a "PASS" response
        mock_response = MagicMock()
        mock_response.text = "PASS"
        mock_model.generate_content.return_value = mock_response

        assignment_text = "This is a sample assignment text."
        criterion = "Criterion 1"
        result = evaluate_criterion(assignment_text, criterion)
        
        self.assertTrue(result)
        mock_model.generate_content.assert_called_once()
        logger.info(f"Test result: {result}")

    @patch('app.ai.agent_evaluation.model')
    def test_evaluate_criterion_fail(self, mock_model):
        logger.info("Testing criterion evaluation with FAIL response")
        # Mock the model's generate_content method to return a "FAIL" response
        mock_response = MagicMock()
        mock_response.text = "FAIL"
        mock_model.generate_content.return_value = mock_response

        assignment_text = "This is a sample assignment text."
        criterion = "Criterion 1"
        result = evaluate_criterion(assignment_text, criterion)
        
        self.assertFalse(result)
        mock_model.generate_content.assert_called_once()
        logger.info(f"Test result: {result}")

    @patch('app.ai.agent_evaluation.evaluate_criterion')
    def test_evaluate_all_criteria(self, mock_evaluate_criterion):
        logger.info("Testing evaluation of multiple criteria")
        # Mock the evaluate_criterion function to return True for the first criterion and False for the second
        mock_evaluate_criterion.side_effect = [True, False]

        assignment_text = "This is a sample assignment text."
        criteria = ["Criterion 1", "Criterion 2"]
        results = evaluate_all_criteria(assignment_text, criteria)
        
        self.assertEqual(results, [True, False])
        self.assertEqual(mock_evaluate_criterion.call_count, 2)
        logger.info(f"Test results: {results}")

if __name__ == '__main__':
    logger.info("Starting test execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAgentEvaluation)
    test_result = unittest.TextTestRunner().run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
