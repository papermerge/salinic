def validate(dsn: str):
    parts = dsn.split('://')
    if len(parts) < 2:
        raise ValueError(
            'Invalid dsn format. Should be scheme://value'
        )

    if parts[0] not in ('xapian', 'solr'):
        raise ValueError(
            'Unsupported scheme.'
            'Only xapian and solr schemes are supported'
        )

    return parts


class Dsn:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._parts = validate(dsn)

    @property
    def scheme(self):
        return self._parts[0]

    @property
    def db_path(self):
        return self._parts[1]

    def __str__(self):
        return self._dsn
