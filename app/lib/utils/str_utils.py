from pydantic.alias_generators import to_camel


def camel_case(string: str | None):
    """Converts a string to camel case."""
    return None if string is None else to_camel(string.replace(" ", "_"))
