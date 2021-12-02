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

COPY ./tg_bot ./tg_bot

# Make /app/* available to be imported by Python globally to
# better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app

ENTRYPOINT ["python"]
CMD ["tg_bot/bot.py"]
