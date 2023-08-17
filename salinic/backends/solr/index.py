from pydantic import BaseModel

from salinic.query import SearchQuery


class Base:
    def __init__(self, client, schema):
        self.client = client
        self.schema = schema

    def search(self, sq: SearchQuery):
        pass


class IndexRO(Base):
    pass


class IndexRW(Base):
    def add(self, entity: BaseModel):
        pass

    def remove(self, docid: str):
        pass
