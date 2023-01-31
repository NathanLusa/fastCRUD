from typing import Type
from pydantic import BaseModel

from app.database import Base
from core.endpoints import BaseEndpoint

from ..models.[class_min] import [class]Model
from ..schemas.[class_min] import [class]


class [class]Endpoints(BaseEndpoint):

    @staticmethod
    def get_endpoint_name() -> str:
        return '[class_min]'

    @staticmethod
    def get_schema() -> Type[BaseModel]:
        return [class]

    @staticmethod
    def get_model() -> Type[Base]:
        return [class]Model
