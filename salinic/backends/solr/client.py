import logging

import requests

from salinic.query import SearchQuery
from salinic.url import URL

logger = logging.getLogger(__name__)


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

    def add(self, some_dict):
        # change data specific for add
        data = dict()
        data['add'] = {'doc': some_dict}

        params = {'commit': 'true'}
        logger.debug(
            f'POST {self.http_update_url} json={data} params={params}'
        )
        response = requests.post(
            self.http_update_url,
            json=data,
            params=params
        )
        if response.status_code == 404:
            raise ValueError(
                f"Index {self.http_index_url} not found"
            )
        return response

    def remove(self, **kwargs):
        # change data specific for delete
        data = {}
        data['delete'] = kwargs

        params = {'commit': 'true'}
        logger.debug(
            f'POST {self.http_update_url} json={data} params={params}'
        )

        response = requests.post(
            self.http_update_url,
            json=data,
            params=params
        )

        if response.status_code == 404:
            raise ValueError(
                f"Index {self.http_index_url} not found"
            )

        return response

    def update_schema(self, data):
        return requests.post(
            self.http_schema_url,
            json=data
        )

    def field_exists(self, name: str) -> bool:
        # for normal fields
        response = requests.get(self.http_field_url(name))

        if response.status_code == 404:
            return False

        return True

    def dynamicfield_exists(self, name: str) -> bool:
        response = requests.get(self.http_dynamicfield_url(name))

        if response.status_code == 404:
            return False

        return True

    def http_field_url(self, name):
        return f"{self.http_index_url}/schema/fields/{name}"

    def http_dynamicfield_url(self, name):
        return f"{self.http_index_url}/schema/dynamicfields/{name}"

    @property
    def http_schema_url(self):
        return f"{self.http_index_url}/schema"

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
        return f"{self.http_index_url}/update"


ClientRO = ClientRW
