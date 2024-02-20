import copy

import pytest
from httpx import AsyncClient

from app.lib.constants import PAYMENT_ERROR_BILL_ID_NOT_FOUND
from app.models.all import Payment
from app.tests.fixtures.fake_data import bill_for_tests, payment_for_tests


# ! Turn this into a utility function because it's used in test_crud_bills as well
@pytest.fixture
def setup_fake_payment():
    def _setup_fake_payment(overrides=None):
        fake_payment = copy.copy(payment_for_tests)
        if overrides:
            fake_payment.update(overrides)
        return fake_payment

    return _setup_fake_payment


@pytest.mark.asyncio
async def test_get_payments_returns_200_if_successful(async_client: AsyncClient):
    result = await async_client.get("payment/")
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_get_payments_returns_list_of_payments_if_successful(
    async_client: AsyncClient,
):
    result = await async_client.get("payment/")
    assert isinstance(result.json(), list)


@pytest.mark.asyncio
async def test_new_payment_return_412_when_bill_id_is_invalid(
    async_client: AsyncClient, setup_fake_payment
):
    result = await async_client.post("payment/", json=setup_fake_payment())
    assert result.status_code == 412


@pytest.mark.asyncio
async def test_new_payment_return_message_when_bill_id_is_invalid(
    async_client: AsyncClient, setup_fake_payment
):
    result = await async_client.post("payment/", json=setup_fake_payment())

    assert PAYMENT_ERROR_BILL_ID_NOT_FOUND in result.json()["detail"]


@pytest.mark.asyncio
async def test_new_payment_returns_200_when_payment_created(
    async_client: AsyncClient, setup_fake_payment
):
    bill = await async_client.post("bills/", json=bill_for_tests)

    bill_id = bill.json()["id"]
    payment = payment_for_tests
    payment["bill_id"] = bill_id

    result = await async_client.post("payment/", json=payment)
    assert result.status_code == 200
