FROM python:3.9

WORKDIR /rss-reader

COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY ./rss_reader ./rss_reader
COPY ./migrations ./migrations
COPY ./alembic.ini .

EXPOSE 8080

CMD [ "uvicorn", "rss_reader.main:app", "--host", "0.0.0.0", "--port", "8080"]
