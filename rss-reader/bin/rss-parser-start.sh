#! /usr/bin/env bash
set -e

celery --app=rss_reader.worker beat \
    --loglevel=INFO
