from typing import List, Type

from .models import MethodType, Path

CREATE: str = 'create'
READ: str = 'read'
READ_ALL: str = 'read_all'
UPDATE: str = 'update'
DELETE: str = 'delete'

ENDPOINT_FUNC_LIST: List[str] = [CREATE, READ, READ_ALL, UPDATE, DELETE]

ENDPOINT_FUNC_TYPE_LIST: List[MethodType] = [
    MethodType(CREATE, 'POST', need_schema=True),
    # MethodType(READ, 'GET', path=Path(suffix='_id')),
    # MethodType(READ_ALL, 'GET'),
    # MethodType(UPDATE, 'PUT', need_schema=True, path=Path(suffix='_id')),
    # MethodType(DELETE, 'DELETE', path=Path(suffix='_id')),
]
