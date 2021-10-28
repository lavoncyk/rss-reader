FROM python:3.9-slim

# Install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

COPY ./tg_bot ./tg_bot

# Make /app/* available to be imported by Python globally to
# better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app

ENTRYPOINT ["python"]
CMD ["tg_bot/bot.py"]
