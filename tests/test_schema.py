import pytest

from salinic import Schema, types


class SimpleIndexWithoutPrimaryKey(Schema):
    id: types.IdStr
    title: types.Text
    text: types.Text


class Index(Schema):
    id: types.IdStrPrimary
    text: types.Text


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
    """Primary key field i.e. doc.pk is the field which
    was defined with IdField(primary_key=True) annotation"""
    doc = Index(id='one', text='some text')
    assert doc.pk == 'one'


def test_pk_name_property():
    doc = Index(id='one', text='some text')
    assert doc.pk_name == 'id'
