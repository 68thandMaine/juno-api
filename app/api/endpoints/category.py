from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.juno_db import get_session
from app.models.all import Category

router = APIRouter(prefix="/category")


@router.get("/", operation_id="get_categories")
async def get_categories(
    session: AsyncSession = Depends(get_session),
) -> List[Category]:
    """
    Gets a list of all possible categories a bill could
    belong to.
    """
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    return [Category(*c) for c in categories]


@router.post("/", operation_id="new_category", response_model=Category)
async def new_category(
    category: Category, session: AsyncSession = Depends(get_session)
) -> Category:
    """
    Creates a new category
    """
    try:
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category
    except Exception as e:
        raise Exception(e)


@router.put("/{id}", operation_id="update_category")
async def update_category(
    category: Category, session: AsyncSession = Depends(get_session)
) -> None:
    """
    Updates a category. Mostly for changing the name.
    """

    db_result = await session.execute(
        select(Category).where(Category.id == category.id)
    )
    db_category = db_result.scalar_one()

    # compare changes and create object for update
    for k, v in category.model_dump().items():
        if v != str(getattr(db_category, k)):
            setattr(db_category, k, v)

    # update the category in the database
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)

    # return the category
    return db_category
