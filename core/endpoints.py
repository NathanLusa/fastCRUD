import abc
from typing import List, Type

from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta as Model


class BaseEndpoint(metaclass=abc.ABCMeta):
    def __init__(self, db_func) -> None:
        self._endpoints = []
        self.db_func = db_func

    @abc.abstractmethod
    def get_path_prefix(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_schema(self) -> Type[BaseModel]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_model(self) -> Model:
        raise NotImplementedError

    def get_endpoint_list(self) -> List[callable]:
        return self._endpoints

    def before_update(self, old_model: Model, new_model: Model):
        pass

    def after_update(self, model: Model):
        pass

    def before_delete(self, model: Model):
        pass

    def after_delete(self, model: Model):
        pass
    
    def before_create(self, model: Model):
        pass

    def after_create(self, model: Model):
        pass
