from typing import List, Tuple


CREATE: str = 'create'
READ: str = 'read'
UPDATE: str = 'update'
DELETE: str = 'delete'

ENDPOINT_FUNC_LIST: List[str] = [CREATE, READ, UPDATE, DELETE]

ENDPOINT_FUNC_TYPE_LIST: List[Tuple[str, str]] = [
    (CREATE, 'POST'),
    (READ, 'GET'),
    (UPDATE, 'PUT'),
    (DELETE, 'DELETE'),
]
