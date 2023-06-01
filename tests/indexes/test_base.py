from dataclasses import is_dataclass
from typing import Optional

from pylastic.indexes import ElasticIndex


class Test(ElasticIndex):
    a: str
    b: int
    c: Optional[str]


def test_is_dataclass():
    assert is_dataclass(Test)
