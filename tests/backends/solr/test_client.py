import pytest
from typing_extensions import Annotated

from salinic import IdField, TextField
from salinic.backends.solr.client import ClientRW
from salinic.schema import Schema
from salinic.url import make_url


@pytest.mark.parametrize(
    "input_url, expected_url",
    [("solr://localhost:8983/index_papermerge",
      "http://localhost:8983/solr/index_papermerge/update/json/docs"),
     ("solr://localhost:6666/my-index",
      "http://localhost:6666/solr/my-index/update/json/docs"),
     ("solrs://localhost:8443/momo",
      "https://localhost:8443/solr/momo/update/json/docs")]
)
def test_client_url(input_url, expected_url):
    url = make_url(input_url)
    client = ClientRW(url)

    assert client.http_url == expected_url


class Model(Schema):
    id: Annotated[str, IdField(primary_key=True)]   # noqa
    title: Annotated[str, TextField()]  # noqa
    text: Annotated[str, TextField()]  # noqa


def test_add_model(requests_mock):
    client = ClientRW(make_url("solr://localhost:8983/index"))

    # it is expected that solr will receive following post request
    mock = requests_mock.post(
        'http://localhost:8983/solr/index/update/json/docs',
        json={}  # irrelevant for this test
    )

    model = Model(id='one', title='My Documents', text='Some content')

    # send http request to solr
    client.add(model)  # this is what is tested here

    # let's check now what actually was sent
    expected = {
        'add': {
            'doc': {
                'id': 'one',
                'title': 'My Documents',
                'text': 'Some content'
            }
        }
    }

    assert expected == mock.request_history[0].json()


def test_remove_model_by_field_id(requests_mock):
    client = ClientRW(make_url("solr://localhost:8983/index"))

    # it is expected that solr will receive following post request
    mock = requests_mock.post(
        'http://localhost:8983/solr/index/update/json/docs',
        json={}  # irrelevant for this test
    )

    # send http request to solr
    client.remove(id='one')  # this is what is tested here

    # let's check now what actually was sent
    expected = {
        'delete': {
            'id': 'one'
        }
    }

    assert expected == mock.request_history[0].json()


def test_remove_model_by_field_document_id(requests_mock):
    client = ClientRW(make_url("solr://localhost:8983/index"))

    # it is expected that solr will receive following post request
    mock = requests_mock.post(
        'http://localhost:8983/solr/index/update/json/docs',
        json={}  # irrelevant for this test
    )

    # send http request to solr
    client.remove(document_id='abc-xyz-1')  # this is what is tested here

    # let's check now what actually was sent
    expected = {
        'delete': {
            'document_id': 'abc-xyz-1'
        }
    }

    assert expected == mock.request_history[0].json()
