"""
Module with RSS API client.
"""

import logging
import urllib.parse
from typing import Any

import requests

from tg_bot import settings
from tg_bot.integrations import constants
from tg_bot.integrations import errors


class BaseClient:
    """Base client"""

    ENDPOINT = settings.RSS_API_URL
    DEFAULT_HEADERS = {}

    def _perform_request(
        self,
        url: str,
        method: str = "get",
        data: dict = None,
        headers: dict = None,
    ) -> Any:
        """
        Perform HTTP request to URL.

        Args:
            url (str): A URL.
            method (str): An HTTP method.
            data (dict): A data to send in request. Defaults to None.
            headers (dict): Request headers. Defaults to None.

        Returns:
            Any: a json-encoded content of response.
        """
        url = urllib.parse.urljoin(self.ENDPOINT, url)

        headers = headers or {}
        if self.DEFAULT_HEADERS:
            headers.update(self.DEFAULT_HEADERS)

        try:
            response = requests.request(
                method,
                url,
                data=data,
                headers=headers,
                timeout=constants.REQUESTS_TIMEOUT
            )
            response.raise_for_status()
        except (requests.RequestException, requests.HTTPError) as err:
            logging.error("Unable to perform request to '%s': %s", url, err)
            raise errors.Error("Unable to perform request")
        return response.json

    def get(self, url: str, headers: dict = None) -> Any:
        """Performs GET HTTP request to given URL."""
        return self._perform_request(url, method="get", headers=headers)

    def post(self, url: str, data: dict = None, headers: dict = None) -> Any:
        """Performs POST HTTP request to given URL with given data."""
        return self._perform_request(url, method="post", data=data,
                                     headers=headers)

    def put(self, url: str, data: dict = None, headers: dict = None) -> Any:
        """Performs PUT HTTP request to given URL with given data."""
        return self._perform_request(url, method="put", data=data,
                                     headers=headers)

    def delete(self, url: str, headers: dict = None):
        """Performs DELETE HTTP request to given URL."""
        return self._perform_request(url, method="delete", headers=headers)


class PostsClient(BaseClient):
    """Posts client."""

    def fetch_posts(self) -> list:
        """Fetch posts parsed from RSS feeds."""
        return self.get("/posts")


class FeedsClient(BaseClient):
    """RSS feeds client"""

    def add_feed(self, name: str, url: str) -> dict:
        """Add new RSS feed."""
        return self.post("/feeds", data={"name": name, "url": url})

    def remove_feed(self, feed_id: int) -> dict:
        """Remove RSS feed."""
        return self.delete(f"/feeds/{feed_id}")
