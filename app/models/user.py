from sqlalchemy import Boolean, Column, Float, String

from app.database import BaseStatus


class UserModel(BaseStatus):
    # __tablename__ = 'users'

    name = Column(String)
    price = Column(Float)
    is_offer = Column(Boolean, default=False)
