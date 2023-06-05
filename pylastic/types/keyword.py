from pylastic.types.base import ElasticType


class Keyword(ElasticType):
    """
    Elastic Keyword type
    https://www.elastic.co/guide/en/elasticsearch/reference/8.8/keyword.html

    Can be `keyword`, `constant_keyword` or `wildcard`
    """

    class Meta:
        type = "keyword"  # NOTE: this may be overriden by `self._type` during class instantiation

    def __init__(
        self, constant_keyword: bool = False, wildcard: bool = False, **kwargs
    ):
        """
        Define a `keyword` (or `constant_keyword` or `wildcard` field)

        :param constant_keyword: Whether to use `constant_keyword` type (always contains the same value)
        :param wildcard: Whether to use `wildcard` type (For unstructured machine-generated content.
        The wildcard type is optimized for fields with large values or high cardinality.)

        All other params are the same as in the documentation for `keyword` type:
        https://www.elastic.co/guide/en/elasticsearch/reference/8.8/keyword.html#keyword-params
        """
        super(Keyword, self).__init__()
        self.custom_args = kwargs

        if all([constant_keyword, wildcard]):
            raise RuntimeError(
                f"Unable to set `constant_keyword` and `wildcard` at the same time!"
            )

        if constant_keyword:
            self._type = "constant_keyword"
        elif wildcard:
            self._type = "wildcard"
        else:
            self._type = "keyword"

    def get_mapping(self) -> dict:
        mapping = {
            "type": self._type,
        }
        for optional_param in (
            "doc_values",
            "eager_global_ordinals",
            "fields",
            "ignore_above",
            "index",
            "index_options",
            "norms",
            "meta",
            "null_value",
            "on_script_error",
            "script",
            "store",
            "similarity",
            "normalizer",
            "split_queries_on_whitespace",
            "time_series_dimension",
        ):
            if (override := self.custom_args.get(optional_param)) is not None:
                mapping[optional_param] = override

        return mapping
