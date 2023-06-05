from pylastic.types import Text
from pylastic.indexes import ElasticIndex


class TextType(ElasticIndex):
    comment: Text(index=False)
    id: Text(match_only_text=True, meta={"description": "ID Field"})
    author: Text


def test_comment():
    assert TextType.get_mapping()["mappings"]["properties"]["comment"] == {
        "type": "text",
        "index": False,
    }


def test_id():
    assert TextType.get_mapping()["mappings"]["properties"]["id"] == {
        "type": "match_only_text",
        "meta": {"description": "ID Field"},
    }


def test_author():
    assert TextType.get_mapping()["mappings"]["properties"]["author"] == {
        "type": "text",
    }
