"""python manage.py migrate_safely — `migrate`, but only one copy of the app at a time (Postgres advisory lock).
Used by bin/start.sh on every start; when nothing is new it just says "No migrations to apply"."""
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

MIGRATION_LOCK = 4209


class Command(BaseCommand):
    help = "Run migrate while holding a database lock."

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_lock(%s)", [MIGRATION_LOCK])
        try:
            call_command("migrate", interactive=False)
        finally:
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_advisory_unlock(%s)", [MIGRATION_LOCK])
