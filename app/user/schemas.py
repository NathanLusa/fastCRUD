from sqlalchemy import Boolean, Column, Integer, Float, String

from app.database import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    is_offer = Column(Boolean, default=False)
