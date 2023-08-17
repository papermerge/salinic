from typing import List, Optional

import pytest
from typing_extensions import Annotated

from salinic import IdField, IndexRW, KeywordField, Schema, Search, types


class Model(Schema):
    id: Annotated[str, IdField(primary_key=True)]  # page id | node_id
    title: types.Text  # document or folder title
    breadcrumb: Annotated[List[str], KeywordField()]  # mandatory keywords
    tags: Annotated[Optional[List[str]], KeywordField()]  # optional keywords


@pytest.mark.parametrize('index', [Model], indirect=True)
def test_basic_index_add_and_read(index: IndexRW):
    """basic insert/serialization of model with list of keywords field"""
    folder_entity = Model(
        id='one',
        title='Bills.pdf',
        breadcrumb=["home", "My Documents", "Bills.pdf"],
        tags=[]
    )

    index.add(folder_entity)

    sq = Search(Model).query('Bills.pdf')
    found: List[Model] = index.search(sq)

    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "My Documents", "Bills.pdf"]


@pytest.mark.parametrize('index', [Model], indirect=True)
def test_xsearch_keywords(index: IndexRW):
    """basic add and search of model with list of keywords field"""
    folder_entity = Model(
        id='one',
        title='Bills.pdf',
        breadcrumb=["home", "Payments", "Bills.pdf"],
        tags=[]
    )

    index.add(folder_entity)

    # now we are searching my exact keyword from breadcrumb field
    sq = Search(Model).query('bills breadcrumb:payments')
    found: List[Model] = index.search(sq)

    assert len(found) == 1
    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "Payments", "Bills.pdf"]


@pytest.mark.parametrize('index', [Model], indirect=True)
def test_search_by_keyword_and_free_text(index: IndexRW):
    folder_1 = Model(
        id='one',
        title='Bills.pdf',
        breadcrumb=["home", "Payments", "Bills.pdf"],
        tags=["important"]
    )

    index.add(folder_1)

    folder_2 = Model(
        id='two',
        title='Bills.pdf',
        breadcrumb=[],
        tags=[]
    )

    index.add(folder_2)

    # should retrieve folder from home/Documents
    sq = Search(Model).query("bills breadcrumb:payments")
    found: List[Model] = index.search(sq)

    assert len(found) == 1
    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "Payments", "Bills.pdf"]

    # filter by tag
    sq = Search(Model).query('bills tags:important')
    found: List[Model] = index.search(sq)
    assert len(found) == 1
    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "Payments", "Bills.pdf"]
    assert found[0].tags == ['important']


@pytest.mark.parametrize('index', [Model], indirect=True)
def test_search_only_by_tags_single_tag(index: IndexRW):
    """There 3 documents. Only two documents have assigned tag 'important'.
    When user searches only by tag i.e. filters documents by tag:

        user query -> tags:important

    only the documents with that tag are returned"""
    node_1 = Model(
        id='one',
        title='one.pdf',
        breadcrumb=["home", "folder_1", "one.pdf"],
        tags=["important"]
    )
    index.add(node_1)

    node_2 = Model(
        id='two',
        title='two.pdf',
        breadcrumb=["home", "folder_2", "two.pdf"],
        tags=["important"]
    )

    index.add(node_2)

    node_3 = Model(
        id='free',
        title='free.pdf',
        breadcrumb=["home", "folder_3", "free.pdf"],
        tags=[]
    )

    index.add(node_3)

    sq = Search(Model).query("tags:important")
    found: List[Model] = index.search(sq)

    assert len(found) == 2
    assert {'one.pdf', 'two.pdf'} == {node.title for node in found}


@pytest.mark.parametrize('index', [Model], indirect=True)
def test_search_only_by_tags_multiple_tags(index: IndexRW):
    """There are 3 documents:

    * (1) with one tag: `important`
    * (2) with two tags: `important` and `paid`
    * (3) without tags

    Search query "tags:important,paid" will return only document 2.
    """
    node_1 = Model(
        id='one',
        title='one.pdf',
        breadcrumb=["home", "folder_1", "one.pdf"],
        tags=["important"]
    )
    index.add(node_1)

    folder_2 = Model(
        id='two',
        title='two.pdf',
        breadcrumb=["home", "folder_2", "two.pdf"],
        tags=["important", "paid"]
    )

    index.add(folder_2)

    folder_3 = Model(
        id='free',
        title='free.pdf',
        breadcrumb=["home", "folder_3", "free.pdf"],
        tags=[]
    )

    index.add(folder_3)

    sq = Search(Model).query("tags:important,paid")
    found: List[Model] = index.search(sq)

    assert len(found) == 1
