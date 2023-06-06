from unittest.mock import MagicMock, call

from pytest import fixture

from pylastic.client import ElasticClient
from pylastic.indexes import ElasticIndex


class Example(ElasticIndex):
    a: str
    b: int

    class Meta:
        index = "example"


class DynamicIndexExample(ElasticIndex):
    a: str
    b: int

    def get_index(self):
        return "dynamic-index"


@fixture()
def client(monkeypatch):
    elastic = MagicMock()
    client = ElasticClient(
        host="localhost", port=123, username="user", password="password"
    )
    client.es_client = elastic
    return client


def test_create_index_for(client):
    client.create_index_for(Example(a="a", b=3))

    client.es_client.perform_request.assert_called_with(
        method="PUT",
        path="/example",
        params=None,
        headers={"accept": "application/json", "content-type": "application/json"},
        body={
            "mappings": {
                "properties": {"a": {"type": "text"}, "b": {"type": "integer"}}
            },
            "settings": {
                "number_of_shards": 1,
                "codec": "default",
                "number_of_replicas": 1,
            },
        },
    )


def test_create_multiple_indexes(client):
    client.create_index_for([Example(a="a", b=3), Example(a="b", b=5)])

    client.es_client.perform_request.assert_called_with(  # noqa
        method="PUT",
        path="/example",
        params=None,
        headers={"accept": "application/json", "content-type": "application/json"},
        body={
            "mappings": {
                "properties": {"a": {"type": "text"}, "b": {"type": "integer"}}
            },
            "settings": {
                "number_of_shards": 1,
                "codec": "default",
                "number_of_replicas": 1,
            },
        },
    )
    assert (
        client.es_client.perform_request.call_count == 1
    ), "Multiple requests are made for one index"


def test_create_index_for_dynamic_index(client):
    client.create_index_for(DynamicIndexExample(a="a", b=3))

    client.es_client.perform_request.assert_called_with(
        method="PUT",
        path="/dynamic-index",
        params=None,
        headers={"accept": "application/json", "content-type": "application/json"},
        body={
            "mappings": {
                "properties": {"a": {"type": "text"}, "b": {"type": "integer"}}
            },
            "settings": {
                "number_of_shards": 1,
                "codec": "default",
                "number_of_replicas": 1,
            },
        },
    )


def test_create_multiple_indexes_for_dynamic_index(client):
    client.create_index_for(
        [
            Example(a="a", b=3),
            Example(a="b", b=5),
            DynamicIndexExample(a="a", b=3),
            DynamicIndexExample(a="c", b=7),
        ]
    )

    client.es_client.perform_request.assert_has_calls(
        [
            call(  # noqa
                method="PUT",
                path="/example",
                params=None,
                headers={
                    "accept": "application/json",
                    "content-type": "application/json",
                },
                body={
                    "mappings": {
                        "properties": {"a": {"type": "text"}, "b": {"type": "integer"}}
                    },
                    "settings": {
                        "number_of_shards": 1,
                        "codec": "default",
                        "number_of_replicas": 1,
                    },
                },
            )
        ]
    )
    client.es_client.perform_request.assert_called_with(
        method="PUT",
        path="/dynamic-index",
        params=None,
        headers={"accept": "application/json", "content-type": "application/json"},
        body={
            "mappings": {
                "properties": {"a": {"type": "text"}, "b": {"type": "integer"}}
            },
            "settings": {
                "number_of_shards": 1,
                "codec": "default",
                "number_of_replicas": 1,
            },
        },
    )
    assert (
        client.es_client.perform_request.call_count == 2
    ), "Multiple requests are made for one index"


def test_refresh(client):
    client.refresh_index(Example)
    client.es_client.perform_request.assert_called_with(
        method="POST",
        path="/example/_refresh",
        params=None,
        headers={"accept": "application/json", "content-type": "application/json"},
        body=None,
    )
