from pydantic import BaseModel

from app.enums import AccountStatusEnum, AccountTypeEnum


class Account(BaseModel):
    id: int
    name: str
    type: int
    status: int
