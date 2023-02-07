from dataclasses import dataclass

from imports import FieldImport


@dataclass
class FieldType:
    model_type: str
    schema_type: str
    import_model_type: FieldImport = None
    import_schema_type: FieldImport = None


class IntField(FieldType):
    model_type = 'Integer'
    schema_type = 'int'
    import_model_type = FieldImport('sqlalchemy', 'Integer')


class StrField(FieldType):
    model_type = 'String'
    schema_type = 'str'
    import_model_type = FieldImport('sqlalchemy', 'String')


class BoolField(FieldType):
    model_type = 'Boolean'
    schema_type = 'bool'
    import_model_type = FieldImport('sqlalchemy', 'Boolean')


class FloatField(FieldType):
    model_type = 'Float'
    schema_type = 'float'
    import_model_type = FieldImport('sqlalchemy', 'Float')


class DateField(FieldType):
    model_type = 'Date'
    schema_type = 'date'
    import_model_type = FieldImport('sqlalchemy', 'Date')
    import_schema_type = FieldImport('datetime', 'date')


class DateTimeField(FieldType):
    model_type = 'DateTime'
    schema_type = 'datetime'
    import_model_type = FieldImport('sqlalchemy', 'DateTime')
    import_schema_type = FieldImport('datetime', 'datetime')


class TimeField(FieldType):
    model_type = 'Time'
    schema_type = 'time'
    import_model_type = FieldImport('sqlalchemy', 'Time')
    import_schema_type = FieldImport('time', 'time')


class EnumField(FieldType):
    model_type = 'Enum'


class Field():
    _FIELD_TYPES = {
        'int': IntField,
        'integer': IntField,
        'str': StrField,
        'string': StrField,
        'bool': BoolField,
        'boolean': BoolField,
        'float': FloatField,
        'currency': FloatField,
        'enum': EnumField,
        'date': DateField,
        'datetime': DateTimeField,
        'time': TimeField,
    }

    _field_type: FieldType = None

    def __init__(self, name: str, field_type: str) -> None:
        self.name = name
        self.field_type = field_type
        self._field_type = self._get_field_type()

    def _get_field_type(self):
        if not self.field_type.lower() in self._FIELD_TYPES:
            raise ValueError(
                f'{self.field_type} is not a supported Python built-in type >> {self.name}')

        return self._FIELD_TYPES[self.field_type.lower()]

    def as_model(self) -> str:
        return f'    {self.name} = Column({self._field_type.model_type})\n'

    def as_schema(self) -> str:
        return f'    {self.name}: {self._field_type.schema_type}\n'

    def get_import_model(self) -> FieldImport:
        return self._field_type.import_model_type

    def get_import_schema(self) -> FieldImport:
        return self._field_type.import_schema_type
