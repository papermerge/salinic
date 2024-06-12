import json
import logging

from glom import glom
from pydantic import BaseModel

from salinic.field import Field
from salinic.query import SearchQuery
from salinic.schema import Document, Folder, Page
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
    ) -> list[Document | Folder]:
        """Query index

        Solr results are grouped by `document_id` field: this way
        all folder entries will be part of group with `document_id=null`,
        while all page entities will be grouped per document i.e.
        pages which belong together are all in the same group.

        {
          "responseHeader":{
            ...
          "grouped":{
            "document_id":{
              "matches":26,
              "groups":[
                      "groupValue":null,
                      "doclist":{"numFound":4,"start":0,"numFoundExact":true,"docs":[
                          {
                            "id":"0b663599-32b1-4396-8dbe-ae7cd327cec6",
                            "lang":"en",
                            "user_id":"4cee7c39-7c34-4cc5-8543-42a8c88c9fe6",
                            "entity_type":"folder",
                            "title_txt_en":"A2  updated",
                            "_version_":1801539995817738240},
                          {
                            "id":"768c6841-d37a-4d02-857f-ab7eaf69b27e",
                            "lang":"en",
                            "user_id":"4cee7c39-7c34-4cc5-8543-42a8c88c9fe6",
                            "entity_type":"folder",
                            "title_txt_en":".inbox",
                            "_version_":1801539995692957696}]
                      }},
                {
                  "groupValue":"9bc57688-302e-4e1f-840a-c747dcccb362",
                  "doclist":{"numFound":5,"start":0,"numFoundExact":true,"docs":[
                      {
                        "id":"a6e4916f-dea6-414b-aa38-f5b9ea375725",
                        "document_id":"9bc57688-302e-4e1f-840a-c747dcccb362",
                        "lang":"en",
                        "user_id":"4cee7c39-7c34-4cc5-8543-42a8c88c9fe6",
                        "page_number":1,
                        "entity_type":"page",
                        "title_txt_en":"brother_004603.pdf",
                        "_version_":1801539996374532096},
                      {
                        "id":"72f6ca9e-af4b-4235-a56c-a62508e24efe",
                        "document_id":"9bc57688-302e-4e1f-840a-c747dcccb362",
                        "lang":"en",
                        "user_id":"4cee7c39-7c34-4cc5-8543-42a8c88c9fe6",
                        "page_number":2,
                        "entity_type":"page",
                        "title_txt_en":"brother_004603.pdf",
                        "_version_":1801539996403892224},]
                  }},
                {
                  "groupValue":"200b0201-cfcd-43df-b41f-f1732568a0d2",
                  "doclist":{"numFound":2,"start":0,"numFoundExact":true,"docs":[
                      {
                        "id":"9fa936e6-fe94-46bf-ad01-d8591cc290d4",
                        "document_id":"200b0201-cfcd-43df-b41f-f1732568a0d2",
                        "lang":"en",
                        "user_id":"4cee7c39-7c34-4cc5-8543-42a8c88c9fe6",
                        "page_number":1,
                        "entity_type":"page",
                        "title_txt_en":"brother_004598.pdf",
                        "_version_":1801539995874361344},
                      {
                        "id":"c364994c-eab5-4c6a-842a-6f40537f7a2e",
                        "document_id":"200b0201-cfcd-43df-b41f-f1732568a0d2",
                        "lang":"en",
                        "user_id":"4cee7c39-7c34-4cc5-8543-42a8c88c9fe6",
                        "page_number":2,
                        "entity_type":"page",
                        "title_txt_en":"brother_004598.pdf",
                        "_version_":1801539995910012928}]
                  }},
                  }}]}}}
        """
        result = self.client.search(sq, user_id)
        grouped = glom(result, 'grouped.document_id')
        if glom(grouped, 'matches') == 0:
            return []

        result = []
        for group in glom(grouped, 'groups'):
            if glom(group, 'groupValue'):
                # groupValue != null => document
                document_id = glom(group, 'groupValue')
                title = ''
                lang = 'en'
                tags = []
                pages = []
                for page in glom(group, 'doclist.docs'):
                    lang = page.get('lang', 'en')
                    title = page.get(f'title_txt_{lang}', None)
                    text = page.get(f'text_txt_{lang}', None)
                    tags = page.get('tags', [])
                    p = Page(
                        id=page['id'],
                        page_number=page['page_number'],
                        text=text
                    )
                    pages.append(p)
                item = Document(
                    id=document_id,
                    title=title,
                    lang=lang,
                    pages=pages,
                    tags=tags,
                )
                result.append(item)
            else:
                for folder in glom(group, 'doclist.docs'):
                    lang = folder.get('lang', 'en')
                    title = folder.get(f'title_txt_{lang}', None)
                    item = Folder(
                        id=folder['id'],
                        title=title,
                        tags=folder.get('tags', []),
                    )
                    result.append(item)

        return result


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
