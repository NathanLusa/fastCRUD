from typing import Type

from pydantic import BaseModel

from app.database import Base, BaseModels
from core.endpoints import BaseEndpoint

from ..models.account import AccountModel
from ..schemas.account import Account


class AccountEndpoints(BaseEndpoint):
    def __init__(self) -> None:
        super().__init__()

    def get_path_prefix(self) -> str:
        return 'account'

    def get_schema(self) -> Type[BaseModel]:
        return Account

    def get_model(self) -> Type[BaseModels]:
        return AccountModel
