from pydantic import BaseModel
from typing import Type

from sqlalchemy.ext.declarative import DeclarativeMeta as Model


class BaseEndpoint():

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_endpoint_name() -> str:
        raise NotImplementedError

    @staticmethod
    def get_schema() -> Type[BaseModel]:
        raise NotImplementedError

    @staticmethod
    def get_model() -> Type[Model]:
        raise NotImplementedError
