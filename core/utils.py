from importlib import import_module
from inspect import getmembers, isclass, isfunction, ismethod, signature

from fastapi import FastAPI
from pydantic import BaseModel


def get_function_list(module):
    return getmembers(module, lambda x: isfunction(x) or ismethod(x))


def get_model(module, module_name: str):
    return getmembers(module, lambda x: isclass(x) and type(x) == BaseModel and x.__name__.lower() == module_name)


def add_routes(app: FastAPI):

    def factory(type, module, *args, **kwargs):
        def update():
            return module.__name__

        return update

    modules = ['user']
    for module_name in modules:
        module = import_module('.endpoints', f'app.{module_name}')

        model_class = get_model(module, module_name)

        # update.module = module
        # print(update.module)
        method = factory('', module)
        method.__module__ = module.__name__
        # signature(method, 'teste')
        method.__dict__ = {'teste': 1}
        print(method.__dict__)

        module.new_func = method

        for _, func in get_function_list(module):
            # print(func.__module__)
            app.add_api_route(
                path=f'/{func.__module__.split(".")[-2]}/{func.__name__}/',
                endpoint=func
            )
