"""General helper functions.

These functions are intentionally left untested for nit to generate tests.
"""

from datetime import UTC, datetime
from typing import Any


def format_date(dt: datetime, format_str: str = "%Y-%m-%d") -> str:
    """Format a datetime object to string."""
    return dt.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> datetime:
    """Parse a string to datetime object."""
    return datetime.strptime(date_str, format_str)


def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage."""
    if total == 0:
        return 0.0
    return (part / total) * 100


def chunk_list(items: list[Any], chunk_size: int) -> list[list[Any]]:
    """Split a list into chunks."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def flatten_dict(d: dict[str, Any], parent_key: str = '', sep: str = '.') -> dict[str, Any]:
    """Flatten a nested dictionary."""
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def remove_none_values(d: dict[str, Any]) -> dict[str, Any]:
    """Remove None values from dictionary."""
    return {k: v for k, v in d.items() if v is not None}


def get_utc_now() -> datetime:
    """Get current UTC time."""
    return datetime.now(UTC)
