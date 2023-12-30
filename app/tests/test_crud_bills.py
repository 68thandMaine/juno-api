import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.all import Bill
from app.core.config import settings


@pytest.mark.asyncio 
async def test_create_bill(
  async_client: AsyncClient,
  async_session: AsyncSession,
  
):
  payload = {'hi': 'bye'}
  response = await async_client.post("/bills", json=payload)
  breakpoint()
  assert response.status_code == 201