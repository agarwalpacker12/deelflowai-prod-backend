#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""

import os
import sys

def main():
    """Run administrative tasks."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'deelflowAI'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deelflowAI.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed in your virtual environment "
            "and that the environment is activated. Check PYTHONPATH and DJANGO_SETTINGS_MODULE."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()


