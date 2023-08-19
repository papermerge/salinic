import importlib

from salinic.query import SearchQuery


class IndexBase:
    def __init__(self, engine, schema):
        self.engine = engine
        self.schema = schema

    def search(self, sq: SearchQuery):
        return self.backend.search(sq)


class IndexRO(IndexBase):

    def __init__(self, engine, schema):
        super().__init__(engine, schema)
        self.backend = get_ro_index_backend(engine, schema)


class IndexRW(IndexBase):
    def __init__(self, engine, schema):
        super().__init__(engine, schema)
        self.backend = get_rw_index_backend(engine, schema)

    def add(self, entity):
        self.backend.add(entity)

    def remove(self, docid: str):
        self.backend.remove(docid)


def get_ro_client_backend_class(engine):
    module_full_path = f'salinic.backends.{engine.url.scheme}.client'
    module = importlib.import_module(module_full_path)

    return module.ClientRO


def get_rw_client_backend_class(engine):
    module_full_path = f'salinic.backends.{engine.url.scheme}.client'
    module = importlib.import_module(module_full_path)

    return module.ClientRW


def get_ro_index_backend_class(engine):
    module_full_path = f'salinic.backends.{engine.url.scheme}.index'
    module = importlib.import_module(module_full_path)

    return module.IndexRO


def get_rw_index_backend_class(engine):
    module_full_path = f'salinic.backends.{engine.url.scheme}.index'
    module = importlib.import_module(module_full_path)

    return module.IndexRW


def get_ro_index_backend(engine, schema):
    ClientKlass = get_ro_client_backend_class(engine)
    client = ClientKlass(engine.dsn)
    IndexKlass = get_ro_index_backend_class(engine)

    return IndexKlass(client, schema)


def get_rw_index_backend(engine, schema):
    ClientKlass = get_rw_client_backend_class(engine)
    client = ClientKlass(engine.url)
    IndexKlass = get_rw_index_backend_class(engine)
    return IndexKlass(client, schema)
