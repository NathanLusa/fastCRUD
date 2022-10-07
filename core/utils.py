from importlib import import_module
from inspect import getmembers, isclass, isfunction, ismethod, signature, Parameter

from fastapi import FastAPI
from pydantic import BaseModel


def get_function_list(module):
    return getmembers(module, lambda x: isfunction(x) or ismethod(x))


def get_model(module, module_name: str):
    def class_filter(x):
        return isclass(x) and issubclass(x, BaseModel) and x.__name__.lower() == module_name

    try:
        _, model_class = getmembers(module, class_filter)[0]
        return model_class
    except IndexError:
        raise IndexError(
            f'Class inherated pydantic.BaseModel not declared on {module_name} module')


def add_routes(app: FastAPI):

    def factory(type, module):
        def create():
            return module.__name__

        def read():
            return module.__name__

        def update():
            return module.__name__

        def delete():
            return module.__name__

        methods = {
            'create': (create, 'POST'),
            'read': (read, 'GET'),
            'update': (update, 'PUT'),
            'delete': (delete, 'DELETE')
        }

        return methods[type]

    modules = ['user']
    for module_name in modules:
        module = import_module('.endpoints', f'app.{module_name}')

        model_class = get_model(module, module_name)

        method, method_type = factory('delete', module)
        method.__module__ = module.__name__

        sig = signature(method)
        params = []
        param = Parameter(
            module_name,
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            annotation=model_class
        )
        params.append(param)
        method.__signature__ = sig.replace(parameters=params)

        module.new_func = method

        for _, func in get_function_list(module):
            print(func)
            app.add_api_route(
                path=f'/{func.__module__.split(".")[-2]}/{func.__name__}/',
                endpoint=func,
                # methods=[method_type],
            )
