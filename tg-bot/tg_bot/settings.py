"""
Module with Telegram Bot settings.
"""

import os
from typing import Any, Callable


def get_env_var(
    name: str,
    *,
    required: bool = False,
    default: Any = None,
    cast: Callable[[str], Any] = str,
) -> Any:
    """Get environment variable by name."""
    value = os.environ.get(name, default)
    if required and value is None:
        raise ValueError(f"The '{name}' environment variable is required!")
    return cast(value)


TG_BOT_TOKEN = get_env_var("TG_BOT_TOKEN", required=True)
RSS_API_URL = get_env_var("RSS_API_URL", required=True)
FETCH_UPDATES_INTERVAL = get_env_var(
    "FETCH_UPDATES_INTERVAL", cast=int, default=5
)
