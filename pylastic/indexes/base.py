from dataclasses import dataclass


class ElasticIndexMetaclass(type):
    def __new__(cls, name, bases, dct):
        return dataclass(super().__new__(cls, name, bases, dct))  # noqa


class ElasticIndex(metaclass=ElasticIndexMetaclass):
    """
    Base Elasticsearch Index class

    Inherit indexes from it and manipulate them in ORM-like ways
    """

    ...
