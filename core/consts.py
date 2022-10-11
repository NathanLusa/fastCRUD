from typing import List, Type

from .models import MethodType

CREATE: str = 'create'
READ: str = 'read'
UPDATE: str = 'update'
DELETE: str = 'delete'

ENDPOINT_FUNC_LIST: List[str] = [CREATE, READ, UPDATE, DELETE]

# ENDPOINT_FUNC_TYPE_LIST: List[Tuple[str, str]] = [
#     (CREATE, 'POST'),
#     (READ, 'GET'),
#     (UPDATE, 'PUT'),
#     (DELETE, 'DELETE'),
# ]


ENDPOINT_FUNC_TYPE_LIST: List[MethodType] = [
    MethodType(endpoint_name=CREATE, method_type='POST', need_model=True),
    MethodType(endpoint_name=READ, method_type='GET'),
    MethodType(endpoint_name=UPDATE, method_type='PUT', need_model=True),
    MethodType(endpoint_name=DELETE, method_type='DELETE'),
]
