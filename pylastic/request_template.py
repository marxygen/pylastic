from dataclasses import dataclass
from typing import List, Any

from pylastic.utils.iterables import is_iterable


@dataclass(kw_only=True)
class RequestTemplate:
    """
    A request template to be passed into `client.execute` function.
    Contains data that is to be sent to the ES.
    """

    query_params: dict = None
    body: dict = None
    headers: dict = None

    def get_query_params_string(self) -> str:
        if not self.query_params:
            return ""

        return "&".join([f"{key}={val}" for key, val in self.query_params.items()])

    @staticmethod
    def is_template(obj: Any) -> bool:
        if is_iterable(obj):
            return all(list(map(RequestTemplate.is_template, obj)))

        return isinstance(obj, RequestTemplate)

    @classmethod
    def build(
        cls,
        value: dict
        | str
        | List[dict]
        | List[str]
        | "RequestTemplate"
        | List["RequestTemplate"],
    ) -> "RequestTemplate" | List["RequestTemplate"]:
        """
        :param value: Data to convert into RequestTemplate.
        If it's a `dict`, the client assumes the data provided is `RequestTemplate.body`.
        If it's a string, the client assumes it's `RequestTemplate.query_params`

        :return: A RequestTemplate instance or a list of instances
        """
        if RequestTemplate.is_template(value):
            return value

        if not is_iterable(value):
            if isinstance(value, dict):
                return RequestTemplate(body=value)
            elif isinstance(value, str):
                try:
                    return RequestTemplate(
                        query_params=dict(
                            [e.split("=") for e in value.lstrip("?").split("&")]
                        )
                    )  # noqa
                except ValueError as e:
                    raise RuntimeError(
                        f"Invalid string provided as `query_params`: {value}"
                    ) from e
            else:
                raise ValueError(
                    f"Unknown template type: {value} ({type(value).__name__})"
                )

        else:
            return list(map(cls.build, value))
