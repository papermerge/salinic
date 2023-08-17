import importlib

from salinic.dsn import Dsn


class Engine:
    def __init__(self, dsn: str):
        self.dsn = Dsn(dsn)

    def get_session(self, schema, **kwargs):
        SessionClass = self.get_session_class()
        return SessionClass(self, schema, **kwargs)

    def get_session_class(self):
        module_full_path = f'salinic.backends.{self.dsn.scheme}.session'
        module = importlib.import_module(module_full_path)

        return module.Session

    def get_client(self, **kwargs):
        ClientClass = self.get_client_class()
        return ClientClass(self, **kwargs)

    def get_client_class(self):
        module_full_path = f'salinic.backends.{self.dsn.scheme}.client'
        module = importlib.import_module(module_full_path)

        return module.Client


def create_engine(dsn: str) -> Engine:
    return Engine(dsn)
