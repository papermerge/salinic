import logging

import requests
from requests.exceptions import HTTPError

from salinic.query import SearchQuery
from salinic.url import URL

logger = logging.getLogger(__name__)


class Base:
    def __init__(self, url: URL):
        self._url = url


class ClientRW(Base):

    def search(self, sq: SearchQuery, user_id: str | None = None):
        payload = {
            'q': sq.query.original_query,
            'rows': sq.rows,
            'start': sq.start,
        }

        if user_id:
            payload['q'] = f"{payload['q']} AND user_id:{user_id}"

        response = requests.get(
            self.http_select_url,
            params=payload
        )
        logger.debug(payload)

        result = response.json()

        return result

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
        logger.debug(
            f'POST {self.http_update_url} json={data}'
        )
        response = requests.post(
            self.http_schema_url,
            json=data
        )
        response.raise_for_status()

    def field_exists(self, name: str) -> bool:
        # for normal fields
        url = self.http_field_url(name)
        logger.debug(f'GET {url}')
        response = requests.get(url)

        try:
            response.raise_for_status()
        except HTTPError:
            if response.status_code == 404:
                # status 404 indicates that field does not exist, this
                # is normal flow
                logger.debug(f"Field {name} does not exist")
                return False
            # we got some other error messages (i.e. != 404)
            # log it
            logger.exception()
            return False

        return True

    def dynamicfield_exists(self, name: str) -> bool:
        url = self.http_dynamicfield_url(name)
        logger.debug(f'GET {url}')
        response = requests.get(url)

        try:
            response.raise_for_status()
        except HTTPError:
            if response.status_code == 404:
                # status 404 indicates that field does not exist, this
                # is normal flow
                logger.debug(f"Dynamic field {name} does not exist")
                return False
            # we got some other error messages (i.e. != 404)
            # log it
            logger.exception()
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
