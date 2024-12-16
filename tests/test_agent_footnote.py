import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging
import json

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

from app import create_app
from app.models import db
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

class TestAgentFootnoteRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up TestAgentFootnoteRoutes class")
        # Set environment variable for testing
        os.environ['SCORE_THRESHOLD'] = '0.6'
        
        cls.app = create_app()
        cls.app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        # Clean up environment variable after tests
        if 'SCORE_THRESHOLD' in os.environ:
            del os.environ['SCORE_THRESHOLD']
        cls.ctx.pop()
        logger.info("Tearing down TestAgentFootnoteRoutes class")

    def setUp(self):
        logger.info(f"Setting up test: {self._testMethodName}")
        # Override any existing threshold value
        os.environ['SCORE_THRESHOLD'] = '0.6'  # Set threshold for testing

    def tearDown(self):
        logger.info(f"Tearing down test: {self._testMethodName}")
        
    @patch('app.routes.generate_footnote')
    def test_api_footnote_success(self, mock_generate):
        logger.info("Testing footnote API endpoint - success case")
        mock_generate.return_value = "Test footnote content"
        
        payload = {
            "text": "Sample text",
            "hc_name": "Test HC",
            "score": 0.8,
            "context": {"assignmentDescription": "Test assignment"}
        }
        
        response = self.client.post(
            '/api/footnote',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('footnote', data)
        self.assertEqual(data['footnote'], "Test footnote content")
        logger.info("Footnote API success test passed")

    def test_api_footnote_low_score(self):
        logger.info("Testing footnote API endpoint - low score case")
        payload = {
            "text": "Sample text",
            "hc_name": "Test HC",
            "score": 0.4,  # Score below threshold (0.6)
            "context": {"assignmentDescription": "Test assignment"}
        }
        
        response = self.client.post(
            '/api/footnote',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, 403, "Expected 403 for score below threshold")
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Score too low")

    def test_api_footnote_missing_fields(self):
        logger.info("Testing footnote API endpoint - missing fields")
        payload = {
            "text": "Sample text"
            # Missing required fields
        }
        
        response = self.client.post(
            '/api/footnote',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Missing required fields")
        logger.info("Footnote API missing fields test passed")

    def test_get_threshold_endpoint(self):
        logger.info("Testing get threshold endpoint")
        response = self.client.get('/api/threshold')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('threshold', data)
        self.assertIsInstance(data['threshold'], float)
        logger.info(f"Retrieved threshold: {data['threshold']}")

    @patch('app.routes.generate_footnote')
    def test_api_footnote_error_handling(self, mock_generate):
        logger.info("Testing footnote API endpoint - error handling")
        mock_generate.side_effect = Exception("Test error")
        
        payload = {
            "text": "Sample text",
            "hc_name": "Test HC",
            "score": 0.8
        }
        
        response = self.client.post(
            '/api/footnote',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
        logger.info("Footnote API error handling test passed")

if __name__ == '__main__':
    logger.info("Starting test suite execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAgentFootnote)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")

    logger.info("Starting test suite execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestAgentFootnoteRoutes)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
