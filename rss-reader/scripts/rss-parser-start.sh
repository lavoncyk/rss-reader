#! /usr/bin/env bash
set -e

alembic upgrade head

celery --app=rss_reader.workers.app worker \
    --beat \
    --loglevel=INFO
