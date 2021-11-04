"""
Module with RSS Reader utils.
"""

from typing import Any, Callable, List, Optional
import functools
import re
import urllib.parse

import bs4
import requests


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
    string = string[:1].upper() + string[1:]
    return re.sub(
        r"[_][A-Za-z]",
        lambda pat: "" + pat.group(0)[1].upper(),
        string,
    )


def pipeline_each(data: List[Any], fns: List[Callable[[Any], Any]]) -> Any:
    """Pipeline each item from `data` through `fns` functions."""
    return functools.reduce(
        lambda a, x: list(map(x, a)),
        fns,
        data,
    )


def extract_icon_url(page_url: str) -> Optional[str]:
    """Extract icon URL from provided page.

    Args:
        page_url (str): A page URL from which extract an icon.

    Returns:
        Optional[str]: An icon URL or None.
    """

    def load_html(url: str) -> str:
        """Load HTML from URL."""
        return requests.get(url, verify=False, timeout=5).text

    def is_icon_tag(tag: dict) -> bool:
        """Check if tag contains icon."""
        return (
            "icon" in tag.get("rel", "") and
            tag.get("href", "")
        )

    html = load_html(page_url)
    soup = bs4.BeautifulSoup(html, features="lxml")
    link_tags = soup.findAll("link")
    icon_tags = [t for t in link_tags if is_icon_tag(t)]
    if not icon_tags:
        return None

    icon_tag, *_ = icon_tags
    return urllib.parse.urljoin(page_url, icon_tag["href"])
