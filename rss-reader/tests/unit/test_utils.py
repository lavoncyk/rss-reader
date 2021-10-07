"""Module with utils tests."""

from typing import Any, Dict

import pytest

from rss_reader import utils


@pytest.mark.parametrize(
    "string,expected",
    [
        ("FooBarBuzz", "foo_bar_buzz"),
        ("fooBarBuzz", "foo_bar_buzz"),
        ("Foo", "foo"),
        ("", ""),
    ]
)
def test_underscore_from_camelcase(string, expected):
    """Test the `underscore_from_camelcase` util."""
    result = utils.underscore_from_camelcase(string)
    assert result == expected


@pytest.mark.parametrize(
    "string,expected",
    [
        ("foo_bar_buzz", "FooBarBuzz"),
        ("Foo_bar_buzz", "FooBarBuzz"),
        ("foo_Bar_buzz", "FooBarBuzz"),
        ("foo_bar_Buzz", "FooBarBuzz"),
        ("Foo_Bar_Buzz", "FooBarBuzz"),
        ("Foo", "Foo"),
        ("", ""),
    ]
)
def test_camelcase_from_underscore(string, expected):
    """Test the `camelcase_from_underscore` util."""
    result = utils.camelcase_from_underscore(string)
    assert result == expected


def test_pipeline_each():
    """Test the `pipeline_each` util."""
    data = [{"foo": 1}, {"bar ": 2}, {" buzz": 3}]

    def capitalize_keys(d: Dict[str, Any]) -> Dict[str, Any]:
        return {k.capitalize(): v for k, v in d.items()}

    def strip_keys(d: Dict[str, Any]) -> Dict[str, Any]:
        return {k.strip(): v for k, v in d.items()}

    result = utils.pipeline_each(
        data,
        [
            strip_keys,
            capitalize_keys,
        ])

    assert result == [{"Foo": 1}, {"Bar": 2}, {"Buzz": 3}]
