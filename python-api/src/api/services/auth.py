"""Authentication service functions.

These functions are intentionally left untested for nit to generate tests.
"""

import hashlib
import secrets
from datetime import UTC, datetime, timedelta


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """Hash a password with a salt."""
    if salt is None:
        salt = secrets.token_hex(16)

    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return pwd_hash.hex(), salt


def verify_password(password: str, hashed: str, salt: str) -> bool:
    """Verify a password against its hash."""
    pwd_hash, _ = hash_password(password, salt)
    return pwd_hash == hashed


def generate_token(length: int = 32) -> str:
    """Generate a random token."""
    return secrets.token_urlsafe(length)


def is_token_expired(issued_at: datetime, expiry_hours: int = 24) -> bool:
    """Check if a token has expired."""
    expiry_time = issued_at + timedelta(hours=expiry_hours)
    return datetime.now(UTC) > expiry_time


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
