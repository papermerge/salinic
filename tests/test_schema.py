from salinic import IdField, Schema, TextField


class SimpleIndex(Schema):
    id: str = IdField()
    title: str = TextField()
    text: str = TextField()


def test_simple_index_instance():
    # SimpleIndex is pydantic model
    doc = SimpleIndex(id='one', title='my title', text='some text')

    actual = doc.model_dump()
    expected = {'id': 'one', 'title': 'my title', 'text': 'some text'}

    assert actual == expected
