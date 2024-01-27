from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from app.lib.utils.str_utils import camel_case


class CamelCaseModel(BaseModel):
    """Use to convert a model's attributes to camel case.
    If used as a response model, all public attributes will be transformed to camel case.
    This is useful when consuming a model schema in an environment that follows a camel case
    naming convention instead of snake case.

    Note: must specify `by_alias=True` when serializing a model as a dict/json
    i.e.: `my_model_instance.json(by_alias=True)`.

    ## Example use

    ```python
    class Foo(CamelCaseModel):
        some_id: str

    foo = Foo(some_id="my custom id")
    foo.json(by_alias=True) # returns {"someId": "my custom id"}
    ```

    ## FastAPI Response Model use

    ```python
    class FooResponse(CamelCaseModel):
        some_id: str

    @router.get("/foo", response_model=FooResponse)
    def get_foo():
        # returned JSON: { "someId": "custom id"}
        return FooResponse(some_id="custom id")

    ```
    """

    class ConfigDict:
        alias_generator = camel_case
        allow_population_by_field_name = True


class IdBase(CamelCaseModel, SQLModel):
    """
    Provides the base ID for all models and introduces code to
    swap snake_case and camel case.
    """

    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
