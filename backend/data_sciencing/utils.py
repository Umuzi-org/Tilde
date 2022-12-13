import os
import sys
import django
from pathlib import Path


def setup_database_connections():
    tilde_backend_path = str(Path(os.getcwd()).parent)
    sys.path.append(tilde_backend_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()
