from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.controllers.bill_controller import BillController
from app.lib.exceptions import ControllerException
from app.models import Bill
from app.tests.fixtures.setup_fake_bill import setup_fake_bill

BILL_ENDPOINT = "bills/"


@pytest.mark.asyncio
async def test_get_bills_returns_200_when_successful(async_client: AsyncClient):
    result = await async_client.get(BILL_ENDPOINT)
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_get_bills_returns_500_when_unsuccessful(
    async_client: AsyncClient, monkeypatch
):
    # Arrange
    async def mock_get_bills():
        raise ControllerException(status_code=500, detail="Some error message")

    mock_controller = AsyncMock(BillController)
    mock_controller.get_bills = mock_get_bills

    monkeypatch.setattr(
        "app.controllers.bill_controller.BillController", mock_controller
    )

    result = await async_client.get(BILL_ENDPOINT)

    assert result.status_code == 500


@pytest.mark.asyncio
async def test_get_bills_returns_list_of_bills_when_successful(
    async_client: AsyncClient, fake_bill: setup_fake_bill
):
    await async_client.post(BILL_ENDPOINT, json=fake_bill())
    result = await async_client.get(BILL_ENDPOINT)
    assert isinstance(result, list[Bill])


@pytest.mark.asyncio
async def test_add_bill_returns_200_when_successful(
    async_client: AsyncClient, fake_bill: setup_fake_bill
):
    result = await async_client.post(BILL_ENDPOINT, fake_bill())
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_add_bill_returns_500_when_unsuccessful(
    async_client: AsyncClient, fake_bill: setup_fake_bill
):
    result = await async_client.post(
        BILL_ENDPOINT, json=fake_bill({"due_date": "12.22.23"})
    )
    assert result.status_code == 500


@pytest.mark.asyncio
async def test_add_bill_returns_bill_when_successful(
    async_client: AsyncClient, fake_bill: setup_fake_bill
):
    result = await async_client.post(BILL_ENDPOINT, json=fake_bill())
    assert isinstance(result, Bill)


@pytest.mark.asyncio
async def test_update_bill_returns_200_when_successful(
    async_client: AsyncClient, fake_bill: setup_fake_bill
):
    bill = await async_client.post(BILL_ENDPOINT, json=fake_bill())
    bill["name"] = "TEST_NAME"
    result = await async_client.put(BILL_ENDPOINT, json=bill)
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_update_bill_returns_500_when_unsuccessful(
    async_client: AsyncClient, fake_bill: setup_fake_bill
):
    FAKE_BILL_ID = uuid4
    result = await async_client.put(
        f"{BILL_ENDPOINT}/f{FAKE_BILL_ID}", json=fake_bill()
    )

    assert result.status_code == 500


@pytest.mark.asyncio
async def test_update_bill_returns_bill_when_successful(
    async_client: AsyncClient, fake_bill: setup_fake_bill
):
    # Create a bill in the database
    new_bill = await async_client.post(BILL_ENDPOINT, json=fake_bill())
    # update the bill
    UPDATE_WORD = "UPDATE"
    new_bill["name"] = UPDATE_WORD
    result = await async_client.put(BILL_ENDPOINT, params=new_bill["id"], json=new_bill)
    assert isinstance(result, Bill)
