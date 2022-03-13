"""
Module which contains API schema definition for Tokens.
"""

import pydantic


class Token(pydantic.BaseModel):
    """
    Model used for token representation.
    """
    access_token: str
    token_type: str = "bearer"
