from abc import ABC, abstractmethod
from typing import Any, List, Optional

from pylastic.request_template import RequestTemplate


class BaseClusterConfiguration(ABC):
    """This class provides a common client interface to all the available configuration options."""

    def _get_meta_attribute(self, name: str) -> Any | None:
        if hasattr(self, "Meta") and (value := getattr(self.Meta, name)):
            return value
        return None

    @abstractmethod
    def to_requests(self) -> List[RequestTemplate]:
        """
        Convert this configuration to a set of requests

        :return: List of request templates to be executed sequentially
        """
        raise NotImplementedError()

    @abstractmethod
    def is_valid(self, raise_exception: bool = False) -> Optional[bool]:
        raise NotImplementedError()

    class Meta:
        name = "abc"
