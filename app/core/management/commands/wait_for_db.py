"""
Django command to wait for the database to be available.
"""
import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = None
        while not db_up:
            try:
                db_up = connections['default']
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
