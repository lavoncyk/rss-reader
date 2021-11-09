"""
Module with app configuring logic.
"""

import fastapi
from fastapi.middleware import cors

from rss_reader.api import api
from rss_reader.api.crud import exceptions as crud_exceptions
from rss_reader.config import settings


app = fastapi.FastAPI()

app.include_router(api.api_router)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(crud_exceptions.CrudError)
async def crud_exception_handler(_, exc: crud_exceptions.CrudError):
    return fastapi.responses.JSONResponse(
        status_code=400,
        content={"message": exc.details}
    )
