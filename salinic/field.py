from typing import NamedTuple


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
