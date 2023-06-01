from abc import abstractmethod, ABC
from typing import Any, Optional


class ElasticType:
    """
    Base ES Field Type class.

    Defines an interface that is used by the index to validate types
    """

    @classmethod
    def is_valid_value(cls, value: Any, raise_exception: bool = True) -> bool:
        try:
            valid = cls.get_valid_object(value)
        except:  # noqa
            if raise_exception:
                raise
            return False

        if valid is None:
            if raise_exception:
                raise ValueError(
                    f'Value "{value}" cannot be converted to type {cls.__name__}'
                )
            return False

        return True

    @classmethod
    def get_valid_object(cls, value: Any) -> Optional[Any]:
        """
        If this object is valid (i.e. it'll be recognized as this type by ES), return it. Otherwise, return `None`
        """
        return value
