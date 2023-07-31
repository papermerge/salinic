from salinic import IdField, Schema, Search, Session, TextField


class SimpleIndex(Schema):
    id: str = IdField(primary_key=True)
    title: str = TextField()
    text: str = TextField()


def test_simple_search(session: Session):
    doc = SimpleIndex(id='one', title='My Document.pdf', text='some text')
    session.add(doc)

    sq1 = Search(SimpleIndex).query('document')

    results = session.exec(sq1)

    assert len(results) == 1
    assert isinstance(results[0], SimpleIndex)
    assert results[0].title == 'My Document.pdf'

    sq2 = Search(SimpleIndex).query('Bills')

    results = session.exec(sq2)

    assert len(results) == 0
