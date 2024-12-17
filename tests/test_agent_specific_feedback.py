import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG to see all messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # Force configuration to ensure logging is visible
)
logger = logging.getLogger(__name__)

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

logger.debug(f"Python path: {sys.path}")

from app.ai.agent_specific_feedback import (
    generate_specific_feedback_for_criterion,
    evaluate_pitfall,
    format_feedback_for_display,
    generate_checklist
)

logger.debug("Starting test execution...")

class TestAgentSpecificFeedback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up TestAgentSpecificFeedback class")

    def setUp(self):
        logger.info(f"Setting up test case: {self._testMethodName}")

    def tearDown(self):
        logger.info("Tearing down test case")

    @patch('app.ai.agent_specific_feedback.analysis_model')
    def test_generate_specific_feedback(self, mock_model):
        logger.info("Testing specific feedback generation")
        mock_response = MagicMock()
        mock_response.text = "- [ ] Change: Fix grammar\n  From: bad grammar\n  To: good grammar\n  Why: Improves clarity"
        mock_model.generate_content.return_value = mock_response

        result = generate_specific_feedback_for_criterion("test text", "test criterion")
        logger.info(f"Generated feedback: {result}")
        self.assertIn("Change:", result)
        self.assertIn("From:", result)

    @patch('app.ai.agent_specific_feedback.analysis_model')
    def test_evaluate_pitfall(self, mock_model):
        logger.info("Testing pitfall evaluation")
        mock_response = MagicMock()
        mock_response.text = "PASS"
        mock_model.generate_content.return_value = mock_response

        result = evaluate_pitfall("test text", "test pitfall")
        logger.info(f"Pitfall evaluation result: {result}")
        self.assertTrue(result)

    def test_format_feedback_display(self):
        logger.info("Testing feedback formatting")
        test_items = ["- [ ] Change: A\n  From: X\n  To: Y\n  Why: Z"]
        result = format_feedback_for_display(test_items, include_why=False)
        logger.info(f"Formatted feedback: {result}")
        self.assertNotIn("Why:", result)

    @patch('app.ai.agent_specific_feedback.evaluate_all_criteria')
    @patch('app.ai.agent_specific_feedback.evaluate_pitfall')
    def test_generate_checklist(self, mock_pitfall, mock_criteria):
        logger.info("Testing checklist generation")
        mock_criteria.return_value = [False]
        mock_pitfall.return_value = True
        
        result = generate_checklist("test", ["criterion"], ["pitfall"])
        logger.info(f"Generated checklist: {result}")
        self.assertIsInstance(result, str)

    def test_basic_functionality(self):
        """Basic test to verify test execution"""
        logger.info("Running basic functionality test")
        self.assertTrue(True)

if __name__ == '__main__':
    logger.info("Starting test suite execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAgentSpecificFeedback)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
