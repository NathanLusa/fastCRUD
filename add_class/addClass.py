import shutil
import sys

from classes import CreateClass

from sqlalchemy import types


FILES_PATH = '_teste/_FILES'
BASE_PATH = '_teste'
# BASE_PATH = 'app'
ENDPOINT_PATH = f'{BASE_PATH}/endpoints'
SCHEMA_PATH = f'{BASE_PATH}/schemas'
MODEL_PATH = f'{BASE_PATH}/models'


def replace_text(file: str, replate_method):
    with open(file, 'r') as f:
        text = f.read()

    text = replate_method(text)

    with open(file, 'w') as f:
        f.write(text)


def add_schema(class_name: str, create_class: CreateClass):
    destination_file = f'{SCHEMA_PATH}/{class_name.lower()}.py'
    shutil.copy(f'{FILES_PATH}/schema.pyt', destination_file)

    replace_text(destination_file, create_class.replace_schema_template)


def add_model(class_name: str, create_class: CreateClass):
    destination_file = f'{MODEL_PATH}/{class_name.lower()}.py'
    shutil.copy(f'{FILES_PATH}/model.pyt', destination_file)

    replace_text(destination_file, create_class.replace_model_template)


def add_endpoint(class_name: str, create_class: CreateClass):
    destination_file = f'{ENDPOINT_PATH}/{class_name.lower()}.py'
    shutil.copy(f'{FILES_PATH}/endpoint.pyt', destination_file)

    replace_text(destination_file, create_class.replace_endpoint_template)


def main(class_name: str, fields: list[dict[str, str]]):
    create_class = CreateClass(name=class_name.lower())
    for field in fields:
        create_class.add_field(field['name'], field['type'])

    add_endpoint(class_name, create_class)
    add_model(class_name, create_class)
    add_schema(class_name, create_class)


if __name__ == '__main__':
    ''
    class_name, *fields = sys.argv[1:]

    fields = [{'name': y[0], 'type': y[1], }
              for y in [x.split(':') for x in fields]]

    main(class_name, fields)
