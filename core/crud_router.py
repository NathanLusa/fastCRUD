from abc import ABC, abstractmethod
from inspect import Parameter
from typing import List, Type, Callable, Generator, Any

from fastapi import APIRouter, Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session
# from sqlalchemy.ext.declarative import DeclarativeMeta as Model
# from sqlalchemy.exc import IntegrityError

try:
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import DeclarativeMeta as Model
    from sqlalchemy.exc import IntegrityError
except ImportError:
    Model = None
    Session = None
    IntegrityError = None
    sqlalchemy_installed = False
else:
    sqlalchemy_installed = True
    Session = Callable[..., Generator[Session, Any, None]]


from core import consts
from core.endpoints import BaseEndpoint
from core.models import MethodType
from core.singleton import Singleton
from core.utils import PaginationParams, model_factory, get_func, get_path, create_parameter, replace_signature


class CrudRouter(metaclass=Singleton):
    _router_classes: List[Type[BaseEndpoint]] = []

    def __init__(self, app: FastAPI) -> None:
        self.app: FastAPI = app

    @abstractmethod
    def _create(self, cls: Type[BaseEndpoint], *args, **kwargs) -> Callable:
        raise NotImplementedError

    @abstractmethod
    def _read(self, cls: Type[BaseEndpoint], *args, **kwargs) -> Callable:
        raise NotImplementedError

    @abstractmethod
    def _read_all(self, cls: Type[BaseEndpoint], *args, **kwargs) -> Callable:
        raise NotImplementedError

    @abstractmethod
    def _update(self, cls: Type[BaseEndpoint], *args, **kwargs) -> Callable:
        raise NotImplementedError

    @abstractmethod
    def _delete(self, cls: Type[BaseEndpoint], *args, **kwargs) -> Callable:
        raise NotImplementedError

    def _factory(self, method_type: MethodType, cls: Type[BaseEndpoint]) -> Callable:
        params: List[Parameter] = []
        match method_type.endpoint_name:
            case consts.CREATE:
                endpoint_func = self._create(cls)

            case consts.READ:
                endpoint_func = self._read(cls)

            case consts.READ_ALL:
                endpoint_func = self._read_all(cls)
                param = create_parameter(
                    'pagination',
                    default=Depends(PaginationParams)
                )
                params.append(param)

            case consts.UPDATE:
                endpoint_func = self._update(cls)

            case consts.DELETE:
                endpoint_func = self._delete(cls)

            case _:
                raise RuntimeError(f'Method type {type} not implemented.')

        if method_type.need_model:
            model_class = cls.get_model()
            if method_type.endpoint_name == consts.CREATE:
                model_class = model_factory(
                    cls.get_model(),
                    name=method_type.endpoint_name.capitalize()
                )

            param = create_parameter(
                cls.get_endpoint_name(),
                annotation=model_class
            )
            params.append(param)

        replace_signature(endpoint_func, params)

        return endpoint_func

    def _make_endpoint_methods(self, cls: Type[BaseEndpoint]) -> None:
        router = APIRouter(
            prefix=f'/{cls.get_endpoint_name()}',
            tags=[cls.get_endpoint_name().capitalize()]
        )

        # Percorre os tipos de métodos padrões (create, read, update, delete)
        for method_type in consts.ENDPOINT_FUNC_TYPE_LIST:

            # Busca o método na classe pelo nome
            endpoint_func = get_func(cls, method_type.endpoint_name)

            # Não existe
            if not endpoint_func:
                # Chama a factory que já vai adicionar o método na classe
                endpoint_func = self._factory(method_type, cls)
                endpoint_func.__module__ = cls.__name__
                cls.new_func = endpoint_func  # type: ignore

            # Adicionar no router o método
            router.add_api_route(
                path=get_path(cls, method_type),
                endpoint=endpoint_func,
                methods=[method_type.method_type],
            )

        # Adiciona o router no app
        self.app.include_router(router)

    def add_class(self, cls: Type[BaseEndpoint]):
        self._router_classes.append(cls)
        self._make_endpoint_methods(cls)


class MemCrudRouter(CrudRouter):

    def _create(self, cls: Type[BaseEndpoint], *args, **kwargs):
        def route(*args, **kwargs):
            return cls.__name__ + ' from route'
        return route

    def _read(self, cls: Type[BaseEndpoint], *args, **kwargs) -> Callable:
        def route(*args, **kwargs):
            return cls.__name__ + ' from route read'
        return route

    def _read_all(self, cls: Type[BaseEndpoint], *args, **kwargs) -> Callable:
        def route(*args, **kwargs):
            return cls.__name__ + ' from route read all'
        return route

    def _update(self, cls: Type[BaseEndpoint], *args, **kwargs) -> Callable:
        def route(*args, **kwargs):
            return cls.__name__ + ' from route update'
        return route

    def _delete(self, cls: Type[BaseEndpoint], *args, **kwargs) -> Callable:
        def route(*args, **kwargs):
            return cls.__name__ + ' from route delete'
        return route


class AlchemyCrudRouter(CrudRouter):

    def __init__(self, app: FastAPI, db: Session) -> None:
        self.db_func = db
        super().__init__(app=app)

    def _create(self, db_schema) -> Callable:
        def route(
            model: self.create_schema,  # type: ignore
            db: Session = Depends(self.db_func),
        ) -> Model:
            try:
                db_model: Model = db_schema(**model.dict())
                db.add(db_model)
                db.commit()
                db.refresh(db_model)
                return db_model
            except IntegrityError:
                db.rollback()
                raise HTTPException(422, "Key already exists") from None

        return route
