from salinic.engine import create_engine


def test_engine():
    engine = create_engine('solr://solr-instance.default')
    assert engine.url.scheme == 'solr'
    assert str(engine.url.scheme) == 'solr'
