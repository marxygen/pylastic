from pylastic.types import GeoPoint


def test_geojson():
    assert GeoPoint.is_valid_value({
        "type": "Point",
        "coordinates": [-71.34, 41.12]
    }, raise_exception=False) is True

    # If we specified (lat, lon)
    assert GeoPoint.is_valid_value({
        "type": "Point",
        "coordinates": [-71.34, 141.12]
    }, raise_exception=False) is False


def test_WKTP():
    assert GeoPoint.is_valid_value('POINT (-171.34 41.12)', raise_exception=False) is True
    assert GeoPoint.is_valid_value('POINT (-71.34 141.12)', raise_exception=False) is False
    assert GeoPoint.is_valid_value('POINT (-71.34141.12)', raise_exception=False) is False
    assert GeoPoint.is_valid_value('POINT (-71.34 )', raise_exception=False) is False


def test_latlon_object():
    assert GeoPoint.is_valid_value({'lat': 14.3535, 'lon': 128.4}, raise_exception=False) is True
    assert GeoPoint.is_valid_value({'latitude': 14.3535, 'lon': 128.4}, raise_exception=False) is False
    assert GeoPoint.is_valid_value({'lat': 14.3535, 'longitude': 128.4}, raise_exception=False) is False
    assert GeoPoint.is_valid_value({'lat': 14.3535}, raise_exception=False) is False
    assert GeoPoint.is_valid_value({'lat': 143.3535, 'lon': 18.4}, raise_exception=False) is False


def test_lonlat_list():
    assert GeoPoint.is_valid_value([124.35, 45.34]) is True
    assert GeoPoint.is_valid_value([24.35, 145.34], raise_exception=False) is False
    assert GeoPoint.is_valid_value([24.35], raise_exception=False) is False


def test_latlon_string():
    assert GeoPoint.is_valid_value("45.34, 124.43") is True
    assert GeoPoint.is_valid_value("145.34, 14.43", raise_exception=False) is False
