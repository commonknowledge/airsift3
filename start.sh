#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python /app/manage.py collectstatic --noinput
python /app/manage.py migrate

# Use PORT environment variable provided by Render, fallback to 5000 for local development
/usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:${PORT:-5000} --chdir=/app

