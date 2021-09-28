#! /usr/bin/env bash
set -e

# Run prestart.sh before starting server.
PRE_START_PATH=${PRE_START_PATH:-./rss_reader/prestart.sh}
echo "Running script $PRE_START_PATH"
. "$PRE_START_PATH"

uvicorn rss_reader.main:app \
    --host 0.0.0.0 \
    --port 8080
