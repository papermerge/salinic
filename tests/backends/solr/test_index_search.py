from typing_extensions import Annotated

from salinic import IdField, IndexRO, Search, TextField, create_engine
from salinic.schema import DocumentPage, Folder, Schema


class Index(Schema):
    id: Annotated[str, IdField(primary_key=True)]   # noqa
    title: Annotated[
        str,
        TextField(multi_lang=True, general_search=True)  # noqa
    ]


def test_index_search_result_with_two_folders(requests_mock):

    engine = create_engine("solr://localhost:8983/index")
    index = IndexRO(engine, schema=Index)

    sq = Search(Index).query('my document')

    json_response = {
        "response": {
            "numFound": 1,
            "start": 0,
            "numFoundExact": True,

            "docs": [
                {
                    "id": "0b663599-32b1-4396-8dbe-ae7cd327cec6",  # noqa
                    "lang": "en",
                    "title_txt_en": "My Documents",
                    "entity_type": "folder",
                    "_version_": 1774301885457498112
                },
                {
                    "id": "1c773599-32b1-4396-8dbe-ae7cd327cec6",  # noqa
                    "lang": "en",
                    "title_txt_en": ".inbox",
                    "entity_type": "folder",
                    "_version_": 1774301885457498112
                }
            ]
        }
    }

    requests_mock.get(
        'http://localhost:8983/solr/index/select?q=my+document',
        json=json_response
    )
    results = index.search(sq)

    expected = {
        Folder(
            id='0b663599-32b1-4396-8dbe-ae7cd327cec6',
            title='My Documents',
            lang='en'
        ),
        Folder(
            id='1c773599-32b1-4396-8dbe-ae7cd327cec6',
            title='.inbox',
            lang='en'
        )
    }

    assert set(results) == expected


def test_index_search_result_with_folders_and_documents(requests_mock):
    engine = create_engine("solr://localhost:8983/index")
    index = IndexRO(engine, schema=Index)

    sq = Search(Index).query('my document')

    json_response = {
        "response": {
            "numFound": 1,
            "start": 0,
            "numFoundExact": True,
            "docs": [
                {
                    "id": "0b663599-32b1-4396-8dbe-ae7cd327cec6",
                    "lang": "en",
                    "title_txt_en": "My Documents",
                    "entity_type": "folder",
                    "_version_": 1774301885457498112
                },
                {
                    "id": "1c773599-32b1-4396-8dbe-ae7cd327cec6",
                    "lang": "en",
                    "title_txt_en": ".inbox",
                    "entity_type": "folder",
                    "_version_": 1774301885457498112
                },
                {
                    "id": "a6e4916f-dea6-414b-aa38-f5b9ea375725",
                    "document_id": "9bc57688-302e-4e1f-840a-c747dcccb362",
                    "lang": "en",
                    "user_id": "4cee7c39-7c34-4cc5-8543-42a8c88c9fe6",
                    "page_number": 1,
                    "entity_type": "page",
                    "title_txt_en": "brother_004603.pdf",
                    "_version_": 1801539996374532096
                },
                {
                    "id": "72f6ca9e-af4b-4235-a56c-a62508e24efe",  # noqa
                    "document_id": "9bc57688-302e-4e1f-840a-c747dcccb362",  # noqa
                    "lang": "en",
                    "user_id": "4cee7c39-7c34-4cc5-8543-42a8c88c9fe6",  # noqa
                    "page_number": 2,
                    "entity_type": "page",
                    "title_txt_en": "brother_004603.pdf",
                    "_version_": 1801539996403892224
                }
            ]
        }
    }

    requests_mock.get(
        'http://localhost:8983/solr/index/select?q=my+document',
        json=json_response
    )
    results = index.search(sq)

    expected = {
        Folder(
            id='0b663599-32b1-4396-8dbe-ae7cd327cec6',
            lang='en',
            title='My Documents',
        ),
        Folder(
            id='1c773599-32b1-4396-8dbe-ae7cd327cec6',
            lang='en',
            title='.inbox',
        ),
        DocumentPage(
            id='a6e4916f-dea6-414b-aa38-f5b9ea375725',
            lang='en',
            document_id='9bc57688-302e-4e1f-840a-c747dcccb362',
            page_number=1,
            title='brother_004603.pdf',
            tags=[]
        ),
        DocumentPage(
            id='72f6ca9e-af4b-4235-a56c-a62508e24efe',
            lang='en',
            title='brother_004603.pdf',
            document_id='9bc57688-302e-4e1f-840a-c747dcccb362',
            page_number=2,
            tags=[]
        )
    }
    assert len(results) == len(expected)
    assert set(results) == expected
