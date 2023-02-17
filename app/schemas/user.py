from typing import Union

from .base import BaseStatusSchema


class User(BaseStatusSchema):
    name: str
    price: float
    is_offer: Union[bool, None] = None
