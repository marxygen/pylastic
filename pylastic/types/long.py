from pylastic.types.base import ElasticType


class Long(ElasticType):
    """
    Elastic Long type

    https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html
    """

    class Meta:
        type = "long"
