from salinic.engine import create_engine
from salinic.index import get_ro_client_backend_class


def test_get_ro_client_backend_class():
    url = "solr://solr-solrcloud-0.solr-solrcloud-headless.default"
    engine = create_engine(url)
    assert get_ro_client_backend_class(engine)
