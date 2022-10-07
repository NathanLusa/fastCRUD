from typing import Union
from pydantic import BaseModel

variable = 'teste'


class User(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


def create():
    return create.__module__ + '--' + variable
