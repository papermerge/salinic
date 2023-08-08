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

Notice that in example 3. there is a white space after comma.

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
    pattern = r'[\w\, ]'
    at_least_one_comma = False
    with_quotes = False

    if text[end_pos] in "\'\"":
        end_pos += 1  # skip initial quotes
        with_quotes = True

    while end_pos < text_len:
        if re.match(pattern, text[end_pos]):
            if text[end_pos] == ' ':
                if at_least_one_comma or with_quotes:
                    end_pos += 1
                    continue
                else:
                    break
            if text[end_pos] == ',':
                at_least_one_comma = True
            end_pos += 1
        else:
            if text[end_pos] in "\'\"":
                end_pos += 1
            break

    return end_pos - 1


def first_filter_pos(text: str) -> Tuple[int, int] | None:
    first_column_pos = text.find(':')

    if first_column_pos < 0:
        return None

    beg_pos = first_filter_beg_pos(text)
    end_pos = first_filter_end_pos(text)

    return beg_pos, end_pos


def extract_free_text(text: str) -> str | None:
    pos = first_filter_pos(text)
    if pos is None:
        return text

    result = text[:pos[0]] + text[pos[1] + 1:]
    stripped_result = result.strip()

    if len(stripped_result) == 0:
        return None

    return stripped_result


def extract_filters(text: str) -> List[str]:
    # TODO: support multiple filters
    result = []
    pos = first_filter_pos(text)
    if pos is None:
        return result

    result.append(text[pos[0]:pos[1] + 1])

    return result


class FreeTextQuery(NamedTuple):
    text: str | None

    def __str__(self):
        if not self.text:
            return ''

        return self.text


class FilterQueryOP(Enum):
    # filter query operation
    AND = 1
    OR = 2


class FilterQuery:
    text: str  # original filter text
    name: str
    values: List[str]
    # which operation should the filter perform on the
    # values? Should it be AND? Should it be OR?
    op: FilterQueryOP = FilterQueryOP.AND  # AND | OR

    def __init__(self, text: str):
        self.text = text
        self.name, self.values = text.split(':')
        self.values = [v.strip() for v in self.values.split(',')]


class Query:
    original_query: str
    free_text: FreeTextQuery
    filters: List[FilterQuery]

    def __init__(self, query: str):
        self.original_query = query
        self.free_text = FreeTextQuery(extract_free_text(query))
        self.filters = [
            FilterQuery(filter_q) for filter_q in extract_filters(query)
        ]

    def get_filters_by(self, name: str) -> List[FilterQuery]:
        return [f for f in self.filters if f.name == name]

    def __repr__(self):
        return f"Query(free_text='{self.free_text}', filters={self.filters})"


class SearchQuery:
    query: Query

    def __init__(self, entity, query: str):
        self.entity = entity
        self.query = Query(query)

    def __str__(self):
        return f"SearchQuery(query={self.query}, entity={self.entity})"

    def __repr__(self):
        return f"SearchQuery(query={self.query}, entity={self.entity})"
