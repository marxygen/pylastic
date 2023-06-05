from pylastic.types.base import ElasticType


class Text(ElasticType):
    """
    Elastic Text type (can define `match_only_text` too)
    https://www.elastic.co/guide/en/elasticsearch/reference/8.8/text.html
    https://www.elastic.co/guide/en/elasticsearch/reference/8.8/text.html#match-only-text-field-type

    This is one of the classes that can be configured to optimize storage, see more details below.
    """

    class Meta:
        type = "text"  # NOTE: this may be overriden by `self._type` during class instantiation

    def __init__(self, match_only_text: bool = False, **kwargs):
        """
        Define a `text` (or `match_only_text` field)

        :param match_only_text: Whether to use `match_only_text` type.
        Trades scoring and efficiency for space efficiency. Use if you need to optimize disk space of your index.
        If `True`, other parameters passed into this method will be ignored.

        All other params are the same as in the documentation for `text` type:
        https://www.elastic.co/guide/en/elasticsearch/reference/8.8/text.html#text-params
        """
        super(Text, self).__init__()
        self.custom_args = kwargs

        if match_only_text:
            self._type = "match_only_text"
        else:
            self._type = 'text'

    def get_mapping(self) -> dict:
        mapping = {
            "type": self._type,
        }
        for optional_param in (
            "analyzer",
            "eager_global_ordinals",
            "fielddata",
            "fielddata_frequency_filter",
            "fields",
            "index",
            "index_options",
            "index_prefixes",
            "index_phrases",
            "norms",
            "position_increment_gap",
            "store",
            "search_analyzer",
            "search_quote_analyzer",
            "similarity",
            "term_vector",
            "meta",
        ):
            if (override := self.custom_args.get(optional_param)) is not None:
                mapping[optional_param] = override

        return mapping
