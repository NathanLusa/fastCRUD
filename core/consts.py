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

METHOD_TYPE_LIST = {
    CREATE: MethodType(CREATE, 'POST', need_schema=True),
    UPDATE: MethodType(UPDATE, 'PUT', need_schema=True, path=Path(suffix='_id')),
    READ: MethodType(READ, 'GET', path=Path(suffix='_id')),
    READ_ALL: MethodType(READ_ALL, 'GET'),
    DELETE: MethodType(DELETE, 'DELETE', path=Path(suffix='_id'))
}

ENDPOINT_FUNC_TYPE_LIST: List[MethodType] = [
    METHOD_TYPE_LIST[CREATE],
    METHOD_TYPE_LIST[READ],
    METHOD_TYPE_LIST[READ_ALL],
    METHOD_TYPE_LIST[UPDATE],
    METHOD_TYPE_LIST[DELETE],
]
