import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.all import Category, Payment
from app.models.bill import Bill
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
