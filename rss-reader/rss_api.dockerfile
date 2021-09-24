FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY ./rss_reader ./rss_reader
COPY ./migrations ./migrations
COPY ./alembic.ini .

EXPOSE 8080

COPY ./scripts/rss-api-start.sh /rss-api-start.sh
RUN chmod +x /rss-api-start.sh

CMD ["bash", "/rss-api-start.sh"]
