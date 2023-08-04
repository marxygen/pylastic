from abc import ABC, abstractmethod
from typing import List

from pylastic.request_template import RequestTemplate


class BaseClusterConfiguration(ABC):
    """This class provides a common client interface to all the available configuration options."""

    @property
    def _policy_name(self) -> str:
        if not hasattr(self, 'Meta') or not getattr(self.Meta, 'name', None):
            return self.__class__.__name__.lower()

        return self.Meta.name

    @abstractmethod
    def to_requests(self) -> List[RequestTemplate]:
        """
        Convert this configuration to a set of requests

        :return: List of request templates to be executed sequentially
        """
        raise NotImplementedError()

    class Meta:
        name = "abc"
