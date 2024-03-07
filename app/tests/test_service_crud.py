import pytest

from app.models import Bill, Category, Payment
from app.services.crud import CRUDService


async def test_service_inits_with_correct_model():
    crud_service = CRUDService(model=Bill)
    assert crud_service.model == Bill
    assert isinstance(crud_service.model(), Bill)


@pytest.mark.asyncio
@pytest.mark.parametrize("models", [Bill, Payment, Category])
async def test_service_gets_table_data_for_model(models):
    crud_service = CRUDService(model=models)

    result = await crud_service.get()
    assert isinstance(result, list)
    for r in result:
        assert isinstance(r, models)


@pytest.mark.asyncio
async def test_service_deletes_data_by_model_id():
    crud_service = CRUDService(model=Category)
    category = Category(name="TEST_CATEGORY")
    await crud_service.create(category)

    found_category = await crud_service.get_one(category.id)
    deleted = await crud_service.delete(found_category.id)
    assert deleted is (True)
