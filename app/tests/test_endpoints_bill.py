from datetime import datetime
from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.core.lib.exceptions import ControllerException
from app.models import Bill
from app.tests.fixtures.setup_fake_bill import setup_fake_bill
from app.tests.mocks.fake_data import bill_for_tests

BILL_ENDPOINT = "bills/"


@pytest.mark.asyncio
async def test_get_bills_returns_200_when_successful(async_client: AsyncClient):
    result = await async_client.get(BILL_ENDPOINT)
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_get_bills_returns_500_when_unsuccessful(
    async_client: AsyncClient, monkeypatch
):
    async def mock_get_bills(_):
        raise ControllerException(status_code=500, detail="Some error message")

    monkeypatch.setattr(
        "app.controllers.bill_controller.BillController.get_bills", mock_get_bills
    )

    result = await async_client.get(BILL_ENDPOINT)
    assert result.status_code == 500


@pytest.mark.asyncio
async def test_get_bills_returns_list_of_bills_when_successful(
    async_client: AsyncClient, setup_fake_bill
):
    await async_client.post(BILL_ENDPOINT, json=setup_fake_bill())
    response = await async_client.get(BILL_ENDPOINT)
    result = [Bill(**b) for b in response.json()]
    for bill in result:
        assert isinstance(bill, Bill)


@pytest.mark.asyncio
async def test_add_bill_returns_200_when_successful(
    async_client: AsyncClient, setup_fake_bill
):
    result = await async_client.post(BILL_ENDPOINT, json=setup_fake_bill())
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_add_bill_returns_bill_when_successful(async_client: AsyncClient):
    fake_bill = {**bill_for_tests, "id": str(uuid4())}
    result = await async_client.post(BILL_ENDPOINT, json=fake_bill)
    assert Bill(**result.json())


@pytest.mark.asyncio
async def test_update_bill_returns_200_when_successful(
    setup_fake_bill, async_client: AsyncClient
):
    response = await async_client.post(BILL_ENDPOINT, json=setup_fake_bill())
    bill = Bill(**response.json())
    bill.name = "TEST_NAME"
    if isinstance(bill.due_date, str):
        bill.due_date = datetime.strptime(bill.due_date, "%Y-%m-%dT%H:%M:%S").strftime(
            "%m/%d/%Y"
        )
    endpoint = f"{BILL_ENDPOINT}update/{bill.id}"

    result = await async_client.put(endpoint, json=bill.model_dump())

    assert result.status_code == 200


@pytest.mark.asyncio
async def test_update_bill_returns_500_when_unsuccessful(
    async_client: AsyncClient,
):
    fake_bill = {**bill_for_tests, "id": str(uuid4())}
    FAKE_BILL_ID = fake_bill["id"]
    result = await async_client.put(
        f"{BILL_ENDPOINT}update/f{FAKE_BILL_ID}", json=fake_bill
    )
    assert result.status_code == 500


@pytest.mark.asyncio
async def test_update_bill_returns_bill_when_successful(
    setup_fake_bill, async_client: AsyncClient
):
    bill = await async_client.post(BILL_ENDPOINT, json=setup_fake_bill())
    new_bill = bill.json()
    UPDATE_WORD = "UPDATE"
    new_bill["name"] = UPDATE_WORD
    new_bill["due_date"] = datetime.strptime(
        new_bill["due_date"], "%Y-%m-%dT%H:%M:%S"
    ).strftime("%m/%d/%Y")
    bill_id = new_bill["id"]

    endpoint = f"{BILL_ENDPOINT}update/{bill_id}"
    result = await async_client.put(endpoint, json=new_bill)
    assert Bill(**result.json())
