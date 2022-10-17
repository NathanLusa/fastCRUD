from typing import Type, TypeVar

from pydantic import BaseModel, create_model


T = TypeVar("T", bound=BaseModel)


class PaginationParams:
    def __init__(self, skip: int = 0, limit: int = 20):
        self.skip = skip
        self.limit = limit


def model_factory(model_cls: Type[T], pk_field_name: str = "id", name: str = "Create") -> Type[T]:
    """
    Is used to create a Createmodel which does not contain pk
    """

    fields = {
        f.name: (f.type_, ...)
        for f in model_cls.__fields__.values()
        if f.name != pk_field_name
    }

    name = model_cls.__name__ + name
    model: Type[T] = create_model(__model_name=name, **fields)  # type: ignore
    return model
