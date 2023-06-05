from pylastic.utils.iterables import is_iterable


def test_iterables():
    assert is_iterable([1, 2, 3]) is True
    assert is_iterable([]) is True
    assert is_iterable((1, 2, 3)) is True


def test_string():
    assert is_iterable('a') is False
    assert is_iterable(['a']) is True
