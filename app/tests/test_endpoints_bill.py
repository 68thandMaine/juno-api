from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.lib.exceptions import ControllerException
from app.models import Bill
from app.tests.mocks.fake_data import bill_for_tests
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
    async def mock_get_bills():
        raise ControllerException(status_code=500, detail="Some error message")

    monkeypatch.setattr(
        "app.controllers.bill_controller.BillController.get_bills", mock_get_bills
    )

    result = await async_client.get(BILL_ENDPOINT)
    assert result.status_code == 500


@pytest.mark.asyncio
async def test_get_bills_returns_list_of_bills_when_successful(
    async_client: AsyncClient, setup_fake_bill: setup_fake_bill
):
    fake_bill = setup_fake_bill()
    fake_bill = fake_bill.model_dump()
    fake_bill["id"] = str(fake_bill["id"])
    fake_bill = {**bill_for_tests, **fake_bill}

    await async_client.post(BILL_ENDPOINT, json=fake_bill)

    result = await async_client.get(BILL_ENDPOINT)
    result = [Bill(**b) for b in result.json()]

    for bill in result:
        assert isinstance(bill, Bill)


@pytest.mark.asyncio
async def test_add_bill_returns_200_when_successful(
    async_client: AsyncClient, setup_fake_bill: setup_fake_bill
):
    fake_bill = setup_fake_bill()
    fake_bill = fake_bill.model_dump()
    fake_bill["id"] = str(fake_bill["id"])
    fake_bill = {**bill_for_tests, **fake_bill}

    result = await async_client.post(BILL_ENDPOINT, json=fake_bill)
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_add_bill_returns_500_when_unsuccessful(
    async_client: AsyncClient, setup_fake_bill: setup_fake_bill
):
    fake_bill = setup_fake_bill({"due_date": "12.22.23"})
    fake_bill = fake_bill.model_dump()
    fake_bill["id"] = str(fake_bill["id"])
    fake_bill = {**bill_for_tests, **fake_bill}

    with pytest.raises(ControllerException) as exc_info:
        result = await async_client.post(BILL_ENDPOINT, json=fake_bill)

    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_add_bill_returns_bill_when_successful(async_client: AsyncClient):
    fake_bill = {**bill_for_tests, "id": str(uuid4())}
    result = await async_client.post(BILL_ENDPOINT, json=fake_bill)
    assert Bill(**result.json())


@pytest.mark.asyncio
async def test_update_bill_returns_200_when_successful(
    async_client: AsyncClient, setup_fake_bill: setup_fake_bill
):
    fake_bill = {**bill_for_tests, "id": str(uuid4())}

    bill = await async_client.post(BILL_ENDPOINT, json=fake_bill)
    bill = bill.json()
    bill["name"] = "TEST_NAME"
    bill_id = bill["id"]
    endpoint = f"{BILL_ENDPOINT}update/{bill_id}"
    result = await async_client.put(endpoint, json=bill)

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
async def test_update_bill_returns_bill_when_successful(async_client: AsyncClient):
    bill = await async_client.post(BILL_ENDPOINT, json=bill_for_tests)
    new_bill = bill.json()
    UPDATE_WORD = "UPDATE"
    new_bill["name"] = UPDATE_WORD
    bill_id = new_bill["id"]
    endpoint = f"{BILL_ENDPOINT}update/{bill_id}"
    result = await async_client.put(endpoint, json=new_bill)
    assert Bill(**result.json())
