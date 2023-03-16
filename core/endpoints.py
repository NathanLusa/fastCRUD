import abc
from typing import List, Type

from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta as Model


class BaseEndpoint(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._endpoints = []

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
