import importlib


class SchemaManager:
    def __init__(self, engine, model):
        self.engine = engine
        self.model = model
        self.backend = get_schema_manager_backend(engine, model)

    def create(self):
        return self.backend.create()

    def apply(self):
        self.backend.apply()

    def delete(self):
        self.backend.delete()

    def create_dict_dump(self):
        return self.backend.create_dict_dump()

    def apply_dict_dump(self):
        return self.backend.apply_dict_dump()

    def delete_dict_dump(self):
        return self.backend.delete_dict_dump()


def get_schema_manager_backend(engine, model):
    ClientKlass = get_rw_client_backend_class(engine)
    client = ClientKlass(engine.url)
    SchemaManagerKlass = get_schema_manager_backend_class(engine)

    return SchemaManagerKlass(client, model)


def get_schema_manager_backend_class(engine):
    module_full_path = f'salinic.backends.{engine.url.scheme}.schema_manager'
    module = importlib.import_module(module_full_path)

    return module.SchemaManager


def get_rw_client_backend_class(engine):
    module_full_path = f'salinic.backends.{engine.url.scheme}.client'
    module = importlib.import_module(module_full_path)

    return module.ClientRW
