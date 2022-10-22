from typing import Union, Type
from pydantic import BaseModel

from sqlalchemy.ext.declarative import DeclarativeMeta as Model

from core.endpoints import BaseEndpoint

from .schemas import UserModel


variable = 'teste'


class User(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Union[bool, None] = None


class UserEndpoints(BaseEndpoint):

    # @staticmethod
    # def create(user: User) -> str:
    #     return UserEndpoints.create.__module__ + '--' + variable

    @staticmethod
    def get_endpoint_name() -> str:
        return 'user'

    @staticmethod
    def get_schema() -> Type[BaseModel]:
        return User

    @staticmethod
    def get_model() -> Type[Model]:
        return UserModel
