from importlib import import_module
from inspect import getmembers, isclass, isfunction, ismethod, signature, Parameter
from typing import Any, Dict, List, Sequence, Tuple, Type, Callable

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from core import consts
from core.endpoints import BaseEndpoint
from core.models import MethodType

from .singleton import Singleton


class CrudRouter(metaclass=Singleton):

    def __init__(self, app: FastAPI) -> None:
        self.app: FastAPI = app
        self.__router_classes: List[Type[BaseEndpoint]] = []

    def __add_api_route(self, cls: Type[BaseEndpoint], router: APIRouter, endpoint_func_name: str, method_type: str) -> bool:
        for func_name, func in self.__get_func_list(cls):
            if func_name == endpoint_func_name:
                router.add_api_route(
                    path='',
                    endpoint=func,
                    methods=[method_type],
                )
                return True
        return False

    def __factory(self, type: str, cls: Type) -> Callable:
        def create():
            return cls.__name__

        def read():
            return cls.__name__ + ' .. ' + read.__annotations__

        def update():
            return cls.__name__

        def delete():
            return cls.__name__

        def __get_param(param_name: str, anotation: Any | None = None) -> Parameter:
            return Parameter(
                param_name,
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                annotation=anotation
            )

        def __replace_signature(func: Callable, params: List[Parameter]):
            sig = signature(func)
            func.__signature__ = sig.replace(  # type: ignore
                parameters=params)

        params: List[Parameter] = []
        match type:
            case consts.CREATE:
                endpoint_func = create
                param = __get_param(cls.get_endpoint_name(), cls.get_model())
                params.append(param)
            case consts.READ:
                endpoint_func = read
                param = __get_param(f'{cls.get_endpoint_name()}_id', int)
                params.append(param)
            case consts.UPDATE:
                endpoint_func = update
            case consts.DELETE:
                endpoint_func = delete
                param = __get_param(f'{cls.get_endpoint_name()}_id', int)
                params.append(param)
            case _:
                raise RuntimeError(f'Method type {type} not implemented.')

        __replace_signature(endpoint_func, params)

        return endpoint_func

    def __get_func_list(self, cls: Type[BaseEndpoint]) -> List[Tuple[str, Callable]]:
        return getmembers(cls, lambda x: (isfunction(x) or ismethod(x)) and (x.__name__ in consts.ENDPOINT_FUNC_LIST))

    def __make_endpoint_methods(self, cls: Type[BaseEndpoint]) -> None:
        router = APIRouter(prefix=f'/{cls.get_endpoint_name()}')

        for method_type in consts.ENDPOINT_FUNC_TYPE_LIST:
            method_type.endpoint_name

            has_endpoint_func: bool = self.__add_api_route(
                cls, router, method_type.endpoint_name, method_type.method_type)

            if not has_endpoint_func:
                print(f'Need create {method_type.endpoint_name}')
                endpoint_func = self.__factory(method_type.endpoint_name, cls)
                endpoint_func.__module__ = cls.__name__

                cls.new_func = endpoint_func  # type: ignore
                # method_type.need_model
                router.add_api_route(
                    path='',
                    endpoint=endpoint_func,
                    methods=[method_type.method_type],
                )
        self.app.include_router(router)

    def add_class(self, cls: Type[BaseEndpoint]):
        self.__router_classes.append(cls)
        self.__make_endpoint_methods(cls)
