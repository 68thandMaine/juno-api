# Test for Error emitted

# Test for shape of data created
from unittest.mock import MagicMock

import pytest

from app.controllers.payment_controller import PaymentController
from app.lib.constants import PAYMENT_ERROR_BILL_ID_NOT_FOUND
from app.lib.exceptions import ControllerException
from app.models import Payment
from app.tests.fixtures.fake_data import payment_for_tests


@pytest.fixture
def payment_controller():
    return PaymentController()


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


@pytest.mark.runonly
async def test_make_payment_returns_payment_when_successful(
    payment_controller: PaymentController, mocker
):
    mocker.patch.object(payment_controller, "_verify_bill_exists", return_value=True)
    mocker.patch.object(
        payment_controller.payment_service,
        "create",
        return_value=Payment(**payment_for_tests),
    )

    result = await payment_controller.make_payment(data=Payment(**payment_for_tests))

    assert isinstance(result, Payment)
