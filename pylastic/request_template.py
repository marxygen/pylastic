from dataclasses import dataclass
from typing import List, Any

from pylastic.utils.iterables import is_iterable


@dataclass(kw_only=True)
class RequestTemplate:
    """
    A request template to be passed into `client.execute` function.
    Contains data that is to be sent to the ES.
    """

    path: str
    query_params: dict = None
    body: dict = None
    headers: dict = None
    method: str = 'GET'

    def get_query_params_string(self) -> str:
        if not self.query_params:
            return ""

        return "&".join([f"{key}={val}" for key, val in self.query_params.items()])

    @staticmethod
    def is_template(obj: Any) -> bool:
        if is_iterable(obj):
            return all(list(map(RequestTemplate.is_template, obj)))

        return isinstance(obj, RequestTemplate)

    def to_kwargs(self) -> dict:
        """
        Transform this RequestTemplate to kwargs that are recognized by `elasticsearch.perform_request`

        :return: Dictionary of kwargs
        """
        return {
            'method': self.method,
            'path': self.path.rstrip('?'),
            'params': self.query_params,
            'headers': self.headers,
            'body': self.body
        }
