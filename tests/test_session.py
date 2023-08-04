import pytest

from salinic import Schema, Session, types


class SimpleIndex(Schema):
    id: types.IdStrPrimary
    title: types.Text
    text: types.Text


def test_add_simple_index_instance_to_session(session: Session):
    # Models added to the session must have exactly one IdField
    # with primary_key=True
    doc = SimpleIndex(id='one', title='my title', text='some text')
    session.add(doc)

    assert session


class IndexWithoutPrimaryKey(Schema):
    id: types.IdStr
    title: types.Text
    text: types.Text


def test_insert_into_index_entity_without_primary_key(session: Session):
    """Index schema should feature IdField with primary_key=True"""
    doc = IndexWithoutPrimaryKey(id='one', title='my title', text='some text')

    with pytest.raises(ValueError):
        # doc does not contain IdField with primary_key=True
        session.add(doc)
