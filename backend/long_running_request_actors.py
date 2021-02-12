"""
These are dramatiq actors

See https://dramatiq.io/guide.html
"""

import dramatiq
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()


@dramatiq.actor
def test_long_running_request():

    from core.models import User

    count = User.objects.filter(active=True).count()
    print(f"Active users: {count}")
