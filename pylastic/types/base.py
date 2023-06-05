from typing import Any, Optional


class ElasticType:
    """
    Base ES Field Type class.

    Defines an interface that is used by the index to validate types
    """

    def __init__(self):
        """
        Instantiate ElasticType. Subclasses might override this method to add new functionality
        """
        pass

    class Meta:
        # Must be defined in a subclass
        type = None

    @classmethod
    def is_valid_value(cls, value: Any, raise_exception: bool = True) -> bool:
        """
        Check if a provided value will be interpreted as this type in ES
        It uses `get_valid_object` method that can be changed in subclasses.

        :param value: Value to test
        :param raise_exception: Whether to raise exception if a value is invalid, or just return `False`
        :return: A boolean indicating whether this value is of correct type (or can be cast to a type in ES)
        """
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

    @staticmethod
    def get_mapping_of(class_or_instance) -> dict:
        """
        Return object mapping (type, ...). Works with `ElasticType` subclasses or their instances.
        Evaluates in the following order:
        - If it's an instance:
            1. Check if `get_mapping` is defined and returns a dict. If so, use it
            3. Check if `self._type` is defined on the instance (because `Meta` class is shared). If so, use it.
            2. Use `Meta.type`
        - If it's a class:
            Use `Meta.type`

        If an ElasticType subclass wants to override its mapping definition,
        overriding the `get_mapping` method is the way to go!

        :return: Mapping of the class or instance
        """
        if isinstance(class_or_instance, ElasticType):
            custom_mapping = getattr(  # noqa
                class_or_instance, "get_mapping", lambda: None
            )()
            if isinstance(custom_mapping, dict):
                return custom_mapping
            elif custom_type := getattr(class_or_instance, '_type', None):
                return {'type': custom_type}
            else:
                return {"type": class_or_instance.Meta.type}
        elif issubclass(class_or_instance, ElasticType):
            return {"type": class_or_instance.Meta.type}
        else:
            raise ValueError(
                f"Unable to detect the elastic type of an object that is not a `ElasticType` subclass"
            )
