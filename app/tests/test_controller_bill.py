import uuid

import pytest

from app.controllers.bill_controller import BillController
from app.models.bill import Bill
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
        ({"due_date": "DATE"}, ("Invalid isoformat string: 'DATE'")),
        ({"category": "UUID"}, ("Input should be a valid UUID")),
    ],
)
@pytest.mark.asyncio
async def test_add_bill_raises_runtime_error_if_bill_properties_are_incorrect(
    setup_fake_bill, overrides, expected_exception, bill_controller: BillController
):
    bill = setup_fake_bill(overrides)
    with pytest.raises(RuntimeError) as excinfo:
        await bill_controller.add_bill(bill)

    exception_msg = str(excinfo.value)
    error_msg = expected_exception
    assert error_msg in exception_msg


@pytest.mark.asyncio
async def test_get_bills_returns_a_list_of_bills(
    setup_fake_bill, bill_controller: BillController
):
    bill = setup_fake_bill()
    await bill_controller.add_bill(new_bill=bill)

    result = await bill_controller.get_bills()
    assert isinstance(result, list)
    assert isinstance(result[0], Bill)


@pytest.mark.asyncio
async def test_get_one_bill_returns_a_bill_instance(
    setup_fake_bill, bill_controller: BillController
):
    bill = await bill_controller.add_bill(new_bill=setup_fake_bill())
    target_bill = bill.model_dump()
    result = await bill_controller.get_one_bill(target_bill["id"])
    returned_bill = result.model_dump()
    assert isinstance(result, Bill)

    for k, v in returned_bill.items():
        assert target_bill[k] == v


@pytest.mark.asyncio
async def test_get_one_bill_returns_none_for_nonexistent_uuid(
    bill_controller: BillController,
):
    fake_uuid = uuid.uuid4()
    result = await bill_controller.get_one_bill(fake_uuid)
    assert result is None


@pytest.mark.asyncio
async def test_update_bill_raises_value_error_if_id_is_not_valid(
    setup_fake_bill, bill_controller: BillController
):
    bill = Bill(**setup_fake_bill())
    with pytest.raises(ValueError) as excinfo:
        await bill_controller.update_bill(bill=bill)
    exception_message = str(excinfo)
    assert f"No bill with id {bill.id} was found" in exception_message


@pytest.mark.asyncio
async def test_update_bill_returns_updated_bill_if_successful(
    setup_fake_bill, bill_controller: BillController
):
    updated_name = "TEST_UPDATE_NAME"
    existing_bill = await bill_controller.add_bill(new_bill=setup_fake_bill())
    existing_bill.name = updated_name
    result = await bill_controller.update_bill(existing_bill)

    assert isinstance(result, Bill)
    for k, v in result.model_dump().items():
        assert v == getattr(existing_bill, k)
