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
