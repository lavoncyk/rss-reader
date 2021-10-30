"""
Module with app configuring logic.
"""

import fastapi
from fastapi.middleware import cors

from rss_reader.api import post
from rss_reader.api import rss_feed
from rss_reader.config import settings


app = fastapi.FastAPI()

app.include_router(post.router)
app.include_router(rss_feed.router)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
