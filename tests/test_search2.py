from typing import List, Optional

from typing_extensions import Annotated

from salinic import IdField, Schema, Search, Session, types


class Index(Schema):
    """Index

    Documents are indexed by page. Note that we place in same index
    both folders and documents, and because the main index entity is page -
    we end up having in index two types of entities: folders and pages.
    """
    id: Annotated[str, IdField(primary_key=True)]  # page id | node_id
    # document ID to whom this page belongs
    document_id: Annotated[Optional[str], IdField()] = None
    # ID of the document version
    document_version_id: Annotated[Optional[str], IdField()] = None
    user_id: str
    # for page this is parent_id of the document to whom the page belongs to
    parent_id: str
    title: types.Text  # document or folder title
    text: types.OptionalText = None  # text is None in case folder entity
    entity_type: types.Keyword  # Folder | Page
    tags: types.OptionalKeyword = []
    page_number: types.OptionalNumeric = None  # None in case of folder entity
    page_count: types.OptionalNumeric = None  # None in case of folder entity


def test_basic_index_add_and_search(session: Session):

    folder_entity = Index(
        id='one',
        title='Bills',
        entity_type='folder',
        user_id='user_id_1',
        parent_id='folder_parent_id'
    )

    session.add(folder_entity)

    page_entity = Index(
        id='two',
        title='My Document.pdf',
        document_id='doc_id_1',
        document_version_id='doc_ver_1',
        text='page of the text',
        entity_type='page',
        page_number=1,
        page_count=10,
        user_id='user_id_1',
        parent_id='folder_parent_id'
    )

    session.add(page_entity)

    sq = Search(Index).query('page of')
    found: List[Index] = session.exec(sq)
    assert found[0].entity_type == 'page'
    assert found[0].title == 'My Document.pdf'

    sq = Search(Index).query('bill')
    found: List[Index] = session.exec(sq)
    assert found[0].entity_type == 'folder'
    assert found[0].title == 'Bills'
