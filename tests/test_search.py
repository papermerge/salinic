from typing_extensions import Annotated

from salinic import IdField, Schema, Search, Session, TextField


class SimpleIndex(Schema):
    id: Annotated[str, IdField(primary_key=True)]
    title: Annotated[str, TextField()]
    text: Annotated[str, TextField()]


def test_simple_search(session: Session):
    doc = SimpleIndex(id='one', title='My Document.pdf', text='some text')
    session.add(doc)

    sq1 = Search(SimpleIndex).query('document')

    results = session.exec(sq1)

    assert len(results) == 1
    assert isinstance(results[0], SimpleIndex)
    assert results[0].title == 'My Document.pdf'

    sq2 = Search(SimpleIndex).query('Bills')

    results = session.exec(sq2)

    assert len(results) == 0


class IndexHasFieldsWithoutAnnotation(Schema):
    """This index features fields which are not annotated

    Fields which are not annotated won't be indexed, thus you
    cannot search by those fields.
    """
    id: Annotated[str, IdField(primary_key=True)]
    title: Annotated[str, TextField()]
    text: Annotated[str, TextField()]
    document_id: Annotated[str, IdField()]
    # fields without annotation won't be indexed
    # however, they will be stored in the index
    user_id: str
    parent_id: str


def test_fields_without_annotation_wont_be_indexed(session: Session):
    doc = IndexHasFieldsWithoutAnnotation(
        id='id_one',
        title='My Document.pdf',
        text='some text',
        user_id='user_id_1',
        parent_id='parent_id_1',
        document_id='annotated_doc_id_1'
    )
    session.add(doc)

    sq_1 = Search(IndexHasFieldsWithoutAnnotation).query(
        'parent_id_1'  # value of field which was not indexed
    )

    results_1 = session.exec(sq_1)

    assert len(results_1) == 0

    sq_2 = Search(IndexHasFieldsWithoutAnnotation).query(
        'user_id_1'  # value of field which was not indexed
    )

    results_2 = session.exec(sq_2)

    assert len(results_2) == 0

    # however, we will find document doc if we search by `id` or `document_id`,
    # which are annotated fields of type IdField
    sq_3 = Search(IndexHasFieldsWithoutAnnotation).query(
        'annotated_doc_id_1'  # searching by document_id value
    )

    results_3 = session.exec(sq_3)

    assert len(results_3) == 1
    assert results_3[0].title == 'My Document.pdf'

    # search by ID value
    sq_4 = Search(IndexHasFieldsWithoutAnnotation).query('id_one')

    results_4 = session.exec(sq_4)

    assert len(results_4) == 1
    assert results_4[0].title == 'My Document.pdf'
