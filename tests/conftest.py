import pytest

from salinic.engine import create_engine
from salinic.session import Session


@pytest.fixture()
def session(tmp_path) -> Session:
    d = tmp_path / "index_db"
    d.mkdir()
    engine = create_engine(f"xapian://{d}")

    return Session(engine)
