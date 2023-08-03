from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest
from app.main import app

client = TestClient(app)


# Mock the get_session function for testing
@patch("app.main.get_session")
async def test_get_bills(mock_get_session):
    # Mock the return value of the session object
    mock_session = mock_get_session.return_value
    mock_result = mock_session.exec.return_value
    mock_result.scalars.return_value.all.return_value = ["Bill 1", "Bill 2"]

    # Send a test request to the endpoint
    response = client.get("/bills/")

    assert response.status_code == 200
    assert response.json() == ["Bill 1", "Bill 2"]

    # Ensure that the function was called with the correct arguments
    mock_get_session.assert_called_once()


# Similar tests can be written for the other endpoints (get_bill and add_bill)
