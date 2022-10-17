from inspect import getmembers, isfunction, ismethod, signature, Parameter, _empty
from typing import Any, List, Type, Callable

from fastapi import APIRouter, Depends, FastAPI

from core import consts
from core.endpoints import BaseEndpoint
from core.models import MethodType
from core.singleton import Singleton
from core.utils import PaginationParams, model_factory


class CrudRouter(metaclass=Singleton):

    def __init__(self, app: FastAPI) -> None:
        self.app: FastAPI = app
        self._router_classes: List[Type[BaseEndpoint]] = []

    def _factory(self, method_type: MethodType, cls: Type[BaseEndpoint]) -> Callable:
        def create(*args, **kwargs):
            return cls.__name__

        def read(*args, **kwargs):
            return cls.__name__

        def read_all(*args, **kwargs):
            return cls.__name__

        def update(*args, **kwargs):
            return cls.__name__

        def delete(*args, **kwargs):
            return cls.__name__

        def _get_param(param_name: str, annotation: Any | None = None, default=_empty) -> Parameter:
            return Parameter(
                param_name,
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                annotation=annotation,
                default=default
            )

        def _replace_signature(func: Callable, params: List[Parameter]):
            sig = signature(func)
            func.__signature__ = sig.replace(  # type: ignore
                parameters=params)

        params: List[Parameter] = []
        match method_type.endpoint_name:
            case consts.CREATE:
                endpoint_func = create
            case consts.READ:
                endpoint_func = read
            case consts.READ_ALL:
                endpoint_func = read_all
                param = _get_param(
                    'pagination', default=Depends(PaginationParams))
                params.append(param)
            case consts.UPDATE:
                endpoint_func = update
            case consts.DELETE:
                endpoint_func = delete
            case _:
                raise RuntimeError(f'Method type {type} not implemented.')

        if method_type.need_model:
            model_class = model_factory(
                cls.get_model(),
                name=cls.get_endpoint_name().capitalize()
            )
            model_class = cls.get_model()

            param = _get_param(cls.get_endpoint_name(),
                               annotation=model_class)
            params.append(param)
        _replace_signature(endpoint_func, params)

        return endpoint_func

    def _get_func(self, cls: Type[BaseEndpoint], func_name: str) -> Callable | None:
        func_list = getmembers(cls, lambda x: (isfunction(x) or ismethod(x)) and
                                              (x.__name__ == func_name))
        return func_list[0][1] if len(func_list) > 0 else None

    def _get_path(self, cls: Type[BaseEndpoint], method_type: MethodType) -> str:
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

    def _make_endpoint_methods(self, cls: Type[BaseEndpoint]) -> None:
        router = APIRouter(
            prefix=f'/{cls.get_endpoint_name()}', tags=[cls.get_endpoint_name().capitalize()])

        # Percorre os tipos de métodos padrões (create, read, update, delete)
        for method_type in consts.ENDPOINT_FUNC_TYPE_LIST:
            # Busca o método na classe pelo nome
            endpoint_func = self._get_func(cls, method_type.endpoint_name)

            # Não existe
            if not endpoint_func:
                print(
                    f'Creating endpoint: /{cls.get_endpoint_name()}/{method_type.endpoint_name}')
                # Chama a factory que já vai adicionar o método na classe
                endpoint_func = self._factory(method_type, cls)
                endpoint_func.__module__ = cls.__name__
                cls.new_func = endpoint_func  # type: ignore

            # Adicionar no router o método
            router.add_api_route(
                path=self._get_path(cls, method_type),
                endpoint=endpoint_func,
                methods=[method_type.method_type],
            )

        self.app.include_router(router)

    def add_class(self, cls: Type[BaseEndpoint]):
        self._router_classes.append(cls)
        self._make_endpoint_methods(cls)
