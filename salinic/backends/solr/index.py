from pydantic import BaseModel

from salinic.query import SearchQuery
from salinic.utils import filter_keys, trim_suffixes


class Base:
    def __init__(self, client, schema):
        self.client = client
        self.schema = schema

    def search(self, sq: SearchQuery):
        result = self.client.search(sq)
        if result['numFound'] == 0:
            return []

        docs_list = [
            trim_suffixes(doc) for doc in result['response']['docs']
        ]
        docs = filter_keys(docs_list, ['_version_'])

        return [sq.entity(**doc) for doc in docs]


class IndexRW(Base):
    def add(self, model: BaseModel):
        self.client.add(model)

    def remove(self, docid: str):
        self.client.remove(docid)


IndexRO = IndexRW
