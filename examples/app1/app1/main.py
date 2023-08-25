import json
import os
import sys

import typer
from app1.schema import Model

from salinic import IndexRO, IndexRW, SchemaManager, Search, create_engine

app = typer.Typer()

INDEX_URL = os.environ.get('INDEX_URL', None)

if not INDEX_URL:
    print('env var INDEX_URL is empty')
    sys.exit(1)


@app.command()
def index_add(data_path: str):
    """Adds content of the file pointed by data_path to the index"""
    engine = create_engine(INDEX_URL)
    index = IndexRW(engine, schema=Model)

    with open(data_path) as f:
        data = json.load(f)

    for item in data:
        model = Model(**item)
        index.add(model)


@app.command()
def index_delete(docid: str):
    """Deletes document with given docid"""
    engine = create_engine(INDEX_URL)
    index = IndexRW(engine, schema=Model)
    index.remove({"id": docid})


@app.command()
def schema_apply(show: bool = False):
    """Applies defined schema to the index"""
    engine = create_engine(INDEX_URL)
    schema_manager = SchemaManager(engine, model=Model)
    if show:
        print(schema_manager.apply_dict_dump())
    else:
        schema_manager.apply()


@app.command()
def search(querystring: str):
    engine = create_engine(INDEX_URL)
    index = IndexRO(engine, schema=Model)

    sq = Search(Model).query(querystring)

    for entity in index.search(sq):
        print(entity)


@app.command()
def reset(data_path: str):
    """Deletes documents from data_path from the index

    Documents are identified by 'id' field
    """
    engine = create_engine(INDEX_URL)
    index = IndexRW(engine, schema=Model)

    with open(data_path) as f:
        data = json.load(f)

    for item in data:
        model = Model(**item)
        index.remove({"id": model.id})


if __name__ == "__main__":
    app()
