from importlib import import_module
from inspect import getmembers, isfunction, ismethod

from fastapi import FastAPI


def add_routes(app: FastAPI):
    modules = ['user']
    for module_name in modules:
        module = import_module(f'.{module_name}', 'core')
        func_list = getmembers(module, lambda x: isfunction(x) or ismethod(x))

        for func_name, func in func_list:
            app.add_api_route(
                path=f'/{func.__module__.split(".")[-1]}/{func_name}',
                endpoint=func
            )
