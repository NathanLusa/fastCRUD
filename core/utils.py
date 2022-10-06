from importlib import import_module
from inspect import getmembers, isfunction, ismethod

from fastapi import FastAPI


def get_function_list(module):
    return getmembers(module, lambda x: isfunction(x) or ismethod(x))


def add_routes(app: FastAPI):
    modules = ['user']
    for module_name in modules:
        module = import_module(f'.{module_name}', 'app')

        for _, func in get_function_list(module):
            app.add_api_route(
                path=f'/{func.__module__.split(".")[-1]}/{func.__name__}/',
                endpoint=func
            )
