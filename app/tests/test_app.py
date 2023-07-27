import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


def test_get_bills_empty(test_client):
    response = test_client.get("/v1/bills")
    assert response.status_code == 200
    assert response.json() == []


# def test_get_bills_with_data(test_client, session):
#     # Assuming you have a test database with sample bills data in the "session" fixture

#     response = test_client.get("/")
#     assert response.status_code == 200
#     assert len(response.json()) > 0
#     # You can also add more specific checks based on your test data and expected results
