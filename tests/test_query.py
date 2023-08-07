import pytest

from salinic.query import (FilterQuery, FreeTextQuery, extract_filters,
                           extract_free_text)


@pytest.mark.parametrize(
    "the_input,expected_output",
    [("free text", "free text"),
     ("breadcrumb:bills", None),
     ("Some document tags:important", "Some document"),
     ("bills   tags:important", "bills"),
     ("tags:important bills", "bills"),
     ("invoice.pdf breadcrumb:My Documents", "invoice.pdf"),
     ("breadcrumb:'My Documents' free text search ", "free text search"),
     ('breadcrumb:"My Documents" free text search ', "free text search")]
)
def test_extract_tree_text(the_input, expected_output):
    actual_output = extract_free_text(the_input)

    assert actual_output == expected_output


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
