import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SchemeEnum(str, Enum):
    xapian = 'xapian'
    solr = 'solr'
    solrs = 'solrs'
    # solr secure, means solr over secure http i.e. (https)


class URL(BaseModel):
    scheme: SchemeEnum
    """search engine backend name, such as ``xapian``, ``solr``,
    ``solrs`` (solr secure)
    """

    username: Optional[str]

    password: Optional[str]

    host: Optional[str]

    port: Optional[int]
    "integer port number"

    index: Optional[str]
    "index name"


def make_url(name_or_url: str | URL) -> URL:
    if isinstance(name_or_url, str):
        return _parse_url(name_or_url)
    elif not isinstance(name_or_url, URL):
        raise ValueError(
            f"Expected string or URL object, got {name_or_url!r}"
        )
    else:
        return name_or_url


def _parse_url(name: str) -> URL:
    pattern = re.compile(
        r"""
            (?P<scheme>[\w\+]+)://
            (?:
                (?P<username>[^:/]*)
                (?::(?P<password>[^@]*))?
            @)?
            (?:
                (?:
                    \[(?P<ipv6host>[^/\?]+)\] |
                    (?P<ipv4host>[^/:\?]+)
                )?
                (?::(?P<port>[^/\?]*))?
            )?
            (?:/(?P<index>[^\?]*))?
            """,
        re.X,
    )

    m = pattern.match(name)
    if m is not None:
        components = m.groupdict()

        ipv4host = components.pop("ipv4host")
        ipv6host = components.pop("ipv6host")
        components["host"] = ipv4host or ipv6host

        if components["port"]:
            components["port"] = int(components["port"])

        return URL(**components)

    else:
        raise ValueError(
            "Could not parse URL from string '%s'" % name
        )
