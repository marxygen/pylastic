import dataclasses
from dataclasses import dataclass, fields
from typing import Union, get_origin, get_args

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
