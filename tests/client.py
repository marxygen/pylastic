from unittest.mock import MagicMock

from pytest import fixture

from pylastic.client import ElasticClient


@fixture()
def client(monkeypatch):
    elastic = MagicMock()
    client = ElasticClient(host='localhost', port=123, username='user', password='password')
    client._client = elastic
    return client



