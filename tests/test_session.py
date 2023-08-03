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
