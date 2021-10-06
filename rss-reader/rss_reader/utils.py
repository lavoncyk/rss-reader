"""
Module with RSS Reader utils.
"""

import functools
import re
from typing import Any, Callable, List


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


def pipeline_each(data: List[Any], fns: List[Callable[[Any], Any]]):
    """Pipeline each item from `data` through `fns` functions."""
    return functools.reduce(
        lambda a, x: list(map(x, a)),
        fns,
        data,
    )
