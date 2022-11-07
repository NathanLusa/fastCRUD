from typing import List, Type

from fastapi import HTTPException

from .models import MethodType, Path


NOT_FOUND = HTTPException(404, "Item not found")

CREATE: str = 'create'
READ: str = 'read'
READ_ALL: str = 'read_all'
UPDATE: str = 'update'
DELETE: str = 'delete'

ENDPOINT_FUNC_LIST: List[str] = [CREATE, READ, READ_ALL, UPDATE, DELETE]

CREATE_METHOD_TYPE = MethodType(CREATE, 'POST', need_schema=True)
UPDATE_METHOD_TYPE = MethodType(
    UPDATE, 'PUT', need_schema=True, path=Path(suffix='_id'))

ENDPOINT_FUNC_TYPE_LIST: List[MethodType] = [
    CREATE_METHOD_TYPE,
    # MethodType(READ, 'GET', path=Path(suffix='_id')),
    # MethodType(READ_ALL, 'GET'),
    UPDATE_METHOD_TYPE,
    # MethodType(DELETE, 'DELETE', path=Path(suffix='_id')),
]
