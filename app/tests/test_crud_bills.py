import copy
import uuid
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from app.tests.fixtures.fake_data import bill_for_tests


# ! Turn this into a utility function because it's used in test_crud_payment as well
@pytest.fixture
def setup_fake_bill():
    def _setup_fake_bill(overrides=None):
        fake_bill = copy.copy(bill_for_tests)
        if overrides:
            fake_bill.update(overrides)
        return fake_bill

    return _setup_fake_bill


@pytest.mark.asyncio
async def test_add_bill_returns_200_upon_successful_completion(
    async_client: AsyncClient,
    setup_fake_bill,
):
    result = await async_client.post("bills/", json=setup_fake_bill())
    assert result.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "overrides, expected_exception",
    [({"due_date": "DATE"}, ("AttributeError", "Invalid isoformat string: 'DATE'"))],
)
async def test_add_bill_throws_error_if_date_is_incorrect(
    async_client: AsyncClient, expected_exception, setup_fake_bill, overrides
):
    fake_bill = setup_fake_bill(overrides)
    with pytest.raises(Exception) as excinfo:
        await async_client.post("bills/", json=fake_bill)
    result = str(excinfo)

    error_type, error_msg = expected_exception
    assert error_type in result and error_msg in result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "overrides, expected_exception",
    [({"category": str(uuid.uuid4())}, ("AttributeError", "not present in table"))],
)
async def test_add_bill_throws_error_if_category_uuid_is_incorrect(
    async_client: AsyncClient, expected_exception, setup_fake_bill, overrides
):
    fake_bill = setup_fake_bill(overrides)
    with pytest.raises(Exception) as excinfo:
        await async_client.post("bills/", json=fake_bill)
    result = str(excinfo)
    error_type, error_msg = expected_exception
    assert error_type in result and error_msg in result


@pytest.mark.asyncio
async def test_get_bills_returns_empty_list_if_no_data_exists(
    async_client: AsyncClient, mocker
):
    mock = mocker.patch.object(async_client, "get", return_value=MagicMock())
    mock.return_value.json.return_value = []
    result = await async_client.get("bills/")
    assert result.json() == []


@pytest.mark.asyncio
async def test_get_bills_returns_a_200_when_successful(async_client: AsyncClient):
    result = await async_client.get("bills/")
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_update_bill_returns_bill_with_updated_data(
    async_client: AsyncClient, setup_fake_bill
):
    created_bill = await async_client.post("bills/", json=setup_fake_bill())
    new_name = "Verizon"
    bill = created_bill.json()
    bill["name"] = new_name
    bill_id = bill["id"]
    result = await async_client.put(f"bills/update/{bill_id}", json=bill)
    assert result.status_code == 200
    assert result.json()["name"] == new_name
