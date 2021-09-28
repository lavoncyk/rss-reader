FROM python:3.9-slim

# Install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

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
CMD ["/server-start.sh"]
