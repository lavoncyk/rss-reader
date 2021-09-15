#! /usr/bin/env bash
set -e

celery --app=rss_reader.worker worker \
    --loglevel=INFO \
    --concurrency=1 \
    --queues=main-queue \
