import uuid

import pytest

from app.controllers.bill_controller import BillController
from app.core.lib.constants import INCORRECT_DATE
from app.core.lib.exceptions import ControllerException
from app.models.bill import Bill, BillUpdate
from app.tests.fixtures.setup_fake_bill import setup_fake_bill
from app.tests.mocks.fake_data import bill_for_tests


@pytest.fixture
def bill_controller():
    return BillController()


@pytest.mark.runonly
@pytest.mark.asyncio
async def test_add_bill_returns_bill_instance(
    bill_controller: BillController, setup_fake_bill
):
    bill = setup_fake_bill()
    result = await bill_controller.add_bill(new_bill=bill)
    assert isinstance(result, Bill)


@pytest.mark.parametrize(
    "overrides, expected_exception",
    [
        (
            {"due_date": "DATE"},
            " There is an issue with a value: Incorrect date string",
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_bill_raises_value_error_if_bill_properties_are_incorrect(
    overrides, expected_exception, bill_controller: BillController, setup_fake_bill
):
    bill = setup_fake_bill(overrides)
    with pytest.raises(ValueError, match=expected_exception):
        await bill_controller.add_bill(bill)


@pytest.mark.asyncio
async def test_get_bills_returns_a_list_of_bills(
    bill_controller: BillController, setup_fake_bill
):
    bill = setup_fake_bill()
    await bill_controller.add_bill(new_bill=bill)
    result = await bill_controller.get_bills()
    assert isinstance(result, list)
    assert isinstance(result[0], Bill)


@pytest.mark.asyncio()
async def test_get_one_bill_returns_a_bill_instance(
    bill_controller: BillController, setup_fake_bill
):
    bill = await bill_controller.add_bill(new_bill=setup_fake_bill())
    if bill.id:
        result = await bill_controller.get_one_bill(bill.id)

        assert isinstance(result, Bill)
        assert result == bill


@pytest.mark.asyncio
async def test_get_one_bill_returns_none_for_nonexistent_uuid(
    bill_controller: BillController,
):
    fake_uuid = uuid.uuid4()
    result = await bill_controller.get_one_bill(fake_uuid)
    assert result is None


@pytest.mark.asyncio
async def test_update_bill_raises_value_error_if_id_is_not_valid(
    bill_controller: BillController, setup_fake_bill
):
    fake_bill = setup_fake_bill()
    fake_bill["id"] = str(fake_bill["id"])
    fake_bill = {**bill_for_tests, **fake_bill}
    fake_bill = BillUpdate(**fake_bill)

    with pytest.raises(ValueError) as excinfo:
        await bill_controller.update_bill(bill=fake_bill)
    exception_message = str(excinfo.value)

    assert f"No bill with id {fake_bill.id} was found" in exception_message


@pytest.mark.asyncio
async def test_update_bill_returns_updated_bill_if_successful(
    bill_controller: BillController, setup_fake_bill
):
    updated_name = "TEST_UPDATE_NAME"
    existing_bill = await bill_controller.add_bill(new_bill=setup_fake_bill())

    existing_bill.name = updated_name
    result = await bill_controller.update_bill(existing_bill)

    assert isinstance(result, Bill)
    for k, v in result.model_dump().items():
        assert v == getattr(existing_bill, k)
