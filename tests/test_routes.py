import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging
import json
from flask import Flask

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
from app.models import db, Cornerstone, HC, GuidedReflection, CommonPitfall

class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up TestRoutes class")
        cls.app = create_app()
        cls.app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        
        # Remove db.init_app(cls.app) since it's already initialized in create_app()

    def setUp(self):
        logger.info(f"Setting up test: {self._testMethodName}")
        with self.app.app_context():
            db.create_all()
            self._populate_test_data()

    def tearDown(self):
        logger.info(f"Tearing down test: {self._testMethodName}")
        db.session.remove()
        db.drop_all()

    @classmethod
    def tearDownClass(cls):
        logger.info("Tearing down TestRoutes class")
        cls.ctx.pop()

    def _populate_test_data(self):
        """Helper method to populate test data"""
        logger.info("Populating test data")
        logger.debug("Creating cornerstone with name 'TEST_CORNERSTONE'")
        
        # Create cornerstone with exact name to match URL
        cornerstone = Cornerstone(name="TEST_CORNERSTONE")
        db.session.add(cornerstone)
        db.session.commit()
        logger.info(f"Created cornerstone with id {cornerstone.id} and name {cornerstone.name}")

        hc = HC(
            name="Test HC",
            footnote="Test footnote",
            general_example="Test example",
            cornerstone_id=cornerstone.id
        )
        db.session.add(hc)
        db.session.commit()
        logger.info(f"Created HC: {hc.name}")

        reflection = GuidedReflection(text="Test reflection", hc_id=hc.id)
        pitfall = CommonPitfall(text="Test pitfall", hc_id=hc.id)
        db.session.add_all([reflection, pitfall])
        db.session.commit()
        logger.info("Test data populated successfully")

    def test_index_route(self):
        logger.info("Testing index route")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TEST_CORNERSTONE', response.data)

    def test_get_hcs_route(self):
        logger.info("Testing get_hcs route")
        # Add debug logging
        cornerstones = Cornerstone.query.all()
        logger.debug(f"Available cornerstones in DB: {[c.name for c in cornerstones]}")
        
        response = self.client.get('/api/hcs/TEST_CORNERSTONE')
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, 200, "Route should return 200 status code")
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list), "Response should be a list")
        self.assertTrue(len(data) > 0, "Response should not be empty")
        self.assertEqual(data[0]['name'], "Test HC")
        self.assertEqual(data[0]['cornerstone'], "TEST_CORNERSTONE")

    def test_get_all_hcs_route(self):
        logger.info("Testing get_all_hcs route")
        response = self.client.get('/api/hcs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue('TEST_CORNERSTONE' in data)

    @patch('app.routes.analyze_hc')
    def test_api_feedback_route(self, mock_analyze):
        logger.info("Testing api_feedback route")
        mock_analyze.return_value = {"feedback": "Test feedback"}
        
        payload = {
            "text": "test text",
            "hc_name": "Test HC",
            "guided_reflection": ["test reflection"],
            "common_pitfalls": ["test pitfall"],
            "context": {"assignmentDescription": "test"}
        }
        
        response = self.client.post(
            '/api/feedback',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["feedback"], "Test feedback")

    @patch('app.routes.check_input_quality')
    def test_api_precheck_route(self, mock_check):
        logger.info("Testing api_precheck route")
        mock_check.return_value = (True, "Good input")
        
        payload = {"text": "test text"}
        response = self.client.post(
            '/api/precheck',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["is_meaningful"])

if __name__ == '__main__':
    logger.info("Starting test suite execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestRoutes)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
