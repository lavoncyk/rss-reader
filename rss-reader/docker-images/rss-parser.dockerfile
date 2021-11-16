FROM python:3.9-slim

# Install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

COPY ./rss_reader ./rss_reader

# Make /app/* available to be imported by Python globally to
# better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app

COPY ./scripts/worker-start.sh /worker-start.sh
RUN chmod +x /worker-start.sh

ENTRYPOINT ["/worker-start.sh"]
