from pylastic.utils.coordinates import is_valid_latitude, is_valid_longitude


def test_latitude():
    assert is_valid_latitude(10.545) is True
    assert is_valid_latitude(100.1455) is False
    assert is_valid_latitude(90) is True
    assert is_valid_latitude(-91.5715) is False
    assert is_valid_latitude(-10.9) is True


def test_longitude():
    assert is_valid_longitude(10.354) is True
    assert is_valid_longitude(-10.354) is True
    assert is_valid_longitude(-180.354) is False
    assert is_valid_longitude(-180.000) is True
    assert is_valid_longitude(180.000) is True
    assert is_valid_longitude(181.340) is False
