
import pytest
from typing_extensions import Annotated

from salinic import IdField, Schema, Session, TextField


class SimpleIndex(Schema):
    id: Annotated[str, IdField(primary_key=True)]
    title: Annotated[str, TextField()]
    text: Annotated[str, TextField()]


def test_add_simple_index_instance_to_session(session: Session):
    # Models added to the session must have exactly one IdField
    # with primary_key=True
    doc = SimpleIndex(id='one', title='my title', text='some text')
    session.add(doc)

    assert session


class IndexWithoutPrimaryKey(Schema):
    id: Annotated[str, IdField()]
    title: Annotated[str, TextField()]
    text: Annotated[str, TextField()]


def test_insert_into_index_entity_without_primary_key(session: Session):
    """Index schema should feature IdField with primary_key=True"""
    doc = IndexWithoutPrimaryKey(id='one', title='my title', text='some text')

    with pytest.raises(ValueError):
        # doc does not contain IdField with primary_key=True
        session.add(doc)
