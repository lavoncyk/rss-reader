FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY ./rss_reader ./rss_reader
COPY ./migrations ./migrations
COPY ./alembic.ini .

COPY ./scripts/rss-parser-start.sh /rss-parser-start.sh
RUN chmod +x /rss-parser-start.sh

CMD ["bash", "/rss-parser-start.sh"]
