import copy

import pytest

from app.tests.mocks.fake_data import bill_for_tests


@pytest.fixture
def setup_fake_bill():
    """Returns a json representation of a Bill object."""

    def _setup_fake_bill(overrides=None):
        fake_bill = copy.copy(bill_for_tests)
        if overrides:
            fake_bill.update(overrides)
        return fake_bill

    return _setup_fake_bill
