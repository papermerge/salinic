import pytest

from salinic.query import (FilterQuery, FreeTextQuery, extract_filters,
                           extract_free_text, first_filter_beg_pos,
                           first_filter_end_pos, first_filter_pos)


@pytest.mark.parametrize(
    "the_input, beg_pos",
    [("tags:one", 0),
     (" tags:one", 1),
     ("some free text tags:one", 15),
     ("  tags:one", 2),
     ("tags:'one'", 0)]
)
def test_first_filter_beg_pos(the_input, beg_pos):
    assert beg_pos == first_filter_beg_pos(the_input)


@pytest.mark.parametrize(
    "the_input, end_pos",
    [("tags:one", 7),
     (" tags:one", 8),
     ("some free text tags:one", 22),
     ("  tags:one", 9),
     ("tags:'one'", 8),
     ("tags:one,two", 11),
     ("tags:one, two", 12)]  # tag list includes one space
)
def test_first_filter_end_pos(the_input, end_pos):
    assert end_pos == first_filter_end_pos(the_input)


@pytest.mark.parametrize(
    "the_input, beg_pos, end_pos",
    [("my tags:imp", 3, 10),
     ("tags:imp", 0, 7),
     ("some tags:imp text", 5, 12),
     ("a tags:'my imp'", 2, 13)]
)
def test_first_filter_pos(the_input, beg_pos, end_pos):
    assert (beg_pos, end_pos) == first_filter_pos(the_input)


@pytest.mark.parametrize(
    "the_input,expected_output",
    [("free text", "free text"),
     ("breadcrumb:bills", None),
     ("Some document tags:important", "Some document"),
     ("bills   tags:important", "bills"),
     ("tags:important bills", "bills"),
     ("invoice.pdf breadcrumb:'My Documents'", "invoice.pdf"),
     ("breadcrumb:'My Documents' free text search ", "free text search"),
     ('breadcrumb:"My Documents" free text search ', "free text search")]
)
def test_extract_tree_text(the_input, expected_output):
    actual_output = extract_free_text(the_input)

    assert actual_output == expected_output


def test_extract_free_text_with_quotes():
    expected_output = "free text"
    actual_output = extract_free_text('some:"text one" free text')
    assert expected_output == actual_output


@pytest.mark.parametrize(
    "the_input,expected_output",
    [("free text", None),
     ("Some document tags:important", "tags:important"),
     ("bills   tags:important", "tags:important"),
     ("tags:important bills", "tags:important"),
     ("invoice.pdf breadcrumb:My Documents", "breadcrumb:My Documents"),
     ("breadcrumb:'My Documents' free text search ", "breadrumb:My Documents"),
     ('breadcrumb:"My Documents" free text search ', "breadcrumb:My Documents")]
)
def test_extract_filters(the_input, expected_output):
    actual_output = extract_filters(the_input)

    assert actual_output == expected_output


@pytest.mark.parametrize(
    "the_input, expected_name, expected_values",
    [("breadcrumb:bills", "breadcrumb", ["bills"]),
     ("breadcrumb:home,bills", "breadcrumb", ["home", "bills"]),
     ("tags:important,paid", "tags", ["important", "paid"])]
)
def test_query_filter(the_input, expected_name, expected_values):
    fq = FilterQuery(the_input)

    assert fq.name == expected_name
    assert fq.values == expected_values


def test_free_text_query():
    ftq = FreeTextQuery("some free text")
    assert str(ftq) == 'some free text'
