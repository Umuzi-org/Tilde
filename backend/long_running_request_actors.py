"""
These are dramatiq actors

See https://dramatiq.io/guide.html
"""
import dramatiq


@dramatiq.actor
def test_long_running_request():
    import os

    os.system("python manage.py active_user_count")
