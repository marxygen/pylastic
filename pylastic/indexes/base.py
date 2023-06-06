import dataclasses
import json
import sys
from dataclasses import dataclass, fields
from typing import Union, get_origin, get_args, Dict, Type, Any, Optional, Sequence

from pylastic.request_template import RequestTemplate
from pylastic.types.base import ElasticType


class ElasticIndexMetaclass(type):
    def __new__(cls, name, bases, dct):
        return dataclass(super().__new__(cls, name, bases, dct))  # noqa


class ElasticIndex(metaclass=ElasticIndexMetaclass):
    """
    Base Elasticsearch Index class

    Inherit indexes from it and manipulate them in ORM-like ways
    """

    class Meta:
        index: str = None
        is_datastream: bool = False
        id_field: str = "_id"

    def __init__(self, *args, **kwargs):
        # This method is just to shut type checks up
        # It's actually coming from a dataclass
        ...

    @property
    def is_datastream(self) -> bool:
        return getattr(self.Meta, "is_datastream", False)

    @classmethod
    @property
    def id_field(cls) -> str | None:
        return getattr(cls.Meta, "id_field", "_id")

    def get_id(self) -> Any | None:
        return getattr(self, self.id_field, None)

    def get_index(self) -> str | None:
        """
        Get index name
        Note that this method is not static, so you can override it in a subclass and create custom index names based on field values

        :return: Name of the index or `None`, if not specified or not applicable (if `is_datastream` is set)
        """
        if self.is_datastream:
            return None

        return self.Meta.index

    @classmethod
    def get_static_index(cls) -> str | None:
        """
        Get `cls.Meta.index` field or `None`
        """
        try:
            return cls.Meta.index
        except AttributeError:
            return None

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

        def resolve_type(type_: Type | ElasticType) -> dict | None:
            if isinstance(type_, ElasticType) or issubclass(type_, ElasticType):
                return ElasticType.get_mapping_of(type_)

            match type_.__name__:
                case "str":
                    return {"type": "text"}
                case "int":
                    return {"type": "integer"}
                case "float":
                    return {"type": "float"}
                case "bool":
                    return {"type": "boolean"}
                case "dict":
                    return {"type": "object"}
                case "list":
                    return {"type": "object"}
                case _:
                    return None

        properties = {}
        for name, type_ in cls._get_fields_with_types().items():
            # _id field should be excluded from the mapping
            if name == cls.id_field:
                continue

            es_type = resolve_type(type_)
            properties[name] = es_type

        return {"mappings": {"properties": properties}}

    def get_body(self) -> dict:
        return {field: getattr(self, field) for field in self._get_fields_with_types() if field != self.id_field}

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
        # Validate fields
        for field in fields(self):
            value = getattr(self, field.name)
            field_type: ElasticType | Type = field.type
            default = field.default
            if get_origin(field_type) is Union:
                field_type = get_args(field_type)[0]

            if value is None and default != dataclasses.MISSING:
                continue

            if not issubclass(field_type, ElasticType):
                # Since it's a built-in type, attempt to transform it
                field_type(value)
                continue

            try:
                field_type.is_valid_value(value, raise_exception=True)
            except Exception as e:
                raise ValueError(
                    f"{e.__class__.__name__} validating "
                    f"{self.__class__.__name__}.{field.name} ({value}): {e}"
                ) from e

        if self.id_field != "_id":
            # https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html
            if self.get_id() is None:
                raise ValueError(
                    f"If a custom ID field is specified, it must be populated"
                )

            if sys.getsizeof(self.get_id()) > 512:
                raise ValueError(f"Elasticsearch limits ID field length to 512 bytes")
            # TODO: remove _id field from mappings

    @classmethod
    def _get_meta_attribute(cls, attr, default: Any = None) -> Any:
        try:
            return getattr(cls.Meta, attr)
        except AttributeError:
            return default

    @classmethod
    def get_index_settings(cls) -> dict:
        return {
            "number_of_shards": cls._get_meta_attribute("primary_shards", 1),
            "codec": cls._get_meta_attribute("compression", "default"),
            "number_of_replicas": cls._get_meta_attribute("replicas", 1),
            # Override and expand index settings
            **cls._get_meta_attribute("index_settings", {}),
        }

    # Define request template builders
    @classmethod
    def get_static_index_creation_request(
        cls, index_name: str = None
    ) -> RequestTemplate:
        return RequestTemplate(
            method="PUT",
            path=f"/{index_name or cls.get_static_index()}",
            body={**cls.get_mapping(), "settings": cls.get_index_settings()},
        )

    def get_index_creation_request(self) -> RequestTemplate:
        return self.get_static_index_creation_request(index_name=self.get_index())

    @classmethod
    def get_index_refresh_template(
        cls, index_name: Optional[str] = None
    ) -> RequestTemplate:
        return RequestTemplate(
            path=f"/{index_name or cls.get_static_index()}/_refresh", method="POST"
        )

    def get_create_document_request(self) -> RequestTemplate:
        return RequestTemplate(
            method="POST",
            path=f"/{self.get_index()}/_doc/" + (self.get_id() or ""),
            body=self.get_body(),
        )

    @staticmethod
    def get_batch_create_request(
        documents: Sequence["ElasticIndex"],
    ) -> RequestTemplate:
        # https://www.elastic.co/guide/en/elasticsearch/reference/8.8/docs-bulk.html#docs-bulk
        body = ""
        for d in documents:
            body += (
                json.dumps({"index": {"_index": d.get_index(), "_id": d.get_id()}}) + "\n" + json.dumps(d.get_body()) + "\n"
            )
        body += "\n"
        return RequestTemplate(body=body, method="POST", path="/_bulk")
