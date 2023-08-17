import random
from itertools import chain
from math import ceil

from pylastic.utils.iterables import is_iterable, get_batches_with_size
from pylastic.utils.size import full_size_of


def test_iterables():
    assert is_iterable([1, 2, 3]) is True
    assert is_iterable([]) is True
    assert is_iterable((1, 2, 3)) is True


def test_string():
    assert is_iterable("a") is False
    assert is_iterable(["a"]) is True


def test_get_batches_with_size():
    objects = [random.randint(1, 10**10) for _ in range(random.randint(100, 1_000))]
    total_size = full_size_of(objects)

    expected_batches = random.randint(1, 10)
    batch_size = ceil(total_size / expected_batches)
    assert (
        0
        <= abs(len(get_batches_with_size(objects, batch_size)) - expected_batches)
        <= 1
    )
