#! /usr/bin/env bash
set -e

# Run migrations
alembic upgrade head

# Load initial data
python ./rss_reader/init_data.py
