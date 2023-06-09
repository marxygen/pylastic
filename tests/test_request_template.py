from pylastic.request_template import RequestTemplate
import pytest

rt = RequestTemplate(query_params={"a": "value", "b": 123}, path="/a/b/")


def test_query_params_generation():
    assert rt.get_query_params_string() == "a=value&b=123"


def test_is_template():
    assert RequestTemplate.is_template(rt) is True
    assert RequestTemplate.is_template([rt]) is True
    assert RequestTemplate.is_template((rt,)) is True
    assert RequestTemplate.is_template((rt, None)) is False
    assert RequestTemplate.is_template((rt, RequestTemplate)) is False


def test_to_kwargs():
    assert rt.to_kwargs() == {
        "method": "GET",
        "path": "/a/b/",
        "params": {"a": "value", "b": 123},
        "headers": {"accept": "application/json", "content-type": "application/json"},
        "body": None,
    }
