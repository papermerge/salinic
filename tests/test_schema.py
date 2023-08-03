from typing_extensions import Annotated

from salinic import IdField, Schema, TextField


class SimpleIndex(Schema):
    id: Annotated[str, IdField()]
    title: Annotated[str, TextField()]
    text: Annotated[str, TextField()]


def test_simple_index_instance():
    # SimpleIndex is pydantic model
    doc = SimpleIndex(id='one', title='my title', text='some text')

    actual = doc.model_dump()
    expected = {'id': 'one', 'title': 'my title', 'text': 'some text'}

    assert actual == expected
