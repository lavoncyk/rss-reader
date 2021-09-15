#! /usr/bin/env bash
set -e

uvicorn rss_reader.main:app \
    --host 0.0.0.0 \
    --port 8080
