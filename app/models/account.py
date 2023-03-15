from sqlalchemy import Boolean, Column, Enum, Float, Integer, String, UniqueConstraint

from app.database import BaseStatus
from app.enums import AccountStatusEnum, AccountTypeEnum


class AccountModel(BaseStatus):
    __tablename__ = 'account'

    name = Column(String)
    type = Column(Enum(AccountTypeEnum))
    # status = Column(Enum(AccountStatusEnum))

    __table_args__ = (
        UniqueConstraint('name', 'status', name='unique_name_type'),
    )
