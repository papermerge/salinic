import pytest

from salinic import Engine, IndexRW, Schema, types


class SimpleModel(Schema):
    id: types.IdStrPrimary
    title: types.Text
    text: types.Text


def test_add_simple_index_instance_to_session(engine: Engine):
    # Models added to the session must have exactly one IdField
    # with primary_key=True
    index = IndexRW(engine, schema=SimpleModel)
    doc = SimpleModel(id='one', title='my title', text='some text')
    index.add(doc)

    assert index


class ModelWithoutPrimaryKey(Schema):
    id: types.IdStr
    title: types.Text
    text: types.Text


def test_insert_into_index_entity_without_primary_key(engine: Engine):
    """Index schema should feature IdField with primary_key=True"""
    index = IndexRW(engine, schema=ModelWithoutPrimaryKey)
    doc = ModelWithoutPrimaryKey(id='one', title='my title', text='some text')

    with pytest.raises(ValueError):
        # doc does not contain IdField with primary_key=True
        index.add(doc)
