import json

import typer
from app1.schema import Model

from salinic import IndexRW, create_engine

app = typer.Typer()


@app.command()
def index_add(data_path: str):
    engine = create_engine("solr://localhost:8983/myindex")
    index = IndexRW(engine, schema=Model)

    with open(data_path) as f:
        data = json.load(f)

    for item in data:
        model = Model(**item)
        index.add(model)


@app.command()
def index_delete(title: str):
    print(f"index delete {title}")


@app.command()
def search(query: str):
    print(f"search {query}!")


if __name__ == "__main__":
    app()
