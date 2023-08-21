from pydantic import BaseModel

from salinic.field import Field
from salinic.query import SearchQuery
from salinic.utils import filter_keys, first, trim_suffixes


class Base:
    def __init__(self, client, schema):
        self.client = client
        self.schema = schema

    def search(self, sq: SearchQuery):
        result = self.client.search(sq)
        if result['response']['numFound'] == 0:
            return []

        docs_list = [
            trim_suffixes(doc) for doc in result['response']['docs']
        ]
        docs = [
            filter_keys(some_doc, ['_version_'])
            for some_doc in docs_list
        ]

        return [sq.entity(**doc) for doc in docs]


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
