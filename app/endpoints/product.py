from typing import Type
from pydantic import BaseModel

from core.endpoints import BaseEndpoint


class Product(BaseModel):
    id: int
    name: str
    price: float


class ProductEndpoints(BaseEndpoint):

    @staticmethod
    def get_endpoint_name() -> str:
        return 'product'

    @staticmethod
    def get_schema() -> Type[BaseModel]:
        return Product
