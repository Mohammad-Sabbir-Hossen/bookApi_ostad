"""
Production server (gunicorn ইত্যাদি) এই ফাইল ব্যবহার করে Django app চালায়।
সাধারণত এখানে হাত দেওয়া লাগে না।
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookapi.settings')
application = get_wsgi_application()
