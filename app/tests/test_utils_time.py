from datetime import date

import pytest

from app.core.lib.constants import INCORRECT_DATE
from app.core.lib.utils import time


def test_convert_str_to_datetime_returns_python_date():
    date_string = "11/12/1212"
    result = time.convert_str_to_datetime(date_string)
    assert isinstance(result, date)


@pytest.mark.parametrize(
    "incorrect_date, value_error",
    [
        ("", INCORRECT_DATE),
        ("test", INCORRECT_DATE),
        ("<script>alert()</script>", INCORRECT_DATE),
        ("1", INCORRECT_DATE),
    ],
)
def test_convert_str_to_datetime_raises_value_error(incorrect_date, value_error):
    with pytest.raises(ValueError) as exc_info:
        time.convert_str_to_datetime(incorrect_date)
    assert str(exc_info.value) == value_error
