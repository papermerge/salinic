from typing import List, Optional, Tuple

from pydantic import BaseModel, ConfigDict
from typing_extensions import Annotated

from salinic.field import KeywordField, TextField, UUIDField
from salinic.schema import Schema

FOLDER = 'folder'
PAGE = 'page'


class ColoredTag(BaseModel):
    name: str
    fg_color: str
    bg_color: str


Tags = Annotated[
    Optional[list[ColoredTag]],
    KeywordField()  # will be indexed as a keyword
]
Breadcrumb = Annotated[
    List[Tuple[str, str]],
    KeywordField()  # will be indexed as a keyword
]


class Model(Schema):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        lang_field_name='lang'
    )

    id: Annotated[
        str,
        UUIDField(primary_key=True, general_search=True)
    ]  # page id | node_id

    # document ID to whom this page belongs
    document_id: Annotated[
        Optional[str],
        UUIDField(index=False, general_search=True)
    ] = None

    lang: Annotated[
        str,
        KeywordField()
    ] = 'en'

    title: Annotated[
        str,
        TextField(general_search=True, multi_lang=True)
    ]  # document or folder title

    # text is None in case folder entity
    text:  Annotated[
        Optional[str],
        TextField(general_search=True, multi_lang=True)
    ] = None

    entity_type: Annotated[
        str,
        KeywordField()
    ]  # folder | page

    breadcrumb: Annotated[
        List[Tuple[str, str]],
        KeywordField(multi_value=True)
    ]

    tags: Annotated[
        Optional[list[ColoredTag]],
        KeywordField(multi_value=True)
    ] = []

    def __str__(self):
        return f'IndexEntity(id={self.id}, title={self.title}, '\
            f'document_id={self.document_id},' \
            f'type={self.entity_type})'

    def get_idx_value__tags(self):
        return list([tag.name for tag in self.tags])

    def get_idx_value__breadcrumb(self):
        return list([item[1] for item in self.breadcrumb])
