from salinic.engine import create_engine


def test_engine_get_session_class_for_xapian():
    from salinic.backends.xapian.session import Session

    engine = create_engine('xapian://some-path')
    assert Session == engine.get_session_class()


def test_engine_get_session_class_for_solr():
    from salinic.backends.solr.session import Session

    engine = create_engine('solr://host-name:8389/')
    assert Session == engine.get_session_class()
