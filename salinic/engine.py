
from salinic.url import make_url


class Engine:
    def __init__(self, url: str):
        self.url = make_url(url)


def create_engine(url: str) -> Engine:
    return Engine(url)
