import pytest

from app.controllers.category_controller import CategoryController
from app.controllers.payment_controller import PaymentController


@pytest.fixture
def payment_controller():
    return PaymentController()


@pytest.fixture
def category_controller():
    return CategoryController()
