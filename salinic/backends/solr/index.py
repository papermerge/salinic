from typing import List

from pydantic import BaseModel, ConfigDict

from salinic.field import CopyFieldDump, Field, FieldDump
from salinic.query import SearchQuery
from salinic.utils import filter_keys, first, trim_suffixes


def to_dash(string: str) -> str:
    return '-'.join(word for word in string.split('_'))


class IndexSchemaDump(BaseModel):
    model_config = ConfigDict(alias_generator=to_dash)

    add_field: List[FieldDump]
    add_copy_field: List[CopyFieldDump]


class Base:
    def __init__(self, client, schema):
        self.client = client
        self.schema = schema

    def search(self, sq: SearchQuery):
        result = self.client.search(sq)
        if result['numFound'] == 0:
            return []

        docs_list = [
            trim_suffixes(doc) for doc in result['response']['docs']
        ]
        docs = filter_keys(docs_list, ['_version_'])

        return [sq.entity(**doc) for doc in docs]

    def index_schema_dump(self):
        """returns Index's schema generated from model"""

        add_copy_field = [
            m.model_dump() for m in self._index_copy_fields_dump()
        ]
        add_field = [
            m.model_dump() for m in self._index_add_fields_dump()
        ]

        return IndexSchemaDump.model_validate({
            'add-field': add_field,
            'add-copy-field': add_copy_field
        }).model_dump(by_alias=True)

    def _index_copy_fields_dump(self) -> List[CopyFieldDump]:
        copy_fields = []

        for name, field in self.schema.model_fields.items():
            field_instance: Field = first(field.metadata)
            if field_instance.general_search or name == 'id':
                if field_instance.multi_lang:
                    source = f"{name}_*"
                else:
                    source = name

                copy_field = CopyFieldDump(
                    source=source,
                    dest=["_text_"]
                )
                copy_fields.append(copy_field)

        return copy_fields

    def _index_add_fields_dump(self) -> List[FieldDump]:
        add_fields = []
        for name, field in self.schema.model_fields.items():
            if name == "id":
                continue
            field_instance: Field = first(field.metadata)

            if field_instance.multi_lang:
                continue

            add_fields.append(
                FieldDump(
                    name=name,
                    type='text_general',
                    multiValued=field_instance.multi_value,
                    indexed=field_instance.index,
                    stored=field_instance.store
                )
            )

        return add_fields


class IndexRW(Base):
    def add(self, model: BaseModel):
        model_dict = model.model_dump()

        for name, field in self.schema.model_fields.items():
            field_instance: Field = first(field.metadata)
            if field_instance.multi_lang:
                # add suffix to multi lang keys:
                # e.g. 'title' -> 'title_txt_en'
                #       'text' -> 'text_txt_en'
                lang_key = model.model_config.get('lang_field_name', 'en')
                lang_value = model_dict[lang_key]
                model_dict[f'{name}_txt_{lang_value}'] = model_dict.pop(name)

        self.client.add(model_dict)

    def remove(self, docid: str):
        self.client.remove(docid)


IndexRO = IndexRW
