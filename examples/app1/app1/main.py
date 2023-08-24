import json

import typer
from app1.schema import Model

from salinic import IndexRO, IndexRW, Search, create_engine

app = typer.Typer()


INDEX_URL = "solr://localhost:8983/myindex"


@app.command()
def index_add(data_path: str):
    engine = create_engine(INDEX_URL)
    index = IndexRW(engine, schema=Model)

    with open(data_path) as f:
        data = json.load(f)

    for item in data:
        model = Model(**item)
        index.add(model)


@app.command()
def index_delete(docid: str):
    engine = create_engine(INDEX_URL)
    index = IndexRW(engine, schema=Model)
    index.remove({"id": docid})


@app.command()
def search(querystring: str):
    engine = create_engine(INDEX_URL)
    index = IndexRO(engine, schema=Model)

    sq = Search(Model).query(querystring)

    for entity in index.search(sq):
        print(entity)


if __name__ == "__main__":
    app()
