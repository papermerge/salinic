[![Tests](https://github.com/papermerge/salinic/actions/workflows/tests.yml/badge.svg)](https://github.com/papermerge/salinic/actions/workflows/tests.yml)

# Salinic

Salinic - provides modular search. It features a unified API that
allows you to plug in different search backends.
Currently, it supports Xapian and Solr backends.


## Usage

Declare your search schema:

    from typing import Optional
    from typing_extensions import Annotated

    from salinic.field import IdField, KeywordField, TextField
    from salinic.schema import Schema


    class MyModel(Schema):
        """Index schema"""
        id: Annotated[str, IdField(primary_key=True)]
        user_id: str
        parent_id: str
        title: Annotated[str, TextField()]
        text: Annotated[Optional[str], TextField()] = None
        tags: Annotated[Optional[list[str]], KeywordField()] = []


Index your documents:

        from salinic import IndexRW, create_engine

        engine = create_engine("xapian:////search_index")
        index = IndexRW(engine, schema=MyModel)

        for document in all_your_documents():
            model = MyModel(
                id=str(document.id),
                user_id=str(document.user_id),
                parent_id=document.parent_id,
                title=document.title,
                text=document.text,
                tags=document.tags
            )
            index.add(model)


Search your documents:

        from salinic import IndexRO, create_engine

        engine = create_engine("xapian:////search_index")
        index = IndexRO(engine, schema=MyModel)

        sq = Search(MyModel).query(" your query string ")

        for found in index.search(sq):
            print(found)  # found is instance of MyModel


The only modification of your for changing to different search
engine backend, is the first argument of the `create_engine` method e.g. from
"xapian:////search_index" to "solr://localhost:8983/my-index-name".
