from dataclasses import dataclass, field

from fields import Field


@dataclass
class CreateClass:
    name: str
    fields: list[Field] = field(default_factory=list)

    def _get_import_str(self, imports) -> str:
        text = ''
        for index, module in enumerate(imports.keys()):
            text += '\n' if index != 0 else ''
            text += f'from {module} import '

            for index, name in enumerate(imports[module]):
                text += ', ' if index != 0 else ''
                text += name

        return text

    def _replate_base(self, template_text: str) -> str:
        text = template_text
        text = text.replace('[class]', self.name.capitalize())
        text = text.replace('[class_min]', self.name.lower())
        return text

    def add_field(self, name: str, field_type: str) -> Field:
        field = Field(name, field_type)
        self.fields.append(field)
        return field

    def replace_endpoint_template(self, template_text: str) -> str:
        text = self._replate_base(template_text)
        return text

    def replace_model_template(self, template_text: str) -> str:
        text = self._replate_base(template_text)

        imports = {'sqlalchemy': {'Column'}}

        fields_str = ''
        for field in self.fields:
            fields_str += field.as_model()
            field_import = field.get_import_model()
            if field_import:
                if not field_import.module in imports:
                    imports.update({field_import.module: set([])})
                imports[field_import.module].add(field_import.type)

        field_type_import_str = self._get_import_str(imports)

        text = text.replace('[fields]', fields_str)
        text = text.replace('[fields_import]', field_type_import_str)

        return text

    def replace_schema_template(self, template_text: str) -> str:
        text = self._replate_base(template_text)

        imports: dict(str, set) = {}

        fields_str = ''
        for field in self.fields:
            fields_str += field.as_schema()
            field_import = field.get_import_schema()
            if field_import:
                if not field_import.module in imports:
                    imports.update({field_import.module: set([])})
                imports[field_import.module].add(field_import.type)

        field_type_import_str = self._get_import_str(imports)

        text = text.replace('[fields]', fields_str)
        text = text.replace('[fields_import]', field_type_import_str)
        text = text.replace('[base_class]', 'Base')

        return text
