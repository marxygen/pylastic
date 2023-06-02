from typing import Optional
from elasticsearch import Elasticsearch
from pylastic.indexes import ElasticIndex


class ElasticClient:
    """
    ElasticSearch Client
    """

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
        self._client = Elasticsearch(
            hosts=[f"{scheme}://{host}:{port}"], basic_auth=(username, password)
        )

    def create(self, index: ElasticIndex | str, mapping: Optional[dict] = None) -> None:
        """
        Create an Elasticsearch index.

        :param index: Index name as string or an `ElasticIndex` subclass
        :param mapping: Mapping to specify. If `index` is a string, this parameter is **required**. If `index` is an `ElasticIndex` subclass,
        the generated mapping will be used
        """
        self._client.create()
