from unittest.mock import AsyncMock

import pytest

from app.controllers.payment_controller import PaymentController
from app.core.lib.constants import PAYMENT_ERROR_BILL_ID_NOT_FOUND
from app.core.lib.exceptions import ControllerException, ServiceException
from app.models import Payment
from app.tests.fixtures.app_fixtures import payment_controller
from app.tests.mocks.fake_data import payment_for_tests


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payment, expected",
    [
        (Payment(**payment_for_tests), PAYMENT_ERROR_BILL_ID_NOT_FOUND),
    ],
)
async def test_make_payment_raises_not_found_if_bill_does_not_exist(
    payment, expected, payment_controller: PaymentController
):
    with pytest.raises(ControllerException) as exception:
        await payment_controller.make_payment(payment)
    assert expected in str(exception.value)


@pytest.mark.asyncio
async def test_make_payment_returns_payment_when_successful(
    payment_controller: PaymentController, mocker
):
    mock_data = Payment(**payment_for_tests)
    mocker.patch.object(payment_controller, "_verify_bill_exists", return_value=True)
    mocker.patch.object(
        payment_controller.payment_service,
        "create",
        return_value=mock_data,
    )

    result = await payment_controller.make_payment(data=mock_data)

    assert isinstance(result, Payment)


@pytest.mark.asyncio
async def test_get_payments_raises_controller_issue_for_service_exceptions(
    payment_controller: PaymentController,
):
    payment_controller.payment_service.get = AsyncMock(
        side_effect=ServiceException("Service error")
    )

    with pytest.raises(ControllerException) as exc_info:
        await payment_controller.get_payments()
    assert (
        "There was an issue with the payment service when getting a payment: Service error"
        in str(exc_info.value)
    )
