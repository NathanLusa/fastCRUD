from typing import Type

from pydantic import BaseModel

from app.database import Base, BaseModels
from core.endpoints import BaseEndpoint

from ..models.user import UserModel
from ..schemas.user import User


class UserEndpoints(BaseEndpoint):
    def __init__(self) -> None:
        super().__init__()

    def get_path_prefix(self) -> str:
        return 'user'

    def get_schema(self) -> Type[BaseModel]:
        return User

    def get_model(self) -> Type[BaseModels]:
        return UserModel

    # def read(self, user_id: int):
    #     return {}
