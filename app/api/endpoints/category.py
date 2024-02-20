from fastapi import APIRouter, Depends, HTTPException

from app.controllers.category_controller import CategoryController
from app.models import Category, CategoryInput

router = APIRouter(prefix="/category")


@router.get("/", operation_id="get_categories", response_model=list[Category])
async def get_categories(controller=Depends(CategoryController)) -> list[Category]:
    """
    Gets a list of all possible categories a bill could
    belong to.
    """
    try:
        categories = await controller.get()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get categories: {str(e)}"
        ) from e
    return categories


@router.post("/", operation_id="new_category", response_model=Category)
async def new_category(
    category: Category, controller=Depends(CategoryController)
) -> Category:
    """
    Creates a new category
    """
    try:
        return await controller.add_category(category)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create new category: {str(e)}"
        ) from e


@router.put("/{category_id}", operation_id="update_category", response_model=Category)
async def update_category(
    category: CategoryInput, controller=Depends(CategoryController)
) -> Category:
    """
    Updates a category. Mostly for changing the name.
    """

    try:
        updated_category = await controller.update_category(category)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update category: {str(e)}"
        ) from e
    return updated_category
