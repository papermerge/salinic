from typing import List, Tuple

from salinic.field import Field, NumericField
from salinic.utils import first

from .types import CopyFieldDump, FieldDump, FieldType


class SchemaManager:
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def create(self):
        self.client.update_schema(self.create_dict_dump())

    def apply(self):
        self.client.update_schema(self.apply_dict_dump())

    def delete(self):
        self.client.update_schema(self.delete_dict_dump())

    def create_dict_dump(self):
        add_copy_field = [
            m.model_dump() for _, m in self._copy_fields()
        ]
        add_field = [
            m.model_dump() for _, m in self._normal_fields()
        ]

        return {
            'add-field': add_field,
            'add-copy-field': add_copy_field
        }

    def apply_dict_dump(self):
        ret = {
            'add-field': [],
            'replace-field': [],
            'add-copy-field': []
        }
        for name, m in self._copy_fields():
            ret['add-copy-field'].append(m.model_dump())

        for name, m in self._normal_fields():
            if self.client.field_exists(name):
                ret['replace-field'].append(m.model_dump())
            else:
                ret['add-field'].append(m.model_dump())

        return ret

    def delete_dict_dump(self):
        copy_fields = [
            m.model_dump() for _, m in self._copy_fields()
        ]
        normal_fields = [
             {'name': m.name} for _, m in self._normal_fields()
        ]

        return {
            'delete-field': normal_fields,
            'delete-copy-field': copy_fields
        }

    def _copy_fields(self) -> List[Tuple[str, CopyFieldDump]]:
        for name, field in self.model.model_fields.items():
            field_instance: Field = first(field.metadata)
            if field_instance.general_search or name == 'id':
                if field_instance.multi_lang:
                    source = f"{name}_*"
                else:
                    source = name

                yield name, CopyFieldDump(
                    source=source,
                    dest=["_text_"]
                )

    def _normal_fields(self) -> List[Tuple[str, FieldDump]]:
        for name, field in self.model.model_fields.items():
            if name == "id":
                continue
            field_instance: Field = first(field.metadata)

            if field_instance.multi_lang:
                continue

            if isinstance(field_instance, NumericField):
                _type = FieldType.pint
            else:
                _type = FieldType.text_general

            yield name, FieldDump(
                name=name,
                type=_type,
                multiValued=field_instance.multi_value,
                indexed=field_instance.index,
                stored=field_instance.store
            )
