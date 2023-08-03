import json

import xapian
from pydantic import BaseModel

from .field import Field, IdField, KeywordField, TextField
from .search import SearchQuery
from .utils import first


def index_text_field(
    term_generator: xapian.TermGenerator,
    insert_value: str,
    prefix: str,
    weight: int = 1
):
    term_generator.index_text(
        insert_value,
        weight,
        prefix  # the prefix
    )

    # index field without prefix for general search
    term_generator.index_text(insert_value)
    term_generator.increase_termpos()


def index_id_field(
    term_generator: xapian.TermGenerator,
    insert_value: str,
    prefix: str,
    weight: int = 1
):
    doc = term_generator.get_document()
    id_as_term = insert_value.replace('-', '')
    doc.add_boolean_term(prefix + id_as_term)

    term_generator.index_text(id_as_term, weight, prefix)
    term_generator.index_text(id_as_term)
    term_generator.increase_termpos()


def index_keyword_field(
    term_generator: xapian.TermGenerator,
    insert_value: str,
    prefix: str
):
    doc = term_generator.get_document()
    doc.add_boolean_term(
        prefix + insert_value.lower()
    )


class Session:
    def __init__(self, engine, language="en"):
        self._engine = engine
        self._termgenerator = xapian.TermGenerator()
        self._termgenerator.set_stemmer(xapian.Stem(language))
        self._queryparser = xapian.QueryParser()
        self._queryparser.set_stemmer(xapian.Stem(language))
        self._queryparser.set_stemming_strategy(self._queryparser.STEM_SOME)

    def add(self, entity: BaseModel):
        doc = xapian.Document()
        self._termgenerator.set_document(doc)

        primary_key_name = None

        for name, field in entity.model_fields.items():
            field_instance = first(field.metadata)
            value = getattr(entity, name)
            if isinstance(value, Field):
                insert_value = value.default
            else:
                insert_value = value
            if not insert_value:
                continue
            prefix = name.upper()

            if isinstance(field_instance, TextField):
                index_text_field(self._termgenerator, insert_value, prefix)
            elif isinstance(field_instance, KeywordField):
                index_keyword_field(
                    self._termgenerator,
                    insert_value,
                    prefix
                )
            elif isinstance(field_instance, IdField):
                if isinstance(insert_value, str):
                    index_id_field(self._termgenerator, insert_value, prefix)

            id_field = first(field.metadata, lambda x: type(x) is IdField)

            if id_field and id_field.primary_key:
                primary_key_name = name

        doc.set_data(
            json.dumps(entity.model_dump())
        )

        if not primary_key_name:
            raise ValueError("No primary field defined")

        identifier = getattr(entity, primary_key_name)
        idterm = f"Q{identifier}"
        doc.add_boolean_term(idterm)

        self._engine._db.replace_document(idterm, doc)
        self._engine._db.commit()

    def remove(self, entity: BaseModel):
        idterm = f"Q{entity.pk}"
        self._engine._db.delete_document(idterm)
        self._engine._db.commit()

    def exec(self, sq: SearchQuery):
        results = []
        for name, field in sq._entity.model_fields.items():
            self._queryparser.add_prefix(name, name)

        query = self._queryparser.parse_query(sq._query)
        enquire = xapian.Enquire(self._engine._db)
        enquire.set_query(query)

        for match in enquire.get_mset(0, 10):
            fields = json.loads(match.document.get_data().decode('utf8'))
            results.append(sq._entity(**fields))

        return results
