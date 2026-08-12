#!/usr/bin/env python
"""
manage.py হলো Django প্রজেক্টের "কমান্ড সেন্টার"।
টার্মিনালে তুমি এই ফাইলটা দিয়েই সব কমান্ড চালাবে, যেমন:
  python manage.py runserver        -> সার্ভার চালু করে (development server)
  python manage.py makemigrations   -> মডেল থেকে migration ফাইল বানায়
  python manage.py migrate          -> migration গুলো database এ apply করে
  python manage.py createsuperuser  -> admin panel এর জন্য user বানায়

এই ফাইলে সাধারণত হাত দিতে হয় না, Django নিজেই এটা বানায়।
"""
import os
import sys


def main():
    """Run administrative tasks."""
    # DJANGO_SETTINGS_MODULE বলে দেয় কোন settings.py ফাইলটা ব্যবহার হবে
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookapi.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
