import pytest

from salinic import IndexRW
from salinic.engine import create_engine


@pytest.fixture()
def solr_index(request):
    engine = create_engine("solr://localhost:8983/index")

    return IndexRW(engine, schema=request.param)
