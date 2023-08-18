import pytest

from salinic.url import make_url


@pytest.mark.parametrize(
    "wrong_dsn",
    ["blah://some", "sulr://hostname:999", "yapian://path"]
)
def test_wrong_schema_name(wrong_dsn):
    with pytest.raises(ValueError):
        make_url(wrong_dsn)


def test_xapian_scheme():
    url = make_url("xapian://some-path")
    assert url.scheme == 'xapian'
    assert url.host == 'some-path'


def test_solr_scheme():
    url = make_url("solr://myhost:6000/path")
    assert url.scheme == 'solr'
    assert url.host == 'myhost'


def test_xapian_index_relative_path():
    """In order to specify index's relative path use 2 slashes"""

    # two slashes specify relative local path, and lack of host
    url = make_url("xapian:///path/to/x/index")
    assert url.host is None
    assert url.index == "path/to/x/index"  # relative path


def test_xapian_index_absolute_path():
    """In order to specify index's absolute path use 4 slashes"""

    # 4 slashes
    url = make_url("xapian:////path/to/x/index")

    # index is specified locally via absolute path, thus host is None
    assert url.host is None

    # index's absolute path
    assert url.index == "/path/to/x/index"
