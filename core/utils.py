from inspect import getmembers, isfunction, ismethod, signature, Parameter, _empty
from typing import Any, Callable, List, Type, TypeVar

from pydantic import BaseModel, create_model

from core.endpoints import BaseEndpoint
from core.models import MethodType


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


def get_func(cls: Type[BaseEndpoint], func_name: str) -> Callable | None:
    func_list = getmembers(cls, lambda x: (isfunction(x) or ismethod(x)) and
                           (x.__name__ == func_name))
    return func_list[0][1] if len(func_list) > 0 else None


def get_path(cls: Type[BaseEndpoint], method_type: MethodType) -> str:
    path_name = ''
    if method_type.path:
        path_name = '/{'
        if method_type.path.prefix:
            path_name += method_type.path.prefix + cls.get_endpoint_name()

        if method_type.path.suffix:
            if not method_type.path.prefix:
                path_name += cls.get_endpoint_name()
            path_name += method_type.path.suffix

        if method_type.path.name:
            path_name = f'/{method_type.path.name}'
        else:
            path_name += '}'

    return path_name


def create_parameter(param_name: str, annotation: Any | None = None, default=_empty) -> Parameter:
    return Parameter(
        param_name,
        kind=Parameter.POSITIONAL_OR_KEYWORD,
        annotation=annotation,
        default=default
    )


def replace_signature(func: Callable, params: List[Parameter]):
    sig = signature(func)
    func.__signature__ = sig.replace(  # type: ignore
        parameters=params)
