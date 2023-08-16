from pydantic import BaseModel

from .query import SearchQuery


class Session:
    def __init__(self, engine, schema, **kwargs):
        self.backend = engine.get_session(schema, **kwargs)

    def add(self, entity: BaseModel):
        self.backend.add(entity)

    def remove(self, docid: str):
        self.backend.remove(docid)

    def search(self, sq: SearchQuery):
        return self.backend.search(sq)
