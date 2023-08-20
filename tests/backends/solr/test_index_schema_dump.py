from operator import itemgetter
from typing import Optional, Tuple

import pytest
from typing_extensions import Annotated

from salinic import IdField, KeywordField, TextField, UUIDField, types
from salinic.schema import Schema


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


class Model_4(Schema):
    id: Annotated[str, UUIDField(primary_key=True)]   # noqa
    tags: Annotated[
        Optional[Tuple[str, str]],
        KeywordField(multi_value=True)  # noqa
    ]


@pytest.mark.parametrize('solr_index', [Model_4], indirect=True)
def test_index_copy_fields_dump_4(solr_index):
    actual = solr_index.index_schema_dump()

    expected = {
        'add-field': [{
            'name': 'tags',
            'type': 'text_general',
            'multiValued': True,
            'indexed': True,
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


class Model_5(Schema):
    id: Annotated[str, UUIDField(primary_key=True)]   # noqa
    page_number: types.OptionalNumeric = None
    page_count: types.OptionalNumeric = None


@pytest.mark.parametrize('solr_index', [Model_5], indirect=True)
def test_index_copy_fields_dump_5(solr_index):
    actual = solr_index.index_schema_dump()

    expected = {
        'add-field': [{
            'name': 'page_number',
            'type': 'pint',
            'indexed': True,
            'multiValued': False,
            'stored': True
        }, {
            'name': 'page_count',
            'type': 'pint',
            'indexed': True,
            'multiValued': False,
            'stored': True
        }],
        'add-copy-field': [
            {
                "source": "id",
                "dest": ["_text_"]
            }
        ]
    }

    assert sort_by(
        actual['add-field'],
        'name'
    ) == sort_by(
        expected['add-field'],
        'name'
    )
    assert sort_by(
        actual['add-copy-field'], 'source'
    ) == sort_by(
        expected['add-copy-field'], 'source'
    )


def sort_by(list_of_dicts, field):
    return sorted(list_of_dicts, key=itemgetter(field))
