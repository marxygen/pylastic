def is_valid_latitude(latitude: float) -> bool:
    """
    Check that a given value is within [-90; 90] degree range
    """
    return -90 <= latitude <= 90


def is_valid_longitude(longitude: float) -> bool:
    """
    Check that a given value is within [-180; 180] degree range
    """
    return -180 <= longitude <= 180
