
class Engine:
    def __init__(self, dsn: str, **kwargs):
        self._dsn = dsn

    def get_session(self, schema, **kwargs):
        SessionClass = self.get_session_class()
        return SessionClass(self, schema, **kwargs)

    def get_session_class(self):
        pass

    def get_client(self, **kwargs):
        ClientClass = self.get_client_class()
        return ClientClass(self, **kwargs)

    def get_client_class(self):
        pass


def create_engine(dsn: str, **kwargs) -> Engine:
    return Engine(dsn, **kwargs)
