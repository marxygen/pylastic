from pylastic.types import Keyword
from pylastic.indexes import ElasticIndex
import pytest


class KeywordType(ElasticIndex):
    id: Keyword()
    type: Keyword(constant_keyword=True)
    uuid: Keyword(wildcard=True, meta={'description': "UUID"})


def test_id():
    assert KeywordType.get_mapping()["mappings"]["properties"]["id"] == {
        "type": "keyword",
    }


def test_type():
    assert KeywordType.get_mapping()["mappings"]["properties"]["type"] == {
        "type": "constant_keyword",
    }


def test_uuid():
    assert KeywordType.get_mapping()["mappings"]["properties"]["uuid"] == {
        "type": "wildcard",
        "meta": {
            "description": "UUID"
        }
    }


def test_constant_and_wildcard():
    with pytest.raises(RuntimeError):
        class InvalidIndex(ElasticIndex):
            field: Keyword(constant_keyword=True, wildcard=True)
