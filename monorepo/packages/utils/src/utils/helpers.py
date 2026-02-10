"""Utility helper functions with untested edge cases."""

from __future__ import annotations

import re
from typing import Any


def slugify(text: str) -> str:
    """Convert a string to a URL-friendly slug.

    Untested edge cases: empty string, all-whitespace, unicode characters,
    consecutive hyphens, leading/trailing hyphens, very long strings.
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    text = text.strip("-")
    return text


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep-merge two dictionaries, with override taking precedence.

    Untested edge cases: nested dicts, conflicting types (dict vs non-dict),
    empty dicts, None values, lists as values.
    """
    result = base.copy()
    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def flatten_dict(
    d: dict[str, Any], parent_key: str = "", sep: str = "."
) -> dict[str, Any]:
    """Flatten a nested dictionary into dot-separated keys.

    Untested: no tests at all. Edge cases: empty dict, deeply nested,
    keys containing the separator, non-string keys, mixed nesting.
    """
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
