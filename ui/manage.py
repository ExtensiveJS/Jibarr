#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ui.settings')
    try:
        from django.core.management import execute_from_command_line
        #from django_celery_beat.models import PeriodicTask
        #PeriodicTask.objects.update(last_run_at=None)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print('Starting on http://localhost:8125/jibarr')
    execute_from_command_line(sys.argv)
    