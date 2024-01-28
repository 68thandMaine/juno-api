from typing import List

from fastapi import APIRouter, Depends

from app.controllers.category_controller import CategoryController
from app.models import Category, CategoryInput

router = APIRouter(prefix="/category")


@router.get("/", operation_id="get_categories")
async def get_categories(controller=Depends(CategoryController)) -> List[Category]:
    """
    Gets a list of all possible categories a bill could
    belong to.
    """
    categories = await controller.get()
    return categories


@router.post("/", operation_id="new_category", response_model=Category)
async def new_category(
    category: Category, controller=Depends(CategoryController)
) -> Category:
    """
    Creates a new category
    """
    try:
        cs = await controller.add_category(category)
        return cs
    except Exception as e:
        raise Exception(e) from e


@router.put("/{category_id}", operation_id="update_category")
async def update_category(
    category_id, category: CategoryInput, controller=Depends(CategoryController)
) -> None:
    """
    Updates a category. Mostly for changing the name.
    """

    try:
        category = await controller.update_category(category)
    except Exception as e:
        raise Exception(e) from e
    return category
