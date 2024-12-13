import pytest
from app import create_app
from app.models import db, HCExample


@pytest.fixture
def app():
    """Create application for the tests."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def init_database(app):
    """Initialize test database."""
    with app.app_context():
        db.create_all()
        example = HCExample(
            hc_name="test", general_example="Test example", footnote="Test footnote"
        )
        db.session.add(example)
        db.session.commit()
        yield db
        db.drop_all()


def test_index_route(client):
    """Test the index route."""
    response = client.get("/")
    assert response.status_code == 200


def test_get_hc_example(client, init_database):
    """Test getting a specific HC example."""
    response = client.get("/api/hc-example/test")
    assert response.status_code == 200
    data = response.get_json()
    assert data["general_example"] == "Test example"
    assert data["footnote"] == "Test footnote"


def test_get_nonexistent_hc_example(client, init_database):
    """Test getting a non-existent HC example."""
    response = client.get("/api/hc-example/nonexistent")
    assert response.status_code == 404


def test_get_all_hc_examples(client, app):
    """Test getting all HC examples."""
    with app.app_context():
        # Clear existing data
        db.session.query(HCExample).delete()

        # Add one test example
        example = HCExample(
            hc_name="test", general_example="Test example", footnote="Test footnote"
        )
        db.session.add(example)
        db.session.commit()

        response = client.get("/api/hc-examples")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["hc_name"] == "test"


def test_feedback_endpoint(client):
    """Test the feedback endpoint."""
    response = client.post("/api/feedback", json={"text": "Test feedback request"})
    assert response.status_code == 200
    data = response.get_json()
    assert "text" in data
    assert "actionable_steps" in data


def test_get_hc_examples(client, app):
    with app.app_context():
        # Clear existing data
        db.session.query(HCExample).delete()

        example = HCExample(
            hc_name="test_hc", general_example="Test example", footnote="Test footnote"
        )
        db.session.add(example)
        db.session.commit()

        response = client.get("/api/hc-examples")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["hc_name"] == "test_hc"


def test_get_specific_hc_example(client, app):
    with app.app_context():
        # Clear existing data
        db.session.query(HCExample).delete()

        example = HCExample(
            hc_name="specific_test",
            general_example="Specific test example",
            footnote="Specific test footnote",
        )
        db.session.add(example)
        db.session.commit()

        response = client.get("/api/hc-example/specific_test")
        assert response.status_code == 200
        data = response.get_json()
        assert data["general_example"] == "Specific test example"
        assert data["footnote"] == "Specific test footnote"
