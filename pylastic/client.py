from typing import Optional, List, Type, Sequence, Dict
from elasticsearch import Elasticsearch, BadRequestError
from pylastic.indexes import ElasticIndex
from pylastic.request_template import RequestTemplate
from elastic_transport._response import ApiResponse  # noqa

from pylastic.utils.iterables import is_iterable, group_by_index, get_batches_with_size


class ElasticClient:
    """
    ElasticSearch Client
    """

    es_client: Elasticsearch

    def __init__(
        self,
        host: str | List[str],
        port: int,
        username: str,
        password: str,
        scheme: str = "https",
        connections_per_node: int = None,
        **kwargs,
    ):
        """
        Instantiate ElasticSearch client

        :param host: ES Host
        :param port: ES Port
        :param username: ES Username to use (Basic Auth)
        :param password: ES Password to use (BasicAuth)
        :param scheme: HTTP/HTTPS
        :param connections_per_node: Number of connections per node
        """
        if isinstance(host, str):
            hosts = [host]
        else:
            hosts = host

        self.es_client = Elasticsearch(
            hosts=[f"{scheme}://{h.strip('https://').strip('http://')}:{port}" for h in hosts],
            basic_auth=(username, password),
            connections_per_node=connections_per_node,
            **kwargs,
        )

    def create_index(
        self, index: Type[ElasticIndex], index_name: Optional[str] = None, exists_ok: bool = False
    ) -> bool:
        """
        Create an Elasticsearch index from a `ElasticIndex` subclass (**not an instance**).
        This method also will set up index lifecycle policies (ILP) if they're configured for the index.

        :param index: `ElasticIndex` subclass. Class **must** have `Meta.index` set or `index_name` argument must be specified.
        :param index_name: Custom index name to use
        :param exists_ok: Whether to suppress `resource_already_exists_exception` error
        :return: Whether the index was successfully created in the cluster
        """
        if (
            not hasattr(index, "get_static_index")
            or not index.get_static_index()
            and index_name is None
        ):
            raise RuntimeError(
                f"Unable to create an elastic index with dynamic definition from a class. "
                f"Pass a class instance"
            )

        try:
            response = self.execute(index.get_static_index_creation_request(index_name))
            return response["acknowledged"]

        except BadRequestError as bad_request:
            if bad_request.error == 'resource_already_exists_exception' and exists_ok:
                return True

            raise

    def execute(self, template: RequestTemplate):
        """
        Execute a request

        :param template: Request template to execute.

        :return:
        """
        response: ApiResponse = self.es_client.perform_request(**template.to_kwargs())

        return response

    def create_index_for(
        self, objects: ElasticIndex | Sequence[ElasticIndex], ignore_400: bool = True
    ) -> List[str]:
        if not is_iterable(objects):
            objects = [objects]

        unique_indexes = []
        for obj in objects:
            if (index := obj.get_index()) not in unique_indexes:
                # Create an index for every unique index
                try:
                    self.create_index(obj.__class__, index_name=index)
                except BadRequestError:
                    pass
                unique_indexes.append(index)

        return unique_indexes

    def refresh_index(
        self, index: ElasticIndex | str | Sequence[ElasticIndex] | Sequence[str]
    ) -> bool:
        """
        Refresh index.

        :param index: Index to refresh
        :return: Whether the operation was successful. If multiple indexes are specified,
        `True` will be returned only if every operation finished successfully
        """

        def _refresh(index_name):
            return not bool(
                self.execute(ElasticIndex.get_index_refresh_template(index_name))[
                    "_shards"
                ]["failed"]
            )

        # `str` is not considered iterable in this function by design
        if not is_iterable(index):
            index = [index]

        return all(
            [_refresh(i if isinstance(i, str) else i.get_static_index()) for i in index]
        )

    def save(
        self,
        objects: ElasticIndex | Sequence[ElasticIndex],
        create_indexes: bool = True,
        max_request_size: int = 99,
        refresh_after: bool = False,
    ) -> None:
        """
        Save one or more `ElasticIndex` subclass objects.

        :param objects: A single instance or a list of instances of classes, inherited from `ElasticIndex`
        :param create_indexes: Whether to create indexes if they don't exist (introduces overhead because before the insertion begins,
         a check request for every unique index will be sent)
        :param max_request_size: Max request size in MB. Note that Elastic limits the max request size to 100MB.
        :param refresh_after: Whether to run a manual refresh after the saving completes
        """
        if not is_iterable(objects):
            objects = [objects]

        if create_indexes:
            self.create_index_for(objects, ignore_400=True)

        documents_by_index: Dict[str, List[ElasticIndex]] = group_by_index(objects)
        for index, documents in documents_by_index.items():
            batches = get_batches_with_size(documents, max_request_size * 1024 * 1024)
            for batch in batches:
                self.execute(ElasticIndex.get_batch_create_request(batch))

            if refresh_after:
                self.refresh_index(index)
