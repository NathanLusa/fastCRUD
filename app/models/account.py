from sqlalchemy import Boolean, Column, Integer, Float, String, Enum, UniqueConstraint

from app.database import Base
from app.enums import AccountTypeEnum, AccountStatusEnum


class AccountModel(Base):
    __tablename__ = 'account'

    name = Column(String)
    type = Column(Enum(AccountTypeEnum))
    status = Column(Enum(AccountStatusEnum))

    __table_args__ = (
        UniqueConstraint('name', 'status', name='unique_name_type'),
    )
