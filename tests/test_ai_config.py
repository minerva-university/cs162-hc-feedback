import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

# Configure logging for tests with forced configuration
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG to see all messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # Force configuration to ensure logging is visible
)
logger = logging.getLogger(__name__)

logger.debug("Starting test file execution")

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

logger.debug(f"Python path: {sys.path}")

from app.ai.ai_config import initialize_evaluation_model, initialize_analysis_model

logger.debug("Imports successful")

class TestAIConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up TestAIConfig class")
    
    def setUp(self):
        logger.info(f"Setting up test: {self._testMethodName}")

    def tearDown(self):
        logger.info("Tearing down test case")

    @patch('app.ai.ai_config.genai')
    def test_initialize_evaluation_model(self, mock_genai):
        logger.info("Testing evaluation model initialization")
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        result = initialize_evaluation_model()
        logger.info(f"Initialization result: {result}")
        self.assertIsNotNone(result)
        mock_genai.configure.assert_called_once()

    @patch('app.ai.ai_config.genai')
    def test_initialize_analysis_model(self, mock_genai):
        logger.info("Testing analysis model initialization")
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        result = initialize_analysis_model()
        logger.info(f"Initialization result: {result}")
        self.assertIsNotNone(result)
        mock_genai.configure.assert_called_once()

    @patch('app.ai.ai_config.genai')
    def test_model_initialization_failure(self, mock_genai):
        logger.info("Testing model initialization failure")
        mock_genai.configure.side_effect = Exception("API Error")
        
        result = initialize_evaluation_model()
        logger.info(f"Initialization result: {result}")
        self.assertIsNone(result)

if __name__ == '__main__':
    logger.info("Starting test suite execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAIConfig)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
