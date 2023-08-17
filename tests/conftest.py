import pytest

from salinic.engine import Engine, create_engine


@pytest.fixture()
def engine(tmp_path) -> Engine:
    d = tmp_path / "index_db"
    d.mkdir()
    return create_engine(f"xapian://{d}")
