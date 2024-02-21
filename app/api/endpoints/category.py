from fastapi import APIRouter, Depends, HTTPException

from app.controllers.category_controller import CategoryController
from app.models import Category, CategoryInput

router = APIRouter(prefix="/category")


async def handle_router_exception(e: Exception):
    raise HTTPException(
        status_code=500, detail=f"Exception caught in router: {str(e)}"
    ) from e


@router.get("/", operation_id="get_categories", response_model=list[Category])
async def get_categories(controller=Depends(CategoryController)) -> list[Category]:
    """
    Gets a list of all possible categories a bill could
    belong to.
    """
    try:
        return await controller.get()
    except Exception as e:
        handle_router_exception(e)


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
        handle_router_exception(e)


@router.put("/{category_id}", operation_id="update_category", response_model=Category)
async def update_category(
    category: CategoryInput, controller=Depends(CategoryController)
) -> Category:
    """
    Updates a category. Mostly for changing the name.
    """

    try:
        return await controller.update_category(category)
    except Exception as e:
        handle_router_exception(e)
