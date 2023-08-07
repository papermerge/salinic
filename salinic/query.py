from enum import Enum
from typing import List, NamedTuple


def extract_free_text(q: str) -> str:
    return q


def extract_filters(q: str) -> list[str]:
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
