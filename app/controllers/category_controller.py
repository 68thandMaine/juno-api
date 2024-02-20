from uuid import UUID

from app.lib.exceptions import ControllerException, ServiceException
from app.models import Category
from app.services.crud import CRUDService


class CategoryController:
    """Controller for handling behaviors needed for interacting with categories
    of financial information.
    """

    def __init__(self):
        self.category_service = CRUDService(Category)

    async def get_categories(self) -> list[Category]:
        """
        Returns a list of all categories a financial transaction could belong to
        """
        try:
            results = await self.category_service.get()
        except ServiceException as e:
            raise ControllerException(
                detail=f"There was an issue with the category service when getting categories:\n {e}"
            ) from e
        except Exception as e:
            raise ControllerException(detail=e) from e
        return results

    async def add_category(self, category: Category) -> Category:
        """
        Creates a new category in the database

        Args:
            category_name (str): The name of the new category
        """
        if not isinstance(category, Category):
            raise ValueError("Not of correct type")
        try:
            added_category = await self.category_service.create(category)
        except ValueError as e:
            raise ValueError(e) from e
        except ServiceException as e:
            raise ControllerException(detail=e) from e
        return added_category

    async def remove_category(self, category_id: UUID):
        if not isinstance(category_id, UUID):
            raise ValueError("Invalid Category Id")
        try:
            await self.category_service.delete(category_id)
        except ServiceException as e:
            raise ControllerException(
                detail=f"There was an issue with the category service when removing a category:\n {e}"
            ) from e
        except Exception as e:
            raise ControllerException(detail=e) from e

    async def update_category(self, category: Category) -> Category:
        """
        Updates a category

        Args:
            category (Category): _description_
        """

        try:
            category = await self.category_service.put(category.id, category)
        except ServiceException as e:
            message = e
            raise ControllerException(
                detail=f"There is an issue with the category service: {message}"
            ) from e
        except Exception as e:
            raise ControllerException(detail=e) from e

        return category
