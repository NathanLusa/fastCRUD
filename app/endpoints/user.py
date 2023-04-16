from typing import Type

from pydantic import BaseModel

from app.database import BaseModels, get_db
from core.endpoints import BaseEndpoint


from fastapi import Depends
from sqlalchemy.orm import Session

from ..models.user import UserModel
from ..schemas.user import User


class UserEndpoints(BaseEndpoint):
    def __init__(self, db_func) -> None:
        super().__init__(db_func)

    def get_path_prefix(self) -> str:
        return 'user'

    def get_schema(self) -> Type[BaseModel]:
        return User

    def get_model(self) -> Type[BaseModels]:
        return UserModel

    def read(self, new_user_id: int, test: str):
        def _read(db: Session = Depends(self.db_func)):
            db = next(db.dependency())
            db_model = self.get_model()

            model = db.query(db_model).get(new_user_id)
            if model:
                return model            
            return {}
        
        return _read()
