from typing import Any, Optional

from pylastic.types.base import ElasticType
from pylastic.utils.coordinates import is_valid_longitude, is_valid_latitude


class GeoPoint(ElasticType):
    class Meta:
        type = "geo_point"

    @classmethod
    def get_valid_object(cls, value: Any) -> Optional[Any]:
        """
        Construct a GeoPoint
        https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html

        Check the order (lat, lon) vs (lon, lat)! Different geo field definition formats might have them in the different
        order!
        """
        lat, lon = None, None

        if isinstance(value, dict):
            # GeoJSON
            if value.get("type") == "Point" and isinstance(
                value.get("coordinates"), list
            ):
                lon, lat = value["coordinates"]

            if value.get("lat") and value.get("lon"):
                lat, lon = value["lat"], value["lon"]

        elif isinstance(value, list):
            lon, lat = value

        elif isinstance(value, str):
            if value.startswith("POINT"):
                # Well-Known Text POINT
                lon, lat = value[len("POINT") : -1].strip().strip("(").strip(")").split(
                    " "
                ) or [None, None]

            if not lon or not lat:
                lat, lon = value.replace(" ", "").split(",")

        if (
            not all([lat, lon])
            or not is_valid_longitude(float(lon))
            or not is_valid_latitude(float(lat))
        ):
            return None

        return value
