import pytest
from httpx import AsyncClient

CATEGORY_ENDPOINT = "category/"


@pytest.mark.asyncio
async def test_get_categories_successful_returns_list(async_client: AsyncClient):
    response = await async_client.get(CATEGORY_ENDPOINT)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
