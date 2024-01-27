from datetime import datetime


def convert_str_to_datetime(string: str) -> datetime:
    return datetime.fromisoformat(string)
