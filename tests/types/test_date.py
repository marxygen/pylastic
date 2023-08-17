from datetime import datetime, date

from pylastic.types import Date


def test_date_from_datetime():
    now = datetime.utcnow()
    assert Date.get_valid_object(now) == int(now.timestamp() * 1000)


def test_date_from_date():
    today = date.today()
    assert Date.is_valid_value(today, raise_exception=False) is True


def test_date_from_number():
    assert Date.get_valid_object(1234567) == 1234567
    assert Date.get_valid_object(1234567.634) == 1234567


def test_date_from_string():
    assert Date.get_valid_object("1234567") == 1234567
    assert Date.get_valid_object("1234567.634") is None
