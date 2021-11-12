"""
Module with tests settings.
"""

import pydantic
from pydantic.networks import AnyUrl


class Settings(pydantic.BaseSettings):
    """
    Class which contains tests settings.
    """
    RSS_DB_URI: AnyUrl


settings = Settings()
