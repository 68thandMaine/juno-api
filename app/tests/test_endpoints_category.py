from fastapi.testclient import TestClient
import pytest
from app.api.endpoints.category import router
from app.models import Category

CATEGORY_ENDPOINT = "category/"


@pytest.fixture
def test_client():
    return TestClient(router)


def test_get_categories_successful_returns_list(test_client):
    response = test_client.get(CATEGORY_ENDPOINT)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
