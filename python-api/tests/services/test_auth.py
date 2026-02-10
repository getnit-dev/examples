"""Example tests to establish project patterns.

These demonstrate the testing style that nit should follow.
"""

import pytest

from src.api.services.auth import hash_password, verify_password


def test_hash_password_returns_tuple():
    """Test that hash_password returns a tuple of hash and salt."""
    password = "test_password123"
    result = hash_password(password)

    assert isinstance(result, tuple)
    assert len(result) == 2
    pwd_hash, salt = result
    assert isinstance(pwd_hash, str)
    assert isinstance(salt, str)


def test_hash_password_with_custom_salt():
    """Test hashing with a provided salt."""
    password = "test_password123"
    custom_salt = "custom_salt_value"

    pwd_hash, salt = hash_password(password, custom_salt)

    assert salt == custom_salt
    assert len(pwd_hash) > 0


def test_verify_password_correct():
    """Test verifying a correct password."""
    password = "test_password123"
    pwd_hash, salt = hash_password(password)

    assert verify_password(password, pwd_hash, salt) is True


def test_verify_password_incorrect():
    """Test verifying an incorrect password."""
    password = "test_password123"
    wrong_password = "wrong_password456"
    pwd_hash, salt = hash_password(password)

    assert verify_password(wrong_password, pwd_hash, salt) is False
