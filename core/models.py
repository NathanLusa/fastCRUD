from typing import Type


class MethodType():
    def __init__(self, endpoint_name: str, method_type: str, need_model: bool = False):
        self.endpoint_name = endpoint_name
        self.method_type = method_type
        self.need_model = need_model
