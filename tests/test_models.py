import unittest
import sys
import os
import logging

# Configure logging for tests with forced configuration
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

from app.models import db, Cornerstone, HC, GuidedReflection, CommonPitfall

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up TestModels class")
        from flask import Flask
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        cls.app = app
        
    def setUp(self):
        logger.info(f"Setting up test: {self._testMethodName}")
        with self.app.app_context():
            db.create_all()
            
    def tearDown(self):
        logger.info("Tearing down test case")
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_cornerstone_creation(self):
        logger.info("Testing cornerstone creation")
        with self.app.app_context():
            cornerstone = Cornerstone(name="TEST_CORNERSTONE")
            db.session.add(cornerstone)
            db.session.commit()
            
            retrieved = Cornerstone.query.filter_by(name="TEST_CORNERSTONE").first()
            logger.info(f"Retrieved cornerstone: {retrieved.name}")
            self.assertEqual(retrieved.name, "TEST_CORNERSTONE")

    def test_hc_creation(self):
        logger.info("Testing HC creation")
        with self.app.app_context():
            cornerstone = Cornerstone(name="TEST_CORNERSTONE")
            db.session.add(cornerstone)
            db.session.commit()

            hc = HC(
                name="Test HC",
                footnote="Test footnote",
                general_example="Test example",
                cornerstone_id=cornerstone.id
            )
            db.session.add(hc)
            db.session.commit()

            retrieved = HC.query.filter_by(name="Test HC").first()
            logger.info(f"Retrieved HC: {retrieved.name}")
            self.assertEqual(retrieved.footnote, "Test footnote")
            self.assertEqual(retrieved.cornerstone.name, "TEST_CORNERSTONE")

    def test_relationships(self):
        logger.info("Testing model relationships")
        with self.app.app_context():
            # Create and commit cornerstone first
            cornerstone = Cornerstone(name="TEST_CORNERSTONE")
            db.session.add(cornerstone)
            db.session.commit()
            logger.info(f"Created cornerstone with id: {cornerstone.id}")

            # Create and commit HC
            hc = HC(
                name="Test HC",
                footnote="Test footnote",
                general_example="Test example",
                cornerstone_id=cornerstone.id
            )
            db.session.add(hc)
            db.session.commit()  # Commit to get the HC id
            logger.info(f"Created HC with id: {hc.id}")

            # Now create related models with proper HC id
            reflection = GuidedReflection(
                text="Test reflection", 
                hc_id=hc.id  # Explicitly set the hc_id
            )
            pitfall = CommonPitfall(
                text="Test pitfall", 
                hc_id=hc.id  # Explicitly set the hc_id
            )
            
            # Add and commit all at once
            db.session.add_all([reflection, pitfall])
            db.session.commit()
            logger.info("Added and committed related models")

            # Test the relationships
            self.assertEqual(len(cornerstone.hcs), 1)
            self.assertEqual(len(hc.guided_reflections), 1)
            self.assertEqual(len(hc.common_pitfalls), 1)
            logger.info("Relationship assertions passed")

if __name__ == '__main__':
    logger.info("Starting test suite execution")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestModels)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    logger.info(f"Test execution completed. Tests run: {test_result.testsRun}, "
               f"Failures: {len(test_result.failures)}, "
               f"Errors: {len(test_result.errors)}")
