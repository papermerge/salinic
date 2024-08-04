import json
import logging

from glom import glom
from pydantic import BaseModel

from salinic.field import Field
from salinic.query import SearchQuery
from salinic.schema import DocumentPage, Folder
from salinic.utils import first

logger = logging.getLogger(__name__)


class Base:
    def __init__(self, client, schema):
        self.client = client
        self.schema = schema

    def search(
        self,
        sq: SearchQuery,
        user_id: str | None = None
    ) -> list[DocumentPage | Folder]:
        """Query index"""
        result = self.client.search(sq, user_id)
        items = glom(result, 'response.docs')
        returned_list = []

        for item in items:
            if document_id := item.get('document_id', None):
                lang = item.get('lang', 'en')
                title = item.get(f'title_txt_{lang}', lang)
                tags = item.get('tags', [])
                dp = DocumentPage(
                    id=item['id'],
                    page_number=item['page_number'],
                    document_id=document_id,
                    title=title,
                    lang=lang,
                    tags=tags
                )
                returned_list.append(dp)
            else:
                lang = item.get('lang', 'en')
                title = item.get(f'title_txt_{lang}', lang)
                folder = Folder(
                    id=item['id'],
                    title=title,
                    lang=lang,
                    tags=item.get('tags', []),
                )
                returned_list.append(folder)

        return returned_list


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
            if model.needs_transform(name):
                actual_value = model.get_field_value(name)
                orig_value = model_dict.pop(name)
                model_dict[name] = actual_value
                model_dict[f'{name}_orig_'] = json.dumps(orig_value)

        self.client.add(model_dict)

    def remove(self, **kwargs):
        logger.debug("Remove document with kwargs={kwargs}")
        self.client.remove(**kwargs)


IndexRO = IndexRW
