#!/usr/bin/env python
"""Django's command-line tool: python manage.py runserver | migrate | createsuperuser | makemigrations ..."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
