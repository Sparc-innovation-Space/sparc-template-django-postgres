#!/bin/sh
# How SPARC Cloud starts the app (sparc.json "start_command"). Migrations first: if they fail, the app stops with a
# clear line and never becomes ready. Static files are collected into /tmp (the app runs as user 1000, not root).
set -u
python manage.py migrate_safely || { echo "MIGRATIONS FAILED - the app will not start (see the error above)." >&2; exit 1; }
python manage.py collectstatic --noinput --verbosity 0 || { echo "collectstatic failed" >&2; exit 1; }
exec gunicorn mysite.wsgi:application --bind "0.0.0.0:${PORT:-8080}" --workers 2 --access-logfile -
