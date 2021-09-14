"""
Module with RSS Reader utils.
"""

import re


def underscore_from_camelcase(string: str) -> str:
    """Convert `string` from camelcase to underscore."""
    string = string[:1].lower() + string[1:]
    return re.sub(
        r"[A-Z]",
        lambda pat: "_" + pat.group(0).lower(),
        string,
    )


def camelcase_from_underscore(string: str) -> str:
    """Convert `string` from underscore to camelcase."""
    string = string[:1].lower() + string[1:]
    return re.sub(
        r"[_][A-Za-z]",
        lambda pat: "" + pat.group(0)[1].upper(),
        string,
    )
