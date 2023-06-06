from typing import Optional, List, Type
from elasticsearch import Elasticsearch
from pylastic.indexes import ElasticIndex
from pylastic.request_template import RequestTemplate
from elastic_transport._response import ApiResponse  # noqa


class ElasticClient:
    """
    ElasticSearch Client
    """

    es_client: Elasticsearch

    def __init__(
        self, host: str, port: int, username: str, password: str, scheme: str = "https"
    ):
        """
        Instantiate ElasticSearch client

        :param host: ES Host
        :param port: ES Port
        :param username: ES Username to use (Basic Auth)
        :param password: ES Password to use (BasicAuth)
        :param scheme: HTTP/HTTPS
        """
        self.es_client = Elasticsearch(
            hosts=[f"{scheme}://{host.strip('https://').strip('http://')}:{port}"],
            basic_auth=(username, password),
        )

    def create_index(self, index: Type[ElasticIndex], index_name: Optional[str] = None) -> bool:
        """
        Create an Elasticsearch index from a `ElasticIndex` subclass (**not an instance**)

        :param index: `ElasticIndex` subclass. Class **must** have `Meta.index` set or `index_name` argument must be specified.
        :param index_name: Custom index name to use
        :return: Whether the index was successfully created in the cluster
        """
        if not index.get_static_index() and index_name is None:
            raise RuntimeError(
                f"Unable to create an elastic index with dynamic definition from a class. "
                f"Pass a class instance"
            )

        return self.execute(index.get_static_index_creation_request(index_name))[
            "acknowledged"
        ]

    def execute(self, template: RequestTemplate):
        """
        Execute a request

        :param template: Request template to execute.

        :return:
        """
        response: ApiResponse = self.es_client.perform_request(**template.to_kwargs())

        return response
