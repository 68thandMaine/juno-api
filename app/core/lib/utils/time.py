import re
from datetime import datetime

from app.core.lib.constants import INCORRECT_DATE


def convert_str_to_datetime(date_string: str) -> datetime:
    """Converts a string to a python date.

    Args:
        date_string (str): The expected format is MM/DD/YYYY

    Returns:
        datetime: Python date
    """
    request_pattern = re.compile("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$")
    internal_pattern = re.compile("^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
    if internal_pattern.match(date_string):
        date_string = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").strftime(
            "%m/%d/%Y"
        )
    if not request_pattern.match(date_string):
        raise ValueError(INCORRECT_DATE)

    date_object = datetime.strptime(date_string, "%m/%d/%Y")

    return date_object
