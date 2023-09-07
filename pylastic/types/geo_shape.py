from pylastic.types.base import ElasticType


class Geoshape(ElasticType):
    """
    Elastic geo_shape type

    https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html
    """

    class Meta:
        type = "geo_shape"

    # TODO: fix construction from GeoJSON and `Location`
