from pylastic.request_template import RequestTemplate
import pytest

rt = RequestTemplate(query_params={"a": "value", "b": 123})


def test_query_params_generation():
    assert rt.get_query_params_string() == "a=value&b=123"


def test_is_template():
    assert RequestTemplate.is_template(rt) is True
    assert RequestTemplate.is_template([rt]) is True
    assert RequestTemplate.is_template((rt,)) is True
    assert RequestTemplate.is_template((rt, None)) is False
    assert RequestTemplate.is_template((rt, RequestTemplate)) is False


def test_build_template():
    assert RequestTemplate.build(rt) is rt
    assert RequestTemplate.build({"a": "b"}) == RequestTemplate(body={"a": "b"})
    assert RequestTemplate.build([{"a": "b"}, {"c": "d"}]) == [
        RequestTemplate(body={"a": "b"}),
        RequestTemplate(body={"c": "d"}),
    ]
    assert RequestTemplate.build([{"a": "b"}]) == [RequestTemplate(body={"a": "b"})]
    assert RequestTemplate.build("a=b") == RequestTemplate(query_params={"a": "b"})
    assert RequestTemplate.build(["a=b"]) == [RequestTemplate(query_params={"a": "b"})]
    assert RequestTemplate.build("?a=b") == RequestTemplate(query_params={"a": "b"})
    assert RequestTemplate.build(["?a=b"]) == [RequestTemplate(query_params={"a": "b"})]
    with pytest.raises(RuntimeError):
        assert RequestTemplate.build("&a=b") == RequestTemplate(query_params={"a": "b"})
