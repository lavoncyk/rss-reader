FROM python:3.6

WORKDIR /usr/src/rss-reader

COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY ./src/rss_reader ./rss_reader

EXPOSE 8080

CMD [ "uvicorn", "rss_reader.main:app", "--host", "0.0.0.0", "--port", "8080"]
