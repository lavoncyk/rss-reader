FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl
# Install Poetry
RUN curl -sSL \
    https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | POETRY_HOME=/opt/poetry python  && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root --no-dev

COPY ./rss_reader ./rss_reader
COPY ./migrations ./migrations
COPY ./alembic.ini .

# Make /app/* available to be imported by Python globally to
# better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app

EXPOSE 8080

COPY ./scripts/server-start.sh /server-start.sh
RUN chmod +x /server-start.sh

# Run the start script, it will run prestart.sh
# and then will start Gunicorn with Uvicorn
ENTRYPOINT ["/server-start.sh"]
