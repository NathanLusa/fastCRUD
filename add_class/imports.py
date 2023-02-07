from dataclasses import dataclass


@dataclass
class FieldImport:
    module: str
    type: str
