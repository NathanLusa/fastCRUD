from importlib import import_module
from inspect import getmembers, isclass, isfunction, ismethod, signature, Parameter
from turtle import up
from typing import Dict, List, Sequence, Tuple, Type, Callable

from fastapi import FastAPI
from pydantic import BaseModel

from core.endpoints import BaseEndpoint

from .singleton import Singleton

"""
def get_function_list(module):
    return getmembers(module, lambda x: isfunction(x) or ismethod(x))


def get_model(module, module_name: str):
    def class_filter(x):
        return isclass(x) and issubclass(x, BaseModel) and x.__name__.lower() == module_name

    try:
        _, model_class = getmembers(module, class_filter)[0]
        return model_class
    except IndexError:
        raise IndexError(
            f'Class inherated pydantic.BaseModel not declared on {module_name} module')


def add_routes(app: FastAPI):

    def factory(type, module):
        def create():
            return module.__name__

        def read():
            return module.__name__

        def update():
            return module.__name__

        def delete():
            return module.__name__

        methods = {
            'create': (create, 'POST'),
            'read': (read, 'GET'),
            'update': (update, 'PUT'),
            'delete': (delete, 'DELETE')
        }

        return methods[type]

    modules = ['user']
    for module_name in modules:
        module = import_module('.endpoints', f'app.{module_name}')

        model_class = get_model(module, module_name)

        method, method_type = factory('delete', module)
        method.__module__ = module.__name__

        sig = signature(method)
        params = []
        param = Parameter(
            module_name,
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            annotation=model_class
        )
        params.append(param)
        method.__signature__ = sig.replace(parameters=params)

        module.new_func = method

        for _, func in get_function_list(module):
            print(func)
            app.add_api_route(
                path=f'/{func.__module__.split(".")[-2]}/{func.__name__}/',
                endpoint=func,
                # methods=[method_type],
            )

"""


class CrudRouter(metaclass=Singleton):
    CREATE: str = 'create'
    READ: str = 'read'
    UPDATE: str = 'update'
    DELETE: str = 'delete'
    METHOD_LIST: List[str] = [CREATE, READ, UPDATE, DELETE]
    METHOD_TYPE_LIST: List[Tuple[str, str]] = [
        (CREATE, 'POST'),
        (READ, 'GET'),
        (UPDATE, 'PUT'),
        (DELETE, 'DELETE'),
    ]

    def __init__(self, app: FastAPI) -> None:
        self.app: FastAPI = app
        self.__router_classes: List[Type[BaseEndpoint]] = []

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
            case self.CREATE:
                return create
            case self.READ:
                return read
            case self.UPDATE:
                return update
            case self.DELETE:
                return delete
            case _:
                raise RuntimeError(f'Method type {type} not implemented.')

    def __make_endpoint_methods(self, cls: Type[BaseEndpoint]) -> None:
        func_list: List[Tuple[str, Callable]] = getmembers(cls, lambda x: (
            isfunction(x) or ismethod(x)) and (x.__name__ in self.METHOD_LIST))

        for method_type_name, method_type in self.METHOD_TYPE_LIST:
            has_method = False
            for func_name, func in func_list:
                has_method = func_name == method_type_name
                if has_method:
                    self.app.add_api_route(
                        path=f'/{cls.get_endpoint()}/{func_name}/',
                        endpoint=func,
                        methods=[method_type],
                    )
                    break

            if not has_method:
                print(f'Need create {method_type_name}')
                method = self.__factory(method_type_name, cls)
                method.__module__ = cls.__name__

                sig = signature(method)
                params: Sequence[Parameter] = []
                # param = Parameter(
                #     'module_name',
                #     kind=Parameter.POSITIONAL_OR_KEYWORD,
                #     # annotation=model_class
                # )
                # params.append(param)

                method.__signature__ = sig.replace(  # type: ignore
                    parameters=params)

                cls.new_func = method  # type: ignore
                self.app.add_api_route(
                    path=f'/{cls.get_endpoint()}/{method.__name__}/',
                    endpoint=method,
                    methods=[method_type],
                )

    def add_class(self, cls: Type[BaseEndpoint]):
        self.__router_classes.append(cls)
        self.__make_endpoint_methods(cls)
