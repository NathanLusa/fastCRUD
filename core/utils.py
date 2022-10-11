from importlib import import_module
from inspect import getmembers, isclass, isfunction, ismethod, signature, Parameter
from typing import Dict, List, Sequence, Tuple, Type, Callable

from fastapi import FastAPI
from pydantic import BaseModel

from core import consts
from core.endpoints import BaseEndpoint
from core.models import MethodType

from .singleton import Singleton


class CrudRouter(metaclass=Singleton):

    def __init__(self, app: FastAPI) -> None:
        self.app: FastAPI = app
        self.__router_classes: List[Type[BaseEndpoint]] = []

    def __add_api_route(self, cls: Type[BaseEndpoint], endpoint_func_name: str, method_type: str) -> bool:
        for func_name, func in self.__get_func_list(cls):
            if func_name == endpoint_func_name:
                self.app.add_api_route(
                    path=f'/{cls.get_endpoint()}/{func_name}/',
                    endpoint=func,
                    methods=[method_type],
                )
                return True
        return False

    def __factory(self, type: str, cls: Type) -> Callable:
        def create():
            return cls.__name__

        def read():
            return cls.__name__

        def update():
            return cls.__name__

        def delete():
            return cls.__name__

        match type:
            case consts.CREATE:
                return create
            case consts.READ:
                return read
            case consts.UPDATE:
                return update
            case consts.DELETE:
                return delete
            case _:
                raise RuntimeError(f'Method type {type} not implemented.')

    def __get_func_list(self, cls: Type[BaseEndpoint]) -> List[Tuple[str, Callable]]:
        return getmembers(cls, lambda x: (isfunction(x) or ismethod(x)) and (x.__name__ in consts.ENDPOINT_FUNC_LIST))

    def __make_endpoint_methods(self, cls: Type[BaseEndpoint]) -> None:
        for method_type in consts.ENDPOINT_FUNC_TYPE_LIST:
            method_type.endpoint_name

            has_endpoint_func: bool = self.__add_api_route(
                cls, method_type.endpoint_name, method_type.method_type)

            if not has_endpoint_func:
                print(f'Need create {method_type.endpoint_name}')
                endpoint_func = self.__factory(method_type.endpoint_name, cls)
                endpoint_func.__module__ = cls.__name__

                sig = signature(endpoint_func)
                params: List[Parameter] = []
                print(method_type)
                if method_type.need_model:
                    param = Parameter(
                        cls.get_endpoint(),
                        kind=Parameter.POSITIONAL_OR_KEYWORD,
                        annotation=cls.get_model()
                    )
                    params.append(param)

                print(params)
                endpoint_func.__signature__ = sig.replace(  # type: ignore
                    parameters=params)

                cls.new_func = endpoint_func  # type: ignore
                self.app.add_api_route(
                    path=f'/{cls.get_endpoint()}/{endpoint_func.__name__}/',
                    endpoint=endpoint_func,
                    methods=[method_type.method_type],
                )

    def add_class(self, cls: Type[BaseEndpoint]):
        self.__router_classes.append(cls)
        self.__make_endpoint_methods(cls)
