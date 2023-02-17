from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int


class BaseStatusSchema(BaseModel):
    status: int
