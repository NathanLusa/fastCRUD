from abc import ABC, abstractmethod
from inspect import Parameter
from datetime import datetime, timezone

from typing import List, Optional, Type, Callable, Generator, Any

from fastapi import APIRouter, Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.exc import IntegrityError

# try:
#     from sqlalchemy.orm import Session
#     from sqlalchemy.ext.declarative import DeclarativeMeta as Model
#     from sqlalchemy.exc import IntegrityError
# except ImportError:
#     Model = None
#     Session = None
#     IntegrityError = None
#     sqlalchemy_installed = False
# else:
#     sqlalchemy_installed = True
#     Session = Callable[..., Generator[Session, Any, None]]


from core._types import DEPENDENCIES, PAGINATION, PYDANTIC_SCHEMA as SCHEMA
from core import consts
from core.endpoints import BaseEndpoint
from core.models import MethodType
from core.singleton import Singleton
from core.utils import PaginationParams, schema_factory, get_func, get_param_name, get_path, create_parameter, replace_signature


CALLABLE = Callable[..., Model]
CALLABLE_LIST = Callable[..., List[Model]]


class CrudRouter(metaclass=Singleton):
    _router_classes: List[Type[BaseEndpoint]] = []

    def __init__(self, app: FastAPI) -> None:
        self.app: FastAPI = app

    @abstractmethod
    def _create(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> Callable:
        raise NotImplementedError

    # @abstractmethod
    def _read(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> Callable:
        raise NotImplementedError

    # @abstractmethod
    def _read_all(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> Callable:
        raise NotImplementedError

    # @abstractmethod
    def _update(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> Callable:
        raise NotImplementedError

    # @abstractmethod
    def _delete(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> Callable:
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

        if method_type.need_schema:
            schema_class = cls.get_schema()
            if method_type.endpoint_name == consts.CREATE:
                schema_class = schema_factory(
                    cls.get_schema(),
                    name=method_type.endpoint_name.capitalize()
                )

            param = create_parameter(
                cls.get_endpoint_name(),
                annotation=schema_class
            )
            params.append(param)

        if method_type.path:
            param = create_parameter(
                get_param_name(cls, method_type),
                annotation=int
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

    def add_class(self, cls: Type[BaseEndpoint]) -> None:
        self._router_classes.append(cls)
        self._make_endpoint_methods(cls)


class MemCrudRouter(CrudRouter):

    def _create(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any):
        def route(*args: Any, **kwargs: Any):
            return cls.__name__ + ' from route'
        return route

    def _read(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> Callable:
        def route(*args: Any, **kwargs: Any):
            return cls.__name__ + ' from route read'
        return route

    def _read_all(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> Callable:
        def route(*args: Any, **kwargs: Any):
            return cls.__name__ + ' from route read all'
        return route

    def _update(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> Callable:
        def route(*args: Any, **kwargs: Any):
            return cls.__name__ + ' from route update'
        return route

    def _delete(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> Callable:
        def route(*args: Any, **kwargs: Any):
            return cls.__name__ + ' from route delete'
        return route


class AlchemyCrudRouter(CrudRouter):

    def __init__(self,
                 app: FastAPI,
                 db: Any,
                 create_schema: Optional[Type[SCHEMA]] = None,
                 ) -> None:
        self.db_func = db
        self.create_schema = create_schema

        # self._pk_type: type = _utils.get_pk_type(schema, self._pk)

        super().__init__(app=app)

    def _create(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> CALLABLE:
        def route(db: Session = Depends(self.db_func), *args: Any, **kwargs: Any) -> Model:
            try:
                model = kwargs.get(cls.get_endpoint_name())
                db_model: Model = cls.get_model()()  # (**model.dict())

                if hasattr(db_model, 'created_at'):
                    setattr(db_model, 'created_at', datetime.now(timezone.utc))
                # breakpoint()
                for key, value in model.dict().items():
                    if hasattr(db_model, key):
                        setattr(db_model, key, value)

                db = next(db.dependency())
                db.add(db_model)
                db.commit()
                db.refresh(db_model)

                return db_model
            except IntegrityError:
                db.rollback()
                raise HTTPException(422, "Key already exists") from None

        return route

    def _read(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> CALLABLE:
        def route(db: Session = Depends(self.db_func), *args: Any, **kwargs: Any) -> Model:
            param_name = get_param_name(
                cls, consts.METHOD_TYPE_LIST[consts.READ])
            item_id = kwargs.get(param_name)
            db = next(db.dependency())
            db_model: Model = cls.get_model()

            model: Model = db.query(db_model).get(item_id)

            if model:
                return model
            else:
                raise consts.NOT_FOUND from None
        return route

    def _read_all(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> CALLABLE:
        def route(db: Session = Depends(self.db_func), *args: Any, **kwargs: Any) -> Model:
            pagination: PaginationParams = kwargs.get('pagination')
            skip, limit = pagination.skip, pagination.limit

            db = next(db.dependency())
            db_model: Model = cls.get_model()

            db_models: List[Model] = (
                db.query(db_model)
                # .order_by(getattr(db_model, self._pk))
                .limit(limit)
                .offset(skip)
                .all()
            )
            return db_models

        return route

    def _update(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> CALLABLE:
        def route(db: Session = Depends(self.db_func), *args: Any, **kwargs: Any) -> Model:
            param_name = get_param_name(
                cls, consts.METHOD_TYPE_LIST[consts.UPDATE])
            item_id = kwargs.get(param_name)
            db = next(db.dependency())
            db_model: Model = cls.get_model()

            actual_model: Model = db.query(db_model).get(item_id)
            client_model = kwargs.get(cls.get_endpoint_name())

            if not actual_model:
                raise consts.NOT_FOUND from None

            try:
                for key, value in client_model.dict(exclude={'id'}).items():
                    if hasattr(actual_model, key):
                        setattr(actual_model, key, value)

                if hasattr(db_model, 'updated_at'):
                    setattr(db_model, 'updated_at', datetime.now(timezone.utc))

                db.commit()
                db.refresh(actual_model)

                return actual_model
            except IntegrityError as e:
                db.rollback()
                self._raise(e)

        return route

    def _delete(self, cls: Type[BaseEndpoint], *args: Any, **kwargs: Any) -> CALLABLE:
        def route(db: Session = Depends(self.db_func), *args: Any, **kwargs: Any) -> Model:
            param_name = get_param_name(
                cls, consts.METHOD_TYPE_LIST[consts.DELETE])
            item_id = kwargs.get(param_name)
            db = next(db.dependency())

            db_model: Model = cls.get_model()
            delete_model: Model = db.query(db_model).get(item_id)

            if delete_model:
                db.delete(delete_model)
                db.commit()
                return delete_model
            else:
                raise consts.NOT_FOUND from None

        return route
