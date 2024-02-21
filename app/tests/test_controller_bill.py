import uuid

import pytest

from app.controllers.bill_controller import BillController
from app.lib.exceptions import ControllerException
from app.models.bill import Bill, BillUpdate
from app.tests.fixtures.fake_data import bill_for_tests
from app.tests.fixtures.setup_fake_bill import setup_fake_bill


@pytest.fixture
def bill_controller():
    return BillController()


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
        ({"due_date": "DATE"}, "Invalid isoformat string: 'DATE'"),
        ({"category": "UUID"}, "invalid UUID"),
    ],
)
@pytest.mark.asyncio
async def test_add_bill_raises_value_error_if_bill_properties_are_incorrect(
    overrides, expected_exception, bill_controller: BillController, setup_fake_bill
):
    bill = setup_fake_bill(overrides)
    with pytest.raises(ControllerException, match=expected_exception):
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


@pytest.mark.asyncio
async def test_get_one_bill_returns_a_bill_instance(
    bill_controller: BillController, setup_fake_bill
):
    bill = await bill_controller.add_bill(new_bill=setup_fake_bill())
    target_bill = bill.model_dump()
    result = await bill_controller.get_one_bill(target_bill["id"])
    returned_bill = result.model_dump()
    assert isinstance(result, Bill)

    assert returned_bill == target_bill


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
    fake_bill = fake_bill.model_dump()
    fake_bill["id"] = str(fake_bill["id"])
    fake_bill = {**bill_for_tests, **fake_bill}
    fake_bill = BillUpdate(**fake_bill)

    with pytest.raises(ValueError) as excinfo:
        await bill_controller.update_bill(bill=fake_bill)
    exception_message = str(excinfo)
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
