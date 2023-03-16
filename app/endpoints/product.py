from typing import Type

from pydantic import BaseModel

from core.endpoints import BaseEndpoint


class Product(BaseModel):
    id: int
    name: str
    price: float


class ProductEndpoints(BaseEndpoint):
    def __init__(self) -> None:
        super().__init__()

    def get_path_prefix(self) -> str:
        return 'product'

    def get_schema(self) -> Type[BaseModel]:
        return Product

    # def get_model(self) -> Type[BaseModels]:
    #     return ProductModel
