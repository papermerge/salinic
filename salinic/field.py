from typing import NamedTuple


class Field(NamedTuple):
    primary_key: bool = False
    store: bool = True
    index: bool = True
    general_search: bool = False
    default: any = None
    multi_value: bool = False
    multi_lang: bool = False
    # enables grouping by this field
    group: bool = False


class KeywordField(Field):
    pass


class TextField(Field):
    pass


class NumericField(Field):
    pass


class StringField(Field):
    pass


class IdField(Field):
    pass


class UUIDField(Field):
    pass
