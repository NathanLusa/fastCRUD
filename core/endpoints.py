from pydantic import BaseModel
from typing import Type


class BaseEndpoint():

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_endpoint() -> str:
        raise NotImplementedError()

    @staticmethod
    def get_model() -> Type[BaseModel]:
        raise NotImplementedError()
