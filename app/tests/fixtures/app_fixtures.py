import pytest
from app.controllers.payment_controller import PaymentController
from app.controllers.category_controller import CategoryController


@pytest.fixture
def payment_controller():
    return PaymentController()


@pytest.fixture
def category_controller():
    return CategoryController()
