from typing import Dict, Optional, Sequence, TypeVar

from fastapi.params import Depends
from pydantic import BaseModel

PAGINATION = Dict[str, Optional[int]]
PYDANTIC_SCHEMA = BaseModel

T = TypeVar('T', bound=BaseModel)
DEPENDENCIES = Optional[Sequence[Depends]]
