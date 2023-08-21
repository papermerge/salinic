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


@pytest.mark.parametrize('schema_manager', [Model_1], indirect=True)
def test_index_copy_fields_dump_1(schema_manager):
    actual = schema_manager.create_dict_dump()

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


@pytest.mark.parametrize('schema_manager', [Model_2], indirect=True)
def test_index_copy_fields_dump_2(schema_manager):
    actual = schema_manager.create_dict_dump()

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


@pytest.mark.parametrize('schema_manager', [Model_2], indirect=True)
def test_schema_manager_apply_dict_dump_1(schema_manager, requests_mock):

    requests_mock.get(
        'http://localhost:8983/solr/index/schema/fields/document_id',
        status_code=200
    )

    actual = schema_manager.apply_dict_dump()

    expected = {
        'replace-field': [{
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

    assert actual['replace-field'] == expected['replace-field']
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


@pytest.mark.parametrize('schema_manager', [Model_3], indirect=True)
def test_index_copy_fields_dump_3(schema_manager):
    actual = schema_manager.create_dict_dump()

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


@pytest.mark.parametrize('schema_manager', [Model_4], indirect=True)
def test_index_copy_fields_dump_4(schema_manager):
    actual = schema_manager.create_dict_dump()

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


@pytest.mark.parametrize('schema_manager', [Model_5], indirect=True)
def test_index_copy_fields_dump_5(schema_manager):
    actual = schema_manager.create_dict_dump()

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


@pytest.mark.parametrize('schema_manager', [Model_5], indirect=True)
def test_schema_management_apply_dict_dump_5(schema_manager, requests_mock):
    # `page_number` field exists in solr schema, thus it is expected to be part
    # of 'replace-field'
    requests_mock.get(
        'http://localhost:8983/solr/index/schema/fields/page_number',
        status_code=200  # field exists in solr schema
    )
    # `page_count` field does NOT exist in solr schema, thus it is expected to
    # be part of the 'add-field'
    requests_mock.get(
        'http://localhost:8983/solr/index/schema/fields/page_count',
        status_code=404  # field does NOT exist in solr schema
    )

    actual = schema_manager.apply_dict_dump()

    expected = {
        # fields which are already part of the solr schema
        'replace-field': [{
            'name': 'page_number',
            'type': 'pint',
            'indexed': True,
            'multiValued': False,
            'stored': True
        }],
        # fields which are not yet part of the solr schema
        'add-field': [{
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

    assert len(actual['add-field']) == 1
    assert len(actual['replace-field']) == 1
    assert len(actual['add-copy-field']) == 1
    assert actual['add-field'][0] == expected['add-field'][0]
    assert actual['replace-field'][0] == expected['replace-field'][0]
    assert actual['add-copy-field'][0] == expected['add-copy-field'][0]


def sort_by(list_of_dicts, field):
    return sorted(list_of_dicts, key=itemgetter(field))
