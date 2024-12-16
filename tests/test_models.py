import pytest
from app.models import HCExample, db


def test_create_hc_example(app):
    example = HCExample(
        hc_name="test_example",
        general_example="This is a test example",
        footnote="Test footnote"
    )

    db.session.add(example)
    db.session.commit()

    assert example.id is not None
    assert example.hc_name == "test_example"
    assert example.general_example == "This is a test example"
    assert example.footnote == "Test footnote"


def test_query_hc_example(app):
    example = HCExample(
        hc_name="query_test",
        general_example="Query test example",
        footnote="Query test footnote"
    )

    db.session.add(example)
    db.session.commit()

    queried_example = HCExample.query.filter_by(hc_name="query_test").first()
    assert queried_example is not None
    assert queried_example.general_example == "Query test example"
