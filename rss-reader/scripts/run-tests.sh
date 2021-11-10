#! /usr/bin/env bash
set -e

# Run migrations
alembic upgrade head

# Run tests
pytest
