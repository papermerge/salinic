import pytest

from salinic import IndexRW
from salinic.engine import Engine, create_engine


@pytest.fixture()
def engine(tmp_path) -> Engine:
    d = tmp_path / "index_db"
    d.mkdir()
    return create_engine(f"xapian:///{d}")


@pytest.fixture()
def index(tmp_path, request):
    d = tmp_path / "index_db"
    d.mkdir()

    _engine = create_engine(f"xapian:///{d}")

    return IndexRW(_engine, schema=request.param)
