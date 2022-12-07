"""
example usage

python manage.py run_automarker "simple-calculator part 1" ""
python manage.py run_automarker "Person" ""
python manage.py run_automarker "password-checker" ""
"""
from django.core.management.base import BaseCommand
import yaml
from pathlib import Path
import os
from curriculum_tracking.models import ContentItem

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from curriculum_tracking.management.automarker_utils import (
    get_cards_needing_review,
    automark_card,
)


CONFIG_PATH = Path(os.getenv("AUTO_MARKER_CONFIGURATION_REPO_PATH")) / "config.yaml"


class Command(BaseCommand):
    def add_arguments(self, parser):

        parser.add_argument("mode", type=str, default="prod")

    def handle(self, *args, **options):
        with open(CONFIG_PATH, "r") as f:
            config = yaml.load(f, Loader)

        mode = options["mode"]
        assert mode in ["prod", "debug"]

        for item in [d for d in config if d["mode"] == mode]:
            print(item)
            content_item = ContentItem.objects.get(id=item["contentItemId"])

            for card in get_cards_needing_review(content_item=content_item):
                automark_card(card, debug_mode=item["mode"] == "debug")
