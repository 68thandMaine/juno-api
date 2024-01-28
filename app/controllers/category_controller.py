from uuid import UUID

from app.lib.exceptions import ServiceException
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
        except Exception as e:
            raise ServiceException(e) from e
        return results

    async def add_category(self, category):
        """
        Creates a new category in the database

        Args:
            category_name (str): The name of the new category
        """

        try:
            category = await self.category_service.create(category)
        except ValueError as e:
            raise ServiceException() from e
        except Exception as e:
            raise Exception(e) from e
        return category

    async def remove_category(self, category_id: UUID):
        try:
            await self.category_service.delete(category_id)
        except Exception as e:
            raise Exception(e) from e

    async def update_category(self, category: Category):
        """
        Updates a category

        Args:
            category (Category): _description_
        """
        try:
            category = await self.category_service.put(category.id, category)
        except Exception as e:
            raise Exception(e) from e

        return category
