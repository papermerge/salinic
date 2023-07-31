from salinic import IdField, Schema, Session, TextField


class SimpleIndex(Schema):
    id: str = IdField(primary_key=True)
    title: str = TextField()
    text: str = TextField()


def test_add_simple_index_instance_to_session(session: Session):
    # Models added to the session must have exactly one IdField
    # with primary_key=True
    doc = SimpleIndex(id='one', title='my title', text='some text')
    session.add(doc)

    assert session
