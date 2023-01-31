import shutil
import sys

from sqlalchemy import types


FILES_PATH = '_teste/_FILES'
# BASE_PATH = '_teste'
BASE_PATH = 'app'
ENDPOINT_PATH = f'{BASE_PATH}/endpoints'
SCHEMA_PATH = f'{BASE_PATH}/schemas'
MODEL_PATH = f'{BASE_PATH}/models'


def get_sqlalchemy_type(python_type):
    match python_type:
        case 'int':
            return 'Integer'
        case 'str' | 'string':
            return 'String'
        case 'bool' | 'boolean':
            return 'Boolean'
        case 'float' | 'currency':
            return 'Float'
        case 'enum':
            return 'Enum'
        case 'date':
            return 'Date'
        case 'datetime':
            return 'Datetime'
        case 'time':
            return 'Time'
        case _:
            raise ValueError(
                f'{python_type} is not a supported Python built-in type')


def get_python_type(python_type):
    match python_type:
        case 'int':
            return 'int'
        case 'str' | 'string':
            return 'str'
        case 'bool' | 'boolean':
            return 'bool'
        case 'float' | 'currency':
            return 'float'
        case 'enum':
            return 'Enum'
        case 'date':
            return 'Date'
        case 'datetime':
            return 'Datetime'
        case 'time':
            return 'Time'
        case _:
            raise ValueError(
                f'{python_type} is not a supported Python built-in type')


def change_class(file, class_name):
    with open(file, 'r') as f:
        text = f.read()

    text = text.replace('[class]', class_name)
    text = text.replace('[class_min]', class_name.lower())

    with open(file, 'w') as f:
        f.write(text)


def add_schema(class_name: str, fields: list[dict[str, str]]):
    destination_file = f'{SCHEMA_PATH}/{class_name.lower()}.py'
    shutil.copy(f'{FILES_PATH}/schema.py', destination_file)
    change_class(destination_file, class_name)

    fields_str = ''

    for field in fields:
        name = field['name']
        field_type = get_python_type(field['type'])

        fields_str += '    ' if fields_str != '' else ''
        fields_str += f'{name}: {field_type}\n'

    # Write file
    with open(destination_file, 'r') as f:
        text = f.read()

    text = text.replace('[fields]', fields_str)

    with open(destination_file, 'w') as f:
        f.write(text)


def add_model(class_name: str, fields: list[dict[str, str]]):
    destination_file = f'{MODEL_PATH}/{class_name.lower()}.py'
    shutil.copy(f'{FILES_PATH}/model.py', destination_file)
    change_class(destination_file, class_name)

    fields_str = ''
    field_type_import = set()

    for field in fields:
        name = field['name']
        field_type = get_sqlalchemy_type(field['type'])

        field_type_import.add(field_type)

        fields_str += '    ' if fields_str != '' else ''
        fields_str += f'{name} = Column({field_type})\n'

    # Write file
    with open(destination_file, 'r') as f:
        text = f.read()

    text = text.replace('[fields]', fields_str)

    field_type_import_str = ''
    for x in field_type_import:
        field_type_import_str += f', {x}'

    text = text.replace('[fields_import]', field_type_import_str)

    with open(destination_file, 'w') as f:
        f.write(text)


def add_endpoint(class_name: str):
    destination_file = f'{ENDPOINT_PATH}/{class_name.lower()}.py'
    shutil.copy(f'{FILES_PATH}/endpoint.py', destination_file)
    change_class(destination_file, class_name)


def main(class_name: str, fields: list[dict[str, str]]):
    add_endpoint(class_name)
    add_model(class_name, fields)
    add_schema(class_name, fields)


# class_name = sys.argv[1]

class_name, *fields = sys.argv[1:]

fields = [{'name': y[0], 'type': y[1], }
          for y in [x.split(':') for x in fields]]

print(class_name, fields)

main(class_name, fields)
