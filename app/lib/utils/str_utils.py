from pydantic.utils import to_lower_camel


def camel_case(string: str | None):
    """Converts a string to camel case."""

    # need to replace spaces otherwise: `to_lower_camel("foo bar") == "foo bar"`
    return None if string is None else to_lower_camel(string.replace(" ", "_"))
