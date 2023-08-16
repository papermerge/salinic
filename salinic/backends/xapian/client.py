import xapian

from salinic.utils import get_db_path

RO = 'ro'
RW = 'rw'


class Client:

    def __init__(self, dsn: str, mode: str = RO):
        self._db_path = get_db_path(dsn)
        if mode == RO:
            self._db = xapian.Database(self._db_path)
        else:  # mode == AccessMode.RW
            self._db = xapian.WritableDatabase(
                self._db_path,
                xapian.DB_CREATE_OR_OPEN
            )

    def replace_document(self, idterm: str, doc: xapian.Document):
        self.db.replace_document(idterm, doc)
        self.commit()

    def delete_document(self, docid: str):
        self.db.delete_document(docid)
        self.commit()

    def commit(self) -> None:
        self.db.commit()

    @property
    def db(self) -> xapian.Database | xapian.WritableDatabase:
        return self._db
