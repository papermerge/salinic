from typing import List, Optional

import pytest
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


def test_basic_index_add_and_search(session: Session):
    """basic add and search of model with list of keywords field"""
    folder_entity = Index(
        id='one',
        title='Bills.pdf',
        breadcrumb=["home", "My Documents", "Bills.pdf"],
        tags=[]
    )

    session.add(folder_entity)

    # now we are searching my exact keyword from breadcrumb field
    sq = Search(Index).query('breadcrumb:My Documents')
    found: List[Index] = session.exec(sq)

    assert len(found) == 1
    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "My Documents", "Bills.pdf"]


@pytest.mark.skip()
def test_search_by_keyword_and_free_text(session: Session):
    folder_1 = Index(
        id='one',
        title='Bills.pdf',
        breadcrumb=["home", "My Documents", "Bills.pdf"],
        tags=[]
    )

    session.add(folder_1)

    folder_2 = Index(
        id='two',
        title='Bills.pdf',
        breadcrumb=["home", "Invoices", "Bills.pdf"],
        tags=[]
    )

    session.add(folder_2)

    # should retrieve folder from home/My Documents
    sq = Search(Index).query('Bills.pdf breadcrumb:My Documents')
    found: List[Index] = session.exec(sq)

    assert len(found) == 1
    assert found[0].title == 'Bills.pdf'
    assert found[0].breadcrumb == ["home", "My Documents", "Bills.pdf"]
