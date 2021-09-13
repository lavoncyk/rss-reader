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


settings = Settings()
