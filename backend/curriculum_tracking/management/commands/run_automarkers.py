"""
example usage

python manage.py run_automarkers prod
python manage.py run_automarkers debug
python manage.py run_automarkers "Build your own website and host it on the web\!"

"""
from django.core.management.base import BaseCommand
import yaml
from pathlib import Path
import os
from curriculum_tracking.models import ContentItem
from core.models import Curriculum

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from curriculum_tracking.management.automarker_utils import (
    get_cards_needing_review,
    automark_project,
)

from curriculum_tracking.card_generation_helpers import get_ordered_content_items


CONFIG_PATH = Path(os.getenv("AUTO_MARKER_CONFIGURATION_REPO_PATH")) / "config.yaml"


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("mode", type=str, default="prod")
        parser.add_argument("curriculum", type=str, nargs="?")

    def handle(self, *args, **options):
        curriculum_name = options.get("curriculum")
        if curriculum_name:
            curriculum = Curriculum.objects.get(name=curriculum_name)
            content_items = [
                o.content_item for o in get_ordered_content_items(curriculum)
            ]

        with open(CONFIG_PATH, "r") as f:
            config = yaml.load(f, Loader)

        mode = options["mode"]
        assert mode in ["prod", "debug"]

        for item in [d for d in config if d["mode"] == mode]:
            print(item)
            content_item = ContentItem.objects.get(id=item["contentItemId"])
            if curriculum_name and content_item not in content_items:
                continue

            for card in get_cards_needing_review(
                content_item=content_item, flavours=item["flavours"]
            ):

                automark_project(
                    card.recruit_project, debug_mode=item["mode"] == "debug"
                )
