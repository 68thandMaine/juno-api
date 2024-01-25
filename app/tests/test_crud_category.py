from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from app.models.all import Category


@pytest.mark.asyncio
async def test_get_cateogories_returns_empty_list(async_client: AsyncClient, mocker):
    mock = mocker.patch.object(async_client, "get", return_value=MagicMock())
    mock.return_value = []
    result = await async_client.get("category/")
    assert result == []


@pytest.mark.asyncio
async def test_post_category_returns_the_newly_created_category(
    async_client: AsyncClient,
):
    new_category = {"name": "TEST_CATEGORY"}
    result = await async_client.post("category/", json=new_category)
    result_json = result.json()
    assert result_json["name"] == "TEST_CATEGORY"


@pytest.mark.asyncio
async def test_post_category_returns_200_upon_successful_category_creation(
    async_client: AsyncClient,
):
    new_category = {"name": "TEST_CATEGORY"}
    result = await async_client.post("category/", json=new_category)

    assert result.status_code == 200


@pytest.mark.asyncio
async def test_post_category_returns_a_category_object_upon_successful_creation(
    async_client: AsyncClient,
):
    """
    Test the status code is correct when a successful category is created
    """
    new_category = {"name": "TEST_CATEGORY"}
    result = await async_client.post("category/", json=new_category)
    for key in result.json().keys():
        assert hasattr(Category, key)


@pytest.mark.asyncio
async def test_update_category_updates_the_category(async_client: AsyncClient):
    """
    Test that the update route returns the updated category
    """
    UPDATED_NAME = "UPDATE"
    BASE_NAME = "TEST_CATEGORY"
    # Create an entry in the db
    base_category = {"name": BASE_NAME}
    post_response = await async_client.post("category/", json=base_category)

    # Update the created category
    db_category = post_response.json()
    db_category_id = db_category["id"]
    db_category["name"] = UPDATED_NAME

    update_response = await async_client.put(
        f"category/{db_category_id}", json=db_category
    )
    updated_category = update_response.json()
    assert updated_category["name"] == UPDATED_NAME
