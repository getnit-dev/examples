"""Basic tests for helper utilities."""

from utils.helpers import slugify, deep_merge


def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"
    assert slugify("  foo  bar  ") == "foo-bar"


def test_deep_merge_simple():
    base = {"a": 1, "b": 2}
    override = {"b": 3, "c": 4}
    result = deep_merge(base, override)
    assert result == {"a": 1, "b": 3, "c": 4}
