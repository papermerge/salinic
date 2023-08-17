
from salinic.dsn import Dsn


class Engine:
    def __init__(self, dsn: str):
        self.dsn = Dsn(dsn)


def create_engine(dsn: str) -> Engine:
    return Engine(dsn)
