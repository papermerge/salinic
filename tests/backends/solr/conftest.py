import pytest

from salinic import SchemaManager
from salinic.engine import create_engine


@pytest.fixture()
def schema_manager(request):
    engine = create_engine("solr://localhost:8983/index")

    return SchemaManager(engine, model=request.param)
