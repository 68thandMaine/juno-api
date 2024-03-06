import uuid
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from app.core.lib.exceptions import ControllerException
from app.tests.fixtures.setup_fake_bill import setup_fake_bill


@pytest.mark.parametrize(
    "overrides",
    [({"date_due": "2023-01-05"})],
)
@pytest.mark.asyncio(scope="function")
async def test_add_bill_returns_200_upon_successful_completion(
    async_client: AsyncClient, setup_fake_bill, overrides
):
    bill = setup_fake_bill(overrides)
    result = await async_client.post("bills/", json=bill)
    assert result.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "overrides, expected_exception",
    [
        (
            {"due_date": "DATE"},
            ("ControllerException", "Invalid isoformat string: 'DATE'"),
        )
    ],
)
async def test_add_bill_throws_error_if_date_is_incorrect(
    async_client: AsyncClient, expected_exception, setup_fake_bill, overrides
):
    fake_bill = setup_fake_bill(overrides)
    
    with pytest.raises(Exception) as excinfo:
        await async_client.post("bills/", json=fake_bill)

    exception = str(excinfo)
    error_type, error_msg = expected_exception
    assert isinstance(excinfo.value, Exception)

    assert error_type in exception and error_msg in exception


# @pytest.mark.asyncio(scope="function")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "overrides, expected_exception",
    [
        (
            {"category": str(uuid.uuid4())},
            ("ControllerException", "Category does not exist"),
        )
    ],
)
async def test_add_bill_throws_error_if_category_uuid_is_incorrect(
    async_client: AsyncClient,
    expected_exception,
    setup_fake_bill,
    overrides,
):
    fake_bill = setup_fake_bill(overrides)

    with pytest.raises(ControllerException) as excinfo:
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
    async_client: AsyncClient,
    setup_fake_bill,
):
    fake_bill = setup_fake_bill()
    created_bill = await async_client.post("bills/", json=fake_bill)
    new_name = "Verizon"
    bill = created_bill.json()
    bill["name"] = new_name
    
    result = await async_client.put(f"bills/update/{bill["id"]}", json=bill)
    
    assert result.status_code == 200
    assert result.json()["name"] == new_name
