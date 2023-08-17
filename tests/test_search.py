import pytest

from salinic import IndexRW, Schema, Search, types


class SimpleModel(Schema):
    id: types.IdStrPrimary
    title: types.Text
    text: types.Text


@pytest.mark.parametrize('index', [SimpleModel], indirect=True)
def test_simple_search(index: IndexRW):
    doc = SimpleModel(id='one', title='My Document.pdf', text='some text')
    index.add(doc)

    sq1 = Search(SimpleModel).query('document')

    results = index.search(sq1)

    assert len(results) == 1
    assert isinstance(results[0], SimpleModel)
    assert results[0].title == 'My Document.pdf'

    sq2 = Search(SimpleModel).query('Bills')

    results = index.search(sq2)

    assert len(results) == 0


@pytest.mark.parametrize('index', [SimpleModel], indirect=True)
def test_adding_document_multiple_times(index: IndexRW):
    """When adding same document multiple times - search results are
    not affected; in other words if same document (i.e. with same ID)
    is added multiple times to the index - it will be inserted in the index only
    once - thus search result will reveal only single instance
    of the document"""
    doc = SimpleModel(id='one', title='My Document.pdf', text='some text')

    # add same document multiple times
    index.add(doc)
    index.add(doc)
    index.add(doc)
    index.add(doc)

    sq1 = Search(SimpleModel).query('document')

    results = index.search(sq1)

    # adding same document multiple times does not affect search results
    # i.e. there only one search result, even though document was
    # added 4 times
    assert len(results) == 1
    assert isinstance(results[0], SimpleModel)
    assert results[0].title == 'My Document.pdf'


@pytest.mark.parametrize('index', [SimpleModel], indirect=True)
def test_remove_document_from_index(index: IndexRW):
    doc = SimpleModel(id='one', title='My Document.pdf', text='some text')
    index.add(doc)

    # (1)
    sq1 = Search(SimpleModel).query('document')

    results = index.search(sq1)

    # confirm that document is part of the index
    assert len(results) == 1

    # remove document from the index
    index.remove("IDone")

    # perform same query as in (1)
    sq2 = Search(SimpleModel).query('document')

    results_2 = index.search(sq2)

    # this time no results as the document was removed from the index
    assert len(results_2) == 0


class ModelHasFieldsWithoutAnnotation(Schema):
    """This index features fields which are not annotated

    Fields which are not annotated won't be indexed, thus you
    cannot search by those fields.
    """
    id: types.IdStrPrimary
    title: types.Text
    text: types.Text
    document_id: types.IdStr
    # fields without annotation won't be indexed
    # however, they will be stored in the index
    user_id: str
    parent_id: str


@pytest.mark.parametrize(
    'index',
    [ModelHasFieldsWithoutAnnotation],
    indirect=True
)
def test_fields_without_annotation_wont_be_indexed(index: IndexRW):
    doc = ModelHasFieldsWithoutAnnotation(
        id='id_one',
        title='My Document.pdf',
        text='some text',
        user_id='user_id_1',
        parent_id='parent_id_1',
        document_id='annotated_doc_id_1'
    )
    index.add(doc)

    sq_1 = Search(ModelHasFieldsWithoutAnnotation).query(
        'parent_id_1'  # value of field which was not indexed
    )

    results_1 = index.search(sq_1)

    assert len(results_1) == 0

    sq_2 = Search(ModelHasFieldsWithoutAnnotation).query(
        'user_id_1'  # value of field which was not indexed
    )

    results_2 = index.search(sq_2)

    assert len(results_2) == 0

    # however, we will find document doc if we search by `id` or `document_id`,
    # which are annotated fields of type IdField
    sq_3 = Search(ModelHasFieldsWithoutAnnotation).query(
        'annotated_doc_id_1'  # searching by document_id value
    )

    results_3 = index.search(sq_3)

    assert len(results_3) == 1
    assert results_3[0].title == 'My Document.pdf'

    # search by ID value
    sq_4 = Search(ModelHasFieldsWithoutAnnotation).query('id_one')

    results_4 = index.search(sq_4)

    assert len(results_4) == 1
    assert results_4[0].title == 'My Document.pdf'


class ModelWithIntPrimaryKey(Schema):
    unique_id: types.IdPrimary
    text: types.Text


@pytest.mark.parametrize(
    'index',
    [ModelHasFieldsWithoutAnnotation],
    indirect=True
)
def test_int_primary_key(index: IndexRW):
    doc = ModelWithIntPrimaryKey(unique_id=1, text='ho ho ho!')
    index.add(doc)
    sq = Search(ModelWithIntPrimaryKey).query('ho ho')

    assert len(index.search(sq)) == 1
