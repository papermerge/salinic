import requests
from pydantic import BaseModel

from salinic.query import SearchQuery
from salinic.url import URL


class Base:
    def __init__(self, url: URL):
        self._url = url


class ClientRW(Base):

    def search(self, sq: SearchQuery):
        payload = {
            'q': sq.query.original_query
        }

        response = requests.get(
            self.http_select_url,
            params=payload
        )

        return response.json()

    def add(self, model: BaseModel):
        # change data specific for add
        data = {}
        data['add'] = {'doc': model.model_dump()}
        return requests.post(self.http_update_url, json=data)

    def remove(self, **kwargs):
        # change data specific for delete
        data = {}
        data['delete'] = kwargs
        return requests.post(self.http_update_url, json=data)

    @property
    def http_index_url(self) -> str:
        """Returns the http url for solr index

        Example of http url to be returned:
            http://localhost:8983/solr/papermerge_index
        """
        s = "http"
        if self._url.scheme == 'solrs':
            s += "s"

        s += f"://{self._url.host}"
        if self._url.port is not None:
            s += f":{self._url.port}/solr/"
        else:
            s += "/solr/"

        s += f"{self._url.index}"

        return s

    @property
    def http_select_url(self) -> str:
        """Returns the http url for searching/selecting documents

        Example of http url to be returned:
            http://localhost:8983/solr/papermerge_index/select
        """
        return f"{self.http_index_url}/select"

    @property
    def http_update_url(self) -> str:
        """Returns the http url for adding/updating/deleting documents

        As of solr9 same http url is used for all CRUD operations on
        the documents.
        Example of http url to be returned:
            http://localhost:8983/solr/papermerge_index/update/json/docs
        """
        return f"{self.http_index_url}/update/json/docs"


ClientRO = ClientRW
