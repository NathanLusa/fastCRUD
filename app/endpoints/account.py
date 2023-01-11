from typing import Type
from pydantic import BaseModel

from app.database import Base
from core.endpoints import BaseEndpoint

from ..models.account import AccountModel
from ..schemas.account import Account


class AccountEndpoints(BaseEndpoint):

    @staticmethod
    def get_endpoint_name() -> str:
        return 'account'

    @staticmethod
    def get_schema() -> Type[BaseModel]:
        return Account

    @staticmethod
    def get_model() -> Type[Base]:
        return AccountModel

    # def read(user_id: int):
        # return {}
