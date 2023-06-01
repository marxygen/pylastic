from dataclasses import is_dataclass
from typing import Optional

import pytest

from pylastic.indexes import ElasticIndex
from pylastic.types import GeoPoint


class Example(ElasticIndex):
    a: str
    b: int
    c: Optional[str]


def test_is_dataclass():
    assert is_dataclass(Example)


def test_geopoint():
    class TestGeo(ElasticIndex):
        point: GeoPoint
        optional_point: Optional[GeoPoint] = None

    TestGeo(point={'lat': 12, 'lon': 20}).validate()
    TestGeo(point={'lat': 12, 'lon': 20}, optional_point={'lat': 12, 'lon': 20}).validate()

    with pytest.raises(ValueError):
        TestGeo(point={'lat': "91", 'lon': "10"}).validate()

    with pytest.raises(ValueError):
        TestGeo(point={'lat': "90", 'lon': "181"}).validate()

    with pytest.raises(ValueError):
        TestGeo(point={'lat': "90", 'lon': "180"}, optional_point={'lat': 12, 'lon': 181}).validate()
