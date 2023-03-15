from typing import List, Type

from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta as Model


class BaseEndpoint:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_endpoint_name() -> str:
        raise NotImplementedError

    @staticmethod
    def get_schema() -> Type[BaseModel]:
        raise NotImplementedError

    @staticmethod
    def get_model() -> Model:
        raise NotImplementedError

    @staticmethod
    def get_endpoint_list() -> List[callable]:
        return []
