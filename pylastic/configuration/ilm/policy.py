from typing import List

from pylastic.configuration.base_configuration import BaseClusterConfiguration
from pylastic.request_template import RequestTemplate


class ILMPolicy(BaseClusterConfiguration):
    """
    Index Lifecycle Management Policy Configuration

    See https://www.elastic.co/guide/en/elasticsearch/reference/current/overview-index-lifecycle-management.html
    """

    def to_requests(self) -> List[RequestTemplate]:
        pass
