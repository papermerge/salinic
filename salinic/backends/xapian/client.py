import xapian

from salinic.url import URL

RO = 'ro'
RW = 'rw'


class ClientRW:

    def __init__(self, url: URL):
        self._db_path = url.index
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


class ClientRO:

    def __init__(self, url: URL):
        self._db_path = url.index
        self._db = xapian.Database(self._db_path)

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
