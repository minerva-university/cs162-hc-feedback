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

logger.debug("Starting test file execution")
from app.ai.agent_precheck import check_input_quality

class TestPrecheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up TestPrecheck class")

    def setUp(self):
        logger.info(f"Setting up test: {self._testMethodName}")

    def tearDown(self):
        logger.info(f"Tearing down test: {self._testMethodName}")

    @patch('app.ai.agent_precheck.model')
    def test_check_input_quality_pass(self, mock_model):
        logger.info("Testing input quality check with PASS response")
        mock_response = MagicMock()
        mock_response.text = "VERDICT: PASS\nFEEDBACK: Good academic content with complete sentences"
        mock_model.generate_content.return_value = mock_response

        is_meaningful, feedback = check_input_quality("This is a well-written academic text.")
        logger.info(f"Check result - meaningful: {is_meaningful}, feedback: {feedback}")
        
        self.assertTrue(is_meaningful)
        self.assertEqual(feedback, "Good academic content with complete sentences")
        mock_model.generate_content.assert_called_once()

    @patch('app.ai.agent_precheck.model')
    def test_check_input_quality_fail(self, mock_model):
        logger.info("Testing input quality check with FAIL response")
        mock_response = MagicMock()
        mock_response.text = "VERDICT: FAIL\nFEEDBACK: Text is too short and lacks academic content"
        mock_model.generate_content.return_value = mock_response

        is_meaningful, feedback = check_input_quality("test")
        logger.info(f"Check result - meaningful: {is_meaningful}, feedback: {feedback}")
        
        self.assertFalse(is_meaningful)
        self.assertEqual(feedback, "Text is too short and lacks academic content")

    @patch('app.ai.agent_precheck.model')
    def test_check_input_quality_error(self, mock_model):
        logger.info("Testing input quality check with error handling")
        mock_model.generate_content.side_effect = Exception("API Error")

        is_meaningful, feedback = check_input_quality("test")
        logger.info(f"Check result - meaningful: {is_meaningful}, feedback: {feedback}")
        
        self.assertFalse(is_meaningful)
        self.assertEqual(feedback, "Unable to evaluate input quality. Please try again.")

if __name__ == '__main__':
    logger.info("Starting test suite execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPrecheck)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
