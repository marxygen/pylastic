import dataclasses
from dataclasses import dataclass, fields
from typing import Union, get_origin, get_args, Dict, Type

from pylastic.types.base import ElasticType


class ElasticIndexMetaclass(type):
    def __new__(cls, name, bases, dct):
        return dataclass(super().__new__(cls, name, bases, dct))  # noqa


class ElasticIndex(metaclass=ElasticIndexMetaclass):
    """
    Base Elasticsearch Index class

    Inherit indexes from it and manipulate them in ORM-like ways
    """

    def __init__(self, *args, **kwargs):
        # This method is just to shut type checks up
        # It's actually coming from a dataclass
        ...

    @classmethod
    def get_mapping(cls) -> dict:
        """
        Get field mapping, e.g

        ```
        {
          "mappings": {
            "properties": {
              "car_id": {
                "type": "integer"
              },
              "manufacturer_loc": {
                "type": "geo_point"
              },
              "report_timestamp": {
                "type": "float"
              }
            }
          }
        ```
        If ES field type cannot be resolved for a field, it will **not** be included in the mapping definition.

        The following built-in types are transformed:
        - str -> "text"
        - int -> "integer"
        - float -> "float"
        - bool -> "boolean"
        - dict -> "object"
        - list -> "object"

        If a type is a subclass of `ElasticType`, `ElasticType.Meta.type` is used.

        :return: Full mapping
        """

        def resolve_type(type_: Type | ElasticType) -> str | None:
            if issubclass(type_, ElasticType):
                return type_.Meta.type

            match type_.__name__:
                case "str":
                    return "text"
                case "int":
                    return "integer"
                case "float":
                    return "float"
                case "bool":
                    return "boolean"
                case "dict":
                    return "object"
                case "list":
                    return "object"
                case _:
                    return None

        properties = {}
        for name, type_ in cls._get_fields_with_types().items():
            es_type = resolve_type(type_)
            if not es_type:
                continue
            properties[name] = es_type

        return {"mappings": {"properties": properties}}

    @classmethod
    def _get_fields_with_types(cls) -> Dict[str, "ElasticType"]:
        """
        Get a dictionary of <field name>: <field type>
        """
        mapping = {}
        for field in fields(cls):
            field_type: ElasticType = field.type
            if get_origin(field_type) is Union:
                field_type = get_args(field_type)[0]

            mapping[field.name] = field_type
        return mapping

    def validate(self):
        for field in fields(self):
            value = getattr(self, field.name)
            field_type: ElasticType = field.type
            default = field.default
            if get_origin(field_type) is Union:
                field_type = get_args(field_type)[0]

            if value is None and default != dataclasses.MISSING:
                continue

            field_type.is_valid_value(value, raise_exception=True)
