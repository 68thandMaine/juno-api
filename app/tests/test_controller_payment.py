import pytest

from app.controllers.payment_controller import PaymentController
from app.models import Payment
from app.tests.mocks.fake_data import payment_for_tests


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
