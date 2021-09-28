#! /usr/bin/env bash
set -e

celery --app=rss_reader.workers.app worker \
    --beat \
    --loglevel=INFO
