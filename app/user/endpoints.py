from typing import Union
from pydantic import BaseModel

from core.endpoints import BaseEndpoint


variable = 'teste'


class User(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class UserEndpoints(BaseEndpoint):

    @staticmethod
    def create() -> str:
        return UserEndpoints.create.__module__ + '--' + variable

    @staticmethod
    def get_endpoint() -> str:
        return 'user'
