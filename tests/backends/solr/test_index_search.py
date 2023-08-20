from typing_extensions import Annotated

from salinic import IdField, IndexRO, Search, TextField, create_engine
from salinic.schema import Schema


class Model_1(Schema):
    id: Annotated[str, IdField(primary_key=True)]   # noqa
    title: Annotated[
        str,
        TextField(multi_lang=True, general_search=True)  # noqa
    ]


def test_index_search(requests_mock):

    engine = create_engine("solr://localhost:8983/index")
    index = IndexRO(engine, schema=Model_1)

    sq = Search(Model_1).query('my document')

    json_response = {
        "responseHeader": {
            "status": 0,
            "QTime": 41,
            "params": {
                "q": "*"
            }
        },
        "response": {
            "numFound": 7,
            "start": 0,
            "numFoundExact": True,
            "docs": [
                {
                    "id": "one",
                    "title_txt_en": "My Documents",
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

    expected = [
        Model_1(id='one', title='My Documents')
    ]

    assert results == expected
