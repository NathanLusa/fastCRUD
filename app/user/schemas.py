from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Union[bool, None] = None
