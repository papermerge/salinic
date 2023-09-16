import pytest

from salinic import IndexRW, Schema, Search, types


class SimpleModel(Schema):
    id: types.IdStrPrimary
    user_id: types.IdStr
    title: types.Text
    text: types.Text


@pytest.mark.parametrize('index', [SimpleModel], indirect=True)
def test_remove_entity_by_primary_field(index: IndexRW):
    """In order to remove document from the index
    provide field name (ID) and its value"""
    doc = SimpleModel(
        id='one',
        user_id='user_1',
        title='my title',
        text='some text'
    )
    index.add(doc)

    sq_1 = Search(SimpleModel).query(
        'some text'
    )

    results_1 = index.search(sq_1)

    assert len(results_1) == 1

    # document is removed from index by ID
    index.remove(id="one")

    sq_2 = Search(SimpleModel).query(
        'some text'
    )

    results_2 = index.search(sq_2)
    assert len(results_2) == 0


@pytest.mark.parametrize('index', [SimpleModel], indirect=True)
def test_remove_entity_by_user_id_field(index: IndexRW):
    """In order to remove document from the index
    provide field name (USER_ID) and its value"""
    doc = SimpleModel(
        id='one',
        title='my title',
        text='some text',
        user_id='user_1'
    )
    index.add(doc)

    sq_1 = Search(SimpleModel).query(
        'some text'
    )

    results_1 = index.search(sq_1)

    assert len(results_1) == 1

    # document is removed from the index by USER_ID
    index.remove(user_id="user_1")

    sq_2 = Search(SimpleModel).query(
        'some text'
    )

    results_2 = index.search(sq_2)
    assert len(results_2) == 0
