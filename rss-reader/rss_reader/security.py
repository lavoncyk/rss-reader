"""
Module with RSS Reader security utils.
"""
from typing import Any, Optional
import datetime

import passlib.context
from jose import jwt

from rss_reader.config import settings


ALGORITHM = "HS256"
pwd_context = passlib.context.CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def create_access_token(
    subject: Any, *, expiration_delta: Optional[datetime.timedelta] = None
) -> str:
    """Create access token.

    Args:
        subject (Any): A subject to create token from.
        expiration_delta (Optional[datetime.timedelta): A token expiration
            time delta. If not passed, a default one will be used.

    Returns:
        str: An access token.
    """
    expiration_delta = (
        expiration_delta or
        datetime.timedelta(seconds=settings.ACCESS_TOKEN_EXP_SECONDS)
    )
    expires_at = datetime.datetime.utcnow() + expiration_delta
    to_encode = {"exp": expires_at, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, key=settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify that password matches with a hashed one.

    Args:
        password (str): A plain password.
        hashed_password (str): A hashed password.

    Returns:
        bool: True if passwords match and False otherwise.
    """
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get hash from password.

    Args:
        password (str): A password.

    Returns:
        str: A password hash.
    """
    return pwd_context.hash(password)
