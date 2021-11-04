"""
Module with tasks utils.
"""

from typing import NamedTuple, Optional, Tuple
from datetime import datetime
import time


def time_struct_2_datetime(
    time_struct: Optional[time.struct_time],
) -> Optional[datetime]:
    """Convert struct_time to datetime.

    Args:
        time_struct (Optional[time.struct_time]): A time struct to convert.

    Returns:
        Optional[datetime]: A converted value.
    """
    return (
        datetime.fromtimestamp(time.mktime(time_struct))
        if time_struct is not None
        else None
    )


class PostStub(NamedTuple):
    """Post stub."""
    title: str
    url: str
    published_at: datetime
    feed_id: int


class FeedStub(NamedTuple):
    """Feed stub."""
    id: int
    url: str
    parsed_at: datetime
    modified: Optional[datetime]
    etag: Optional[str]
    posts: Tuple[PostStub]
