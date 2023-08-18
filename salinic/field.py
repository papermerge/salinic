from typing import NamedTuple


class Field(NamedTuple):
    primary_key: bool = False
    store: bool = True
    index: bool = True
    general_search: bool = False
    default: any = None


class KeywordField(Field):
    multi_value: bool = False


class TextField(Field):
    multi_lang: bool = False


class NumericField(Field):
    pass


class IdField(Field):
    pass


class UUIDField(Field):
    pass
