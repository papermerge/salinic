from typing_extensions import Annotated

from salinic import IdField, IndexRW, TextField, create_engine
from salinic.schema import Schema


class Model(Schema):
    id: Annotated[str, IdField(primary_key=True)]   # noqa
    title: Annotated[str, TextField()]  # noqa
    text: Annotated[str, TextField()]  # noqa


def test_index_add(requests_mock):
    engine = create_engine("solr://localhost:8983/index")
    index = IndexRW(engine, schema=Model)
    model = Model(id='one', title='my title', text='my text')

    # it is expected that solr will receive following post request
    mock = requests_mock.post(
        'http://localhost:8983/solr/index/update/json/docs',
        json={}  # irrelevant for this test
    )

    index.add(model)  # this is what is tested here

    # let's check now what actually was sent
    expected = {
        'add': {
            'doc': {
                'id': 'one',
                'title': 'my title',
                'text': 'my text'
            }
        }
    }

    assert expected == mock.request_history[0].json()
