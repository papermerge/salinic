from typing import List, Optional

from typing_extensions import Annotated

from salinic import IdField, KeywordField, Schema, Search, Session, types


class Index(Schema):
    id: Annotated[str, IdField(primary_key=True)]  # page id | node_id
    title: types.Text  # document or folder title
    breadcrumb: Annotated[List[str], KeywordField()]  # mandatory keywords
    tags: Annotated[Optional[List[str]], KeywordField()]  # optional keywords


def test_basic_index_add_and_read(session: Session):
    """basic insert/serialization of model with list of keywords field"""
    folder_entity = Index(
        id='one',
        title='Bills.pdf',
        breadcrumb=["home", "My Documents", "Bills.pdf"],
        tags=[]
    )

    session.add(folder_entity)

    sq = Search(Index).query('Bills.pdf')
    found: List[Index] = session.exec(sq)

    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "My Documents", "Bills.pdf"]


def test_xsearch_keywords(session: Session):
    """basic add and search of model with list of keywords field"""
    folder_entity = Index(
        id='one',
        title='Bills.pdf',
        breadcrumb=["home", "Payments", "Bills.pdf"],
        tags=[]
    )

    session.add(folder_entity)

    # now we are searching my exact keyword from breadcrumb field
    sq = Search(Index).query('bills breadcrumb:payments')
    found: List[Index] = session.exec(sq)

    assert len(found) == 1
    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "Payments", "Bills.pdf"]


def test_search_by_keyword_and_free_text(session: Session):
    folder_1 = Index(
        id='one',
        title='Bills.pdf',
        breadcrumb=["home", "Payments", "Bills.pdf"],
        tags=["important"]
    )

    session.add(folder_1)

    folder_2 = Index(
        id='two',
        title='Bills.pdf',
        breadcrumb=[],
        tags=[]
    )

    session.add(folder_2)

    # should retrieve folder from home/Documents
    sq = Search(Index).query("bills breadcrumb:payments")
    found: List[Index] = session.exec(sq)

    assert len(found) == 1
    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "Payments", "Bills.pdf"]

    # filter by tag
    sq = Search(Index).query('bills tags:important')
    found: List[Index] = session.exec(sq)
    assert len(found) == 1
    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "Payments", "Bills.pdf"]
    assert found[0].tags == ['important']


def test_search_only_by_tags_single_tag(session: Session):
    """There 3 documents. Only two documents have assigned tag 'important'.
    When user searches only by tag i.e. filters documents by tag:

        user query -> tags:important

    only the documents with that tag are returned"""
    node_1 = Index(
        id='one',
        title='one.pdf',
        breadcrumb=["home", "folder_1", "one.pdf"],
        tags=["important"]
    )
    session.add(node_1)

    node_2 = Index(
        id='two',
        title='two.pdf',
        breadcrumb=["home", "folder_2", "two.pdf"],
        tags=["important"]
    )

    session.add(node_2)

    node_3 = Index(
        id='free',
        title='free.pdf',
        breadcrumb=["home", "folder_3", "free.pdf"],
        tags=[]
    )

    session.add(node_3)

    sq = Search(Index).query("tags:important")
    found: List[Index] = session.exec(sq)

    assert len(found) == 2
    assert {'one.pdf', 'two.pdf'} == {node.title for node in found}


def test_search_only_by_tags_multiple_tags(session: Session):
    """There are 3 documents:

    * (1) with one tag `important`
    * (2) with two tags `important` and `paid`
    * (3) without tags

    Search query "tags:important,paid" will return only document 2.
    """
    node_1 = Index(
        id='one',
        title='one.pdf',
        breadcrumb=["home", "folder_1", "one.pdf"],
        tags=["important"]
    )
    session.add(node_1)

    folder_2 = Index(
        id='two',
        title='two.pdf',
        breadcrumb=["home", "folder_2", "two.pdf"],
        tags=["important", "paid"]
    )

    session.add(folder_2)

    folder_3 = Index(
        id='free',
        title='free.pdf',
        breadcrumb=["home", "folder_3", "free.pdf"],
        tags=[]
    )

    session.add(folder_3)

    sq = Search(Index).query("tags:important,paid")
    found: List[Index] = session.exec(sq)

    assert len(found) == 1
