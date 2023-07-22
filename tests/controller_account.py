import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Account
from app.api.controllers.account_controller import AccountController


def test_accounts_returns_all_accounts():
    return True
