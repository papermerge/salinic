# Salinic

Salinic - provides modular search. It features a unified, familiar API that
allows you to plug in different search backends.
Currently it supports only Xapian backend.



## Usage

Declare your search schema:

    from typing import Optional

    from salinic.field import IdField, KeywordField, TextField
    from salinic.schema import Schema


    class IndexEntity(Schema):
        id: str = IdField(primary_key=True)
        user_id: str
        parent_id: str
        title: str = TextField()
        text: Optional[str] = TextField()
        tags: list[str] | None = KeywordField()


Index your documents:

        from salinic import Session, create_engine

        engine = create_engine("xapian:////search_index")
        session = Session(engine)

        for document in all_your_documents():
            entity = IndexEntity(
                id=str(document.id),
                user_id=str(document.user_id),
                parent_id=document.parent_id,
                title=document.title,
                text=document.text,
                tags=document.tags
            )
            session.add(entity)


Search your documents:

        from salinic import Session, create_engine

        engine = create_engine("xapian:////search_index")
        session = Session(engine)

        sq = Search(IndexEntity).query(" your query string ")

        for found in session.exec(sq):
            print(found)  # found is instance of IndexEntity
