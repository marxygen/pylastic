from typing import List, Optional

from pylastic.configuration.base_configuration import BaseClusterConfiguration
from pylastic.request_template import RequestTemplate


class ILMPolicy(BaseClusterConfiguration):
    """
    Index Lifecycle Management Policy Configuration

    See https://www.elastic.co/guide/en/elasticsearch/reference/current/overview-index-lifecycle-management.html
    """

    ENDPOINT = "_ilm/policy/my_policy"
    HTTP_METHOD = "PUT"
    PHASES = ["hot", "warm", "cold", "frozen", "delete"]

    @property
    def _policy_name(self) -> str:
        return self._get_meta_attribute("name") or self.__class__.__name__.lower()

    @property
    def metadata(self) -> dict:
        if hasattr(self, "Meta"):
            return {
                key: value
                for key, value in self.Meta.__dict__.items()
                if not key.startswith("_")
            }
        return {}

    @property
    def phases(self) -> dict:
        for phase in self.PHASES:
            class_name = phase.capitalize()
            if not hasattr(self, class_name):
                continue

            # TODO: convert phases from class to dict https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-put-lifecycle.html

    def to_requests(self) -> List[RequestTemplate]:
        phases = {}
        body = {"policy": {"_meta": self.metadata, "phases": phases}}
        return [RequestTemplate(path=self.ENDPOINT, body=body, method=self.HTTP_METHOD)]

    def is_valid(self, raise_exception: bool = False) -> Optional[bool]:
        """
        Check if this ILM policy is valid

        :param raise_exception: Whether to raise an exception
        """
        for phase in ("hot", "warm", "cold", "frozen", "delete"):
            ...
