#! /usr/bin/env bash
set -e

celery --app=rss_reader.worker worker \
    --beat \
    --loglevel=INFO
