from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_serializer

from .field import Field, IdField
from .utils import first


class Schema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_serializer()
    def model_ser(self):
        result = {}
        for name, field in self.model_fields.items():
            default_value = getattr(self, name)
            if isinstance(default_value, Field):
                result[name] = field.default.default
            else:
                result[name] = default_value

        return result

    @property
    def pk(self):
        """returns the value of the primary key field"""
        primary_key_name = self.pk_name

        if primary_key_name is None:
            raise ValueError("No primary field defined")

        result = getattr(self, primary_key_name)
        if result:
            return result.replace('-', '')

        return result

    @property
    def pk_name(self):
        """returns the name of the primary key field"""
        for name, field in self.model_fields.items():
            id_field = first(field.metadata, lambda x: type(x) is IdField)
            if id_field and id_field.primary_key:
                return name

        return None

    def get_field_value(self, field_name):
        """Returns the field value to actually be stored on the index

        Value actually stored in the index may differ from the one in the
        model. Let's consider an example when index schema has a field
        composed of a list of colored tags (tag has a name and a color):

            from salinic import IdField, KeywordField, Schema
            from pydantic import BaseModel

            class ColoredTag(BaseModel):
                name: str   # e.g. of value 'important'
                color: str  # e.g. of value '#ff00dd'

            class Index(Schema):
                id: Annotated[str, IdField(primary_key=True)]
                tags: Annotated[List[ColoredTag], KeywordField()]

        In context of full text search user will
        look up models only based on tags name; in other words, it does
        not make sense to index the color of the tag.
        However, when it comes to displaying the tag to the user, user of course
        wants to see the colored tag (not just names).

        `get_field_value` returns value of the given field which will actually
        be indexed (i.e. user will search by that specific part of the field).
        This method may be overriden by defining method with following name:

            `get_idx_value__<field_name>`
        """
        if self.needs_transform(field_name):
            func = getattr(self, f'get_idx_value__{field_name}')
            return func()

        return getattr(self, field_name)

    def needs_transform(self, field_name):
        return hasattr(self, f'get_idx_value__{field_name}')


class Page(BaseModel):
    id: UUID
    page_number: int
    text: str | None = None


class Document(BaseModel):
    id: UUID
    title: str
    lang: str
    tags: list[str] = []
    pages: list[Page]
    entity_type: str = 'document'

    def __hash__(self):
        return hash(self.model_dump_json())


class Folder(BaseModel):
    id: UUID
    title: str
    tags: list[str] = []
    entity_type: str = 'folder'

    def __hash__(self):
        return hash(self.model_dump_json())
