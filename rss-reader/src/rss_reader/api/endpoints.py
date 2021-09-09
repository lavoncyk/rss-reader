"""
Module which contains API endpoints.
"""

from typing import List

import fastapi

from rss_reader import schemas


router = fastapi.APIRouter(
    prefix="/feeds",
    tags=["feeds"],
)


@router.get("/", response_model=List[schemas.RssFeed])
async def read_feeds():
    """
    Retrieve RSS feeds.
    """


@router.post("/", response_model=schemas.RssFeed)
async def create_feed(feed: schemas.RssFeedCreate):
    """
    Create new RSS feed.
    """


@router.put("/{feed_id}", response_model=schemas.RssFeed)
async def update_feed(feed_id: int, feed: schemas.RssFeedUpdate):
    """
    Update RSS feed.
    """


@router.get("/{feed_id}", response_model=schemas.RssFeed)
async def read_feed(feed_id: int):
    """
    Read RSS feed.
    """


@router.delete("/{feed_id}", response_model=schemas.RssFeed)
async def delete_feed(feed_id: int):
    """
    Delete RSS feed.
    """
