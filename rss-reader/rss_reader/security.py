"""
Module with RSS Reader security utils.
"""

import passlib.context


ALGORITHM = "HS256"
pwd_context = passlib.context.CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


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
