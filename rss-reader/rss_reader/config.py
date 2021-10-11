"""
Module with RSS reader settings.
"""

import pydantic
from pydantic.networks import AnyUrl


class Settings(pydantic.BaseSettings):
    """
    Class which contains app settings.
    """
    RSS_DB_URI: AnyUrl
    RSS_TASKS_QUEUE_URI: AnyUrl
    RSS_TASKS_RES_BACKEND_URI: AnyUrl
    RSS_PARSE_FEEDS_INTERVAL: int


settings = Settings()
