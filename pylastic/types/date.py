from datetime import date, datetime
from time import mktime
from typing import Any, Optional

from pylastic.types.base import ElasticType


class Date(ElasticType):
    class Meta:
        type = "date"

    @classmethod
    def get_valid_object(cls, value: Any) -> Optional[Any]:
        """
        Construct a Date
        https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html

        Returns the `date` value as a timestamp in milliseconds
        """
        if isinstance(value, datetime):
            return int(value.timestamp() * 1_000)

        if isinstance(value, date):
            return mktime(value.timetuple())

        if isinstance(value, (float, int)):
            return int(value)

        if isinstance(value, str) and value.isdigit():
            return int(value)

        return None
