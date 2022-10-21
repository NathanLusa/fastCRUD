# from typing import Type


class Path():
    def __init__(self, name: str = '', prefix: str = '', suffix: str = ''):
        self.name = name
        self.prefix = prefix
        self.suffix = suffix

        if self.name and (self.prefix or self.suffix):
            raise TypeError(
                'Não é permitido informar nome junto com prefixo ou sufixo')


class MethodType():
    def __init__(self, endpoint_name: str, method_type: str, need_schema: bool = False, path: Path | None = None):
        self.endpoint_name = endpoint_name
        self.method_type = method_type
        self.need_schema = need_schema
        self.path = path
