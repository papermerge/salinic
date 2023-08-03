import pytest
from typing_extensions import Annotated

from salinic import IdField, Schema, TextField


class SimpleIndexWithoutPrimaryKey(Schema):
    id: Annotated[str, IdField()]
    title: Annotated[str, TextField()]
    text: Annotated[str, TextField()]


class Index(Schema):
    id: Annotated[str, IdField(primary_key=True)]
    text: Annotated[str, TextField()]


def test_simple_index_instance():
    # SimpleIndex is pydantic model
    doc = SimpleIndexWithoutPrimaryKey(
        id='one',
        title='my title',
        text='some text'
    )

    actual = doc.model_dump()
    expected = {'id': 'one', 'title': 'my title', 'text': 'some text'}

    assert actual == expected


def test_index_should_feature_primary_key():
    """If index does not feature IdField(primary_key=Trye)
    an error will be raised when accessing pk attribute
    """
    doc = SimpleIndexWithoutPrimaryKey(
        id='one',
        title='my title',
        text='some text'
    )

    with pytest.raises(ValueError):
        _ = doc.pk  # there is no primary key


def test_pk_property():
    doc = Index(id='one', text='some text')
    assert doc.pk == 'one'


def test_pk_name_property():
    doc = Index(id='one', text='some text')
    assert doc.pk_name == 'id'
