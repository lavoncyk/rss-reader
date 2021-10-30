"""
Module with RSS reader settings.
"""

from typing import List, Union

import pydantic
from pydantic.networks import AnyUrl, AnyHttpUrl


class Settings(pydantic.BaseSettings):
    """
    Class which contains app settings.
    """

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", \
    # "http://localhost:8080", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @pydantic.validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, value: Union[str, List[str]]
    ) -> Union[List[str], str]:
        """Parse the `BACKEND_CORS_ORIGINS` value."""
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    RSS_DB_URI: AnyUrl
    RSS_TASKS_QUEUE_URI: AnyUrl
    RSS_TASKS_RES_BACKEND_URI: AnyUrl
    RSS_PARSE_FEEDS_INTERVAL: int


settings = Settings()
