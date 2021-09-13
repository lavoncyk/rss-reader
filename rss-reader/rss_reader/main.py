import fastapi

from rss_reader.api import endpoints


app = fastapi.FastAPI()

app.include_router(endpoints.router)
