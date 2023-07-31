from salinic.session import Session
from salinic.schema import Schema
from salinic.search import Search
from salinic.field import IdField, TextField


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
    assert results[0].title == 'My Document.pdf'

    sq2 = Search(SimpleIndex).query('Bills')

    results = session.exec(sq2)

    assert len(results) == 0
