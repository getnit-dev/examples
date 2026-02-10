"""Data validation functions.

These functions are intentionally left untested for nit to generate tests.
"""

import re
from typing import Any


def validate_username(username: str) -> bool:
    """Validate username format."""
    if len(username) < 3 or len(username) > 20:
        return False
    return re.match(r'^[a-zA-Z0-9_-]+$', username) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None


def validate_age(age: int) -> bool:
    """Validate age is within reasonable range."""
    return 0 < age < 150


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """Validate password meets strength requirements."""
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain an uppercase letter")
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain a lowercase letter")
    if not re.search(r'\d', password):
        errors.append("Password must contain a digit")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain a special character")

    return len(errors) == 0, errors


def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from input."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove script tags
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
    return text.strip()


def validate_json_structure(data: dict[str, Any], required_fields: list[str]) -> bool:
    """Validate JSON has required fields."""
    return all(field in data for field in required_fields)
