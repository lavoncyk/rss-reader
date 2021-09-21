import fastapi

from rss_reader.api import post
from rss_reader.api import rss_feed


app = fastapi.FastAPI()

app.include_router(post.router)
app.include_router(rss_feed.router)
