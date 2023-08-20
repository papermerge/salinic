from operator import itemgetter
from typing import Optional

import pytest
from typing_extensions import Annotated

from salinic import IdField, IndexRW, TextField, UUIDField, create_engine
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


class Model_1(Schema):
    id: Annotated[str, IdField(primary_key=True)]   # noqa
    title: Annotated[
        str,
        TextField(multi_lang=True, general_search=True)  # noqa
    ]
    text: Annotated[
        str,
        TextField(multi_lang=True, general_search=True)  # noqa
    ]


@pytest.mark.parametrize('solr_index', [Model_1], indirect=True)
def test_index_copy_fields_dump_1(solr_index):
    actual = solr_index.index_schema_dump()

    expected = {
        'add-field': [],
        'add-copy-field': [
            {
              "source": "title_*",
              "dest": ["_text_"]
            },
            {
              "source": "text_*",
              "dest": ["_text_"]
            },
            {
              "source": "id",
              "dest": ["_text_"]
            }
        ]
    }

    assert actual['add-field'] == []

    actual_add_field = sorted(actual['add-field'], key=itemgetter('source'))
    exp_add_field = sorted(expected['add-field'], key=itemgetter('source'))

    assert actual_add_field == exp_add_field


class Model_2(Schema):
    id: Annotated[str, IdField(primary_key=True)]   # noqa
    document_id: Annotated[
        Optional[str],
        UUIDField(index=False, general_search=True)  # noqa
    ]


@pytest.mark.parametrize('solr_index', [Model_2], indirect=True)
def test_index_copy_fields_dump_2(solr_index):
    actual = solr_index.index_schema_dump()

    expected = {
        'add-field': [{
            'name': 'document_id',
            'type': 'text_general',
            'multiValued': False,
            'indexed': False,
            'stored': True
        }],
        'add-copy-field': [
            {
                "source": "id",
                "dest": ["_text_"]
            },
            {
                "source": "document_id",
                "dest": ["_text_"]
            }
        ]
    }

    assert actual['add-field'] == expected['add-field']
    assert sort_by(
        actual['add-copy-field'], 'source'
    ) == sort_by(
        expected['add-copy-field'], 'source'
    )


class Model_3(Schema):
    id: Annotated[str, IdField(primary_key=True)]   # noqa
    user_id: Annotated[
        Optional[str],
        UUIDField(index=False)  # noqa
    ]


@pytest.mark.parametrize('solr_index', [Model_3], indirect=True)
def test_index_copy_fields_dump_3(solr_index):
    actual = solr_index.index_schema_dump()

    expected = {
        'add-field': [{
            'name': 'user_id',
            'type': 'text_general',
            'multiValued': False,
            'indexed': False,
            'stored': True
        }],
        'add-copy-field': [
            {
                "source": "id",
                "dest": ["_text_"]
            }
        ]
    }

    assert actual['add-field'] == expected['add-field']
    assert sort_by(
        actual['add-copy-field'], 'source'
    ) == sort_by(
        expected['add-copy-field'], 'source'
    )


def sort_by(list_of_dicts, field):
    return sorted(list_of_dicts, key=itemgetter(field))
