from uuid import uuid4

import pytest

from app.controllers.category_controller import CategoryController
from app.core.lib.constants import CANNOT_UPDATE
from app.core.lib.exceptions import ControllerException, ServiceException
from app.models import Category
from app.services.crud import CRUDService

INVALID_INPUT = "invalid input for query argument"


@pytest.fixture
def category_controller():
    return CategoryController()


@pytest.mark.asyncio
async def test_get_categories_returns_list_of_category_objects(
    mocker, category_controller: CategoryController
):
    mocker.patch.object(
        CRUDService,
        "get",
        return_value=[
            Category(id=1, name="Category1"),
            Category(id=2, name="Category2"),
        ],
    )

    result = await category_controller.get_categories()

    assert isinstance(result, list)
    assert len(result) is 2
    assert all(isinstance(category, Category) for category in result)


@pytest.mark.asyncio
async def test_get_categories_returns_list_if_no_categories_exist(
    mocker, category_controller: CategoryController
):
    mocker.patch.object(
        CRUDService,
        "get",
        return_value=[],
    )

    result = await category_controller.get_categories()

    assert len(result) is 0


@pytest.mark.asyncio
async def test_add_category_raises_value_error_for_wrong_input(
    mocker, category_controller: CategoryController
):
    mocker.patch.object(CRUDService, "get", side_effect=ServiceException())

    with pytest.raises(ControllerException) as exc_info:
        await category_controller.add_category("string")
    assert isinstance(exc_info.value, ControllerException)


@pytest.mark.asyncio
async def test_add_category_creates_new_category(
    mocker, category_controller: CategoryController
):
    # Arrange
    mock_category_service = mocker.patch.object(
        CRUDService, "create", return_value=Category(id=1, name="NewCategory")
    )

    # Act
    new_category_data = Category(**{"name": "NewCategory"})
    new_category = await category_controller.add_category(new_category_data)

    # Assert
    assert isinstance(new_category, Category)
    assert new_category.id == 1
    assert new_category.name == "NewCategory"

    mock_category_service.assert_called_once_with(new_category_data)


@pytest.mark.asyncio
async def test_remove_category_removes_category(
    mocker, category_controller: CategoryController
):
    mock_category_service = mocker.patch.object(CRUDService, "delete")

    category_id_to_remove = uuid4()
    await category_controller.remove_category(category_id_to_remove)

    mock_category_service.assert_called_once_with(category_id_to_remove)


@pytest.mark.asyncio
async def test_remove_category_raises_value_error_if_category_id_is_invalid(
    category_controller: CategoryController,
):
    with pytest.raises(ControllerException) as exc_info:
        uuid = uuid4()
        await category_controller.remove_category(uuid)
    assert "Invalid Category Id" in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_category_updates_category(
    mocker, category_controller: CategoryController
):
    mock_category_service = mocker.patch.object(
        CRUDService, "put", return_value=Category(id=1, name="UpdatedCategory")
    )

    updated_category_data = Category(id=1, name="UpdatedCategory")
    updated_category = await category_controller.update_category(updated_category_data)

    assert isinstance(updated_category, Category)
    assert updated_category.id == 1
    assert updated_category.name == "UpdatedCategory"

    mock_category_service.assert_called_once_with(
        updated_category_data.id, updated_category_data
    )
