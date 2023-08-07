import re
from enum import Enum
from typing import List, NamedTuple, Tuple

"""
Filter is a character sequence of format:
    <name>:<values>

where values can be separated by comma.
Examples:
    1. tags:important  => one value
    2. tags:important,paid => two values
    3. tags:invoice, paid => two values

Filters may contain one single value composed from multiple
words, but in such case you need to include them single
or double quotes.
Examples:
    1. breadcrumb:"My Documents"
    2. breadcrumb:'My bills'
"""


def first_filter_beg_pos(text: str) -> int | None:
    """Returns the beginning position of the first filter"""
    first_column_pos = text.find(':')

    if first_column_pos < 0:
        return None

    beg_pos = first_column_pos - 1

    while beg_pos >= 0:
        if re.match(r'\w', text[beg_pos]):
            beg_pos -= 1
        else:
            break

    return beg_pos + 1


def first_filter_end_pos(text: str) -> int | None:
    """Returns the end position of the first filter"""
    if text is None:
        return None

    first_column_pos = text.find(':')

    if first_column_pos < 0:
        return None

    text_len = len(text)
    end_pos = first_column_pos + 1
    if text[end_pos] in "\'\"":
        pattern = r'[\w ]'  # with white space
        end_pos += 1  # skip initial quotes
    else:
        pattern = r'\w'  # without white space

    while end_pos < text_len:
        if re.match(pattern, text[end_pos]):
            end_pos += 1
        else:
            break

    return end_pos - 1


def first_filter_pos(text: str) -> Tuple[int, int] | None:
    first_column_pos = text.find(':')

    if first_column_pos < 0:
        return None

    beg_pos = first_filter_beg_pos(text)
    end_pos = first_filter_end_pos(text)

    return beg_pos, end_pos


def extract_free_text(q: str) -> str:
    pass


def extract_filters(q: str) -> List[str]:
    return []


class FreeTextQuery(NamedTuple):
    text: str

    def __str__(self):
        return self.text


class FilterQueryOP(Enum):
    # filter query operation
    AND = 1
    OR = 2


class FilterQuery(NamedTuple):
    text: str  # original filter text
    name: str
    values: List[str]
    # which operation should the filter perform on the
    # values? Should it be AND? Should it be OR?
    op: FilterQueryOP  # AND | OR


class Query:
    free_text: FreeTextQuery
    filters: List[FilterQuery]

    def __init__(self, query: str):
        self.free_text = FreeTextQuery(extract_free_text(query))
        self.filters = [
            FilterQuery(filter_q) for filter_q in extract_filters(query)
        ]

    def get_filters_by(self, name: str) -> List[FilterQuery]:
        return [f for f in self.filters if f.name == name]


class SearchQuery:
    query: Query

    def __init__(self, entity, query: str):
        self.entity = entity
        self.query = Query(query)
