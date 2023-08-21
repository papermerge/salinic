"""Solr specific types"""
from enum import Enum
from typing import List

from pydantic import BaseModel


def to_dash(string: str) -> str:
    return '-'.join(word for word in string.split('_'))


class FieldType(str, Enum):
    text_general = 'text_general'
    pint = 'pint'


class CopyFieldDump(BaseModel):
    source: str
    dest: List[str]


class FieldDump(BaseModel):
    name: str
    type: FieldType
    multiValued: bool
    indexed: bool
    stored: bool
