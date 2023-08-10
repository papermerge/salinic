from typing import List, Optional, Tuple

from pydantic import BaseModel
from typing_extensions import Annotated

from salinic import IdField, KeywordField, Schema, Search, Session, types


class Tag(BaseModel):
    name: str  # field to be indexed i.e. so
    bg_color: str
    fg_color: str


Breadcrumb = Annotated[
    List[Tuple[str, str]],
    KeywordField()
]

Tags = Annotated[
    Optional[List[Tag]],
    KeywordField()
]


class Index(Schema):
    id: Annotated[str, IdField(primary_key=True)]  # page id | node_id
    title: types.Text  # document or folder title
    breadcrumb: Breadcrumb  # mandatory keywords
    tags: Tags  # optional keywords

    def get_idx_value__tags(self) -> list[str]:
        """Returns field value which will be indexed"""
        return list([tag.name for tag in self.tags])

    def get_idx_value__breadcrumb(self) -> list[str]:
        """Returns field value which will be indexed"""
        return list([item[1] for item in self.breadcrumb])


def test_get_field_value():
    breadcrumb = [
        ('uuid-1', 'home'),
        ('uuid-2', 'my documents')
    ]
    tags = [
        Tag(name='important', fg_color='white', bg_color='red'),
        Tag(name='paid', fg_color='white', bg_color='green')
    ]
    index = Index(
        id="one",
        title="Some title",
        tags=tags,
        breadcrumb=breadcrumb
    )

    assert index.get_field_value('title') == 'Some title'
    assert index.get_field_value('tags') == ['important', 'paid']
    assert index.get_field_value('breadcrumb') == ['home', 'my documents']


class ColoredTag(BaseModel):
    name: str  # field to be indexed i.e. so
    color: str


ColoredTags = Annotated[
    Optional[List[ColoredTag]],
    KeywordField()
]


class Index2(Schema):
    id: Annotated[str, IdField(primary_key=True)]  # page id | node_id
    tags: ColoredTags

    def get_idx_value__tags(self) -> list[str]:
        """Returns field value which will be indexed"""
        return list([tag.name for tag in self.tags])


def test_index_vs_stored(session: Session):
    doc1 = Index2(
        id="one",
        tags=[
            ColoredTag(name="important", color="#ff0000"),
            ColoredTag(name="paid", color="#ffdd1a")
        ],
    )
    session.add(doc1)

    doc2 = Index2(
        id="two",
        tags=[],
    )

    session.add(doc2)

    sq = Search(Index2).query("tags:important")

    found: List[Index2] = session.exec(sq)

    assert len(found) == 1
    # search result retrieves tags field as list of ColoredTag instances
    assert found[0].tags == doc1.tags
    # however, tags field is indexed as List[str]
    assert doc1.get_field_value('tags') == ['important', 'paid']
