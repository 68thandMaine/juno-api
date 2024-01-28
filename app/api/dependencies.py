"""
This module declares service dependencies that leverage the FastAPI `Depends()` method for effective dependency injection.
Each dependency corresponds to a CRUD (Create, Read, Update, Delete) service for a specific model.
"""

from app.models import Bill, Category, RecurringBill
from app.services.crud import CRUDService


async def get_bill_crud():
    """
    Returns a CRUD service instance for the 'Bill' model.
    """
    return CRUDService(model=Bill)


async def get_recurring_bill_crud():
    """
    Returns a CRUD service instance for the 'RecurringBill' model.
    """
    return CRUDService(model=RecurringBill)


async def get_category_crud():
    """
    Returns a CRUD service instance for the 'Category' model.
    """
    return CRUDService(model=Category)
