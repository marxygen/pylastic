from dataclasses import is_dataclass
from typing import Optional

import pytest

from pylastic.indexes import ElasticIndex
from pylastic.types import GeoPoint, Text


class Example(ElasticIndex):
    a: str
    b: int
    g: GeoPoint
    c: Optional[str] = None

    class Meta:
        index = "example"


example_instance = Example(a="abc", b=3, g={"lat": 20, "lon": 30})


class CustomFieldExample(ElasticIndex):
    g: Text(match_only_text=True, meta={"description": "Dynamically defined field"})

    class Meta:
        index = "cfex"


def test_is_dataclass():
    assert is_dataclass(Example)


def test_validation():
    class TestGeo(ElasticIndex):
        point: GeoPoint
        optional_point: Optional[GeoPoint] = None

    TestGeo(point={"lat": 12, "lon": 20}).validate()
    TestGeo(
        point={"lat": 12, "lon": 20}, optional_point={"lat": 12, "lon": 20}
    ).validate()

    with pytest.raises(ValueError):
        TestGeo(point={"lat": "91", "lon": "10"}).validate()

    with pytest.raises(ValueError):
        TestGeo(point={"lat": "90", "lon": "181"}).validate()

    with pytest.raises(ValueError):
        TestGeo(
            point={"lat": "90", "lon": "180"}, optional_point={"lat": 12, "lon": 181}
        ).validate()


def test_get_fields_with_types():
    assert Example._get_fields_with_types() == {
        "a": str,
        "b": int,
        "c": str,
        "g": GeoPoint,
    }


def test_get_mapping():
    Example.Meta.id_field = "a"
    assert Example.id_field == "a"
    assert Example.get_mapping() == {
        "mappings": {
            "properties": {
                "b": {"type": "integer"},
                "c": {"type": "text"},
                "g": {"type": "geo_point"},
            }
        }
    }

    Example.Meta.id_field = "_id"
    assert Example.get_mapping() == {
        "mappings": {
            "properties": {
                "a": {"type": "text"},
                "b": {"type": "integer"},
                "c": {"type": "text"},
                "g": {"type": "geo_point"},
            }
        }
    }


def test_custom_field_mapping():
    assert CustomFieldExample.get_mapping() == {
        "mappings": {
            "properties": {
                "g": {
                    "type": "match_only_text",
                    "meta": {"description": "Dynamically defined field"},
                }
            }
        }
    }


def test_get_index():
    assert example_instance.get_index() == "example"


def test_empty_custom_id():
    Example.Meta.id_field = "c"
    with pytest.raises(ValueError):
        ei = Example(a="abc", b=3, g={"lat": 20, "lon": 30})
        assert ei.get_id() is None
        ei.validate()

    # If id field is not overridden, `None` is the accepted value
    Example.Meta.id_field = "_id"

    ei.validate()
    assert getattr(ei, "_id", None) is None
    assert ei.get_id() is None
