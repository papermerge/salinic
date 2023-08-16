from pydantic import BaseModel

from salinic.query import SearchQuery


class Session:
    def __init__(self, client, schema, language="en"):
        self.client = client
        self._schema = schema
        self._language = language

    def add(self, entity: BaseModel):
        pass

    def remove(self, docid: str):
        pass

    def search(self, sq: SearchQuery):
        pass
