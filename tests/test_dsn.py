import pytest

from salinic.dsn import Dsn


@pytest.mark.parametrize(
    "wrong_dsn",
    ["blah://some", "sulr://hostname:999", "yapian://path"]
)
def test_wrong_schema_name(wrong_dsn):
    with pytest.raises(ValueError):
        Dsn(wrong_dsn)


def test_xapian_scheme():
    dsn = Dsn("xapian://some-path")
    assert dsn.scheme == 'xapian'


def test_solr_scheme():
    dsn = Dsn("solr://host:port/path")
    assert dsn.scheme == 'solr'
