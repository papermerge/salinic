from enum import Enum

import xapian

from .utils import get_db_path


class AccessMode(Enum):
    RO = 1  # read only
    RW = 2  # read/write


class Engine:

    def __init__(self, dsn: str, mode: AccessMode = AccessMode.RO):
        self._dsn = dsn
        self._db_path = get_db_path(dsn)
        if mode == AccessMode.RO:
            self._db = xapian.Database(self._db_path)
        else:  # mode == AccessMode.RW
            self._db = xapian.WritableDatabase(
                self._db_path,
                xapian.DB_CREATE_OR_OPEN
            )


def create_engine(dsn: str, mode: AccessMode = AccessMode.RO) -> Engine:
    return Engine(dsn, mode=mode)
