from typing import Type
from pydantic import BaseModel

from app.database import Base
from core.endpoints import BaseEndpoint

from .models import UserModel
from .schemas import User


class UserEndpoints(BaseEndpoint):

    @staticmethod
    def get_endpoint_name() -> str:
        return 'user'

    @staticmethod
    def get_schema() -> Type[BaseModel]:
        return User

    @staticmethod
    def get_model() -> Type[Base]:
        return UserModel

    # def read(user_id: int):
        # return {}
