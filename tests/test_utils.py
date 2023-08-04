from salinic.utils import first, get_db_path


def test_first_negative_scenarios():
    assert first([]) is None  # iterable is empty -> None
    # there is no matching element -> None
    assert first(['X', 'Y', None], lambda x: type(x) is int) is None
    assert first(None) is None


def test_first_positive_scenarios():
    def is_int(x):
        return type(x) is int

    iterable = ['one', 2, None]

    # returns first integer number
    assert first(iterable, is_int) == 2


def test_get_db_path():
    assert get_db_path("xapian://index_db") == "index_db"
    assert get_db_path("xapian:///index_db") == "/index_db"
    assert get_db_path("xapian:///some/path/") == "/some/path/"
