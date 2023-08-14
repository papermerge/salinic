
from salinic import Schema, Search, Session, types


class SimpleIndex(Schema):
    id: types.IdStrPrimary
    user_id: types.IdStr
    title: types.Text
    text: types.Text


def test_remove_entity_by_primary_field(session: Session):
    """In order to remove document from the index
    provide field name (ID) and its value"""
    doc = SimpleIndex(
        id='one',
        user_id='user_1',
        title='my title',
        text='some text'
    )
    session.add(doc)

    sq_1 = Search(SimpleIndex).query(
        'some text'
    )

    results_1 = session.exec(sq_1)

    assert len(results_1) == 1

    # document is removed from index by ID
    session.remove("IDone")

    sq_2 = Search(SimpleIndex).query(
        'some text'
    )

    results_2 = session.exec(sq_2)
    assert len(results_2) == 0


def test_remove_entity_by_user_id_field(session: Session):
    """In order to remove document from the index
    provide field name (USER_ID) and its value"""
    doc = SimpleIndex(
        id='one',
        title='my title',
        text='some text',
        user_id='user_1'
    )
    session.add(doc)

    sq_1 = Search(SimpleIndex).query(
        'some text'
    )

    results_1 = session.exec(sq_1)

    assert len(results_1) == 1

    # document is removed from the index by USER_ID
    session.remove("USER_IDuser_1")

    sq_2 = Search(SimpleIndex).query(
        'some text'
    )

    results_2 = session.exec(sq_2)
    assert len(results_2) == 0
