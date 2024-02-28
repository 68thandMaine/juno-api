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
        """Get a list of all categories in the database.

        Returns:
            list[Category]: List of Category objects.
        """
        try:
            return await self.category_service.get()

        except ServiceException as e:
            raise ControllerException(detail=f"Service error: {str(e)}") from e
        except Exception as e:
            raise ControllerException(detail=f"Unexpected error: {str(e)}") from e

    async def add_category(self, category: Category) -> Category:
        """Creates a new category in the database.

        Args:
            category (Category): The Category object to be added.

        Returns:
            Category: The added Category object.
        """
        if not isinstance(category, Category):
            raise ControllerException(detail="Invalid Category Object")
        try:
            return await self.category_service.create(category)
        except ServiceException as e:
            raise ControllerException(detail=f"Service error: {str(e)}") from e
        except Exception as e:
            raise ControllerException(detail=f"Unexpected error: {str(e)}") from e

    async def remove_category(self, category_id: UUID):
        """Removes a category from the database.

        Args:
            category_id (UUID): The UUID of the category to be removed.
        """
        if not isinstance(category_id, UUID):
            raise ControllerException(detail="Invalid Category Id")
        try:
            await self.category_service.delete(category_id)
        except ServiceException as e:
            raise ControllerException(detail=f"Service error: {str(e)}") from e
        except Exception as e:
            raise ControllerException(detail=f"Unexpected error: {str(e)}") from e

    async def update_category(self, category: Category) -> Category:
        """Updates a category in the database.

        Args:
            category (Category): The updated Category object.

        Returns:
            Category: The updated Category object.
        """
        try:
            return await self.category_service.put(category.id, category)
        except ServiceException as e:
            raise ControllerException(detail=f"Service error: {str(e)}") from e
        except Exception as e:
            raise ControllerException(detail=f"Unexpected error: {str(e)}") from e
