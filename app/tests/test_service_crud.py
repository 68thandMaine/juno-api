import pytest
from app.services.crud import CRUDService
from app.models.bill import Bill
from app.models.all import Payment, Category
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_service_inits_with_correct_model(
    async_session: AsyncSession,
):
    CRUD_service = CRUDService(session=async_session, model=Bill)

    assert CRUD_service.model == Bill
    assert isinstance(CRUD_service.model(), Bill)


@pytest.mark.asyncio
@pytest.mark.parametrize("models", [Bill, Payment, Category])
async def test_service_gets_table_data_for_model(async_session: AsyncSession, models):
    CRUD_service = CRUDService(session=async_session, model=models)

    result = await CRUD_service.get()
    assert isinstance(result, list)
    for r in result:
        assert isinstance(r, models)
