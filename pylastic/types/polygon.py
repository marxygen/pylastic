from pylastic.types.base import ElasticType


class Polygon(ElasticType):
    """
    Elastic Polygon type

    long.py
    """

    class Meta:
        type = "polygon"

    # TODO: fix construction from GeoJSON and `Location`
