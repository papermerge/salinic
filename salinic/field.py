from enum import Enum
from typing import List, NamedTuple

from pydantic import BaseModel


class FieldType(str, Enum):
    text_general = 'text_general'


class CopyFieldDump(BaseModel):
    source: str
    dest: List[str]


class FieldDump(BaseModel):
    name: str
    type: str
    multiValued: bool
    indexed: bool
    stored: bool


class Field(NamedTuple):
    primary_key: bool = False
    store: bool = True
    index: bool = True
    general_search: bool = False
    default: any = None
    multi_value: bool = False
    multi_lang: bool = False


class KeywordField(Field):
    pass


class TextField(Field):
    pass


class NumericField(Field):
    pass


class IdField(Field):
    pass


class UUIDField(Field):
    pass
