"""
Similar to the run_automarkers script but it marks things that aren't linked to cards. It also needs to be a bit more careful about how the database is queried because there will be something like 10000 users. 

This script might not actually work well in the long run, it'll be fine for smaller scale UX testing at least

python manage.py run_zmc_automarkers debug "Build your own website and host it on the web\!"

"""
from django.core.management.base import BaseCommand
from pathlib import Path
import yaml
import os
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import ContentItem, RecruitProject
from core.models import Curriculum
from curriculum_tracking.management.automarker_utils import (
    automark_project,
)

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

CONFIG_PATH = Path(os.getenv("AUTO_MARKER_CONFIGURATION_REPO_PATH")) / "config.yaml"


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("mode", type=str, default="prod", nargs="?")
        parser.add_argument("curriculum", type=str)

    def handle(self, *args, **options):
        with open(CONFIG_PATH, "r") as f:
            config = yaml.load(f, Loader)

        mode = options["mode"]
        assert mode in ["prod", "debug"]

        curriculum_name = options.get("curriculum")
        curriculum = Curriculum.objects.get(name=curriculum_name)
        content_and_flavours = list(get_ordered_content_items(curriculum))

        for d in config:
            print()
            print(d)
            if d["mode"] != mode:
                continue

            match = False
            for content_and_flavour in content_and_flavours:
                if content_and_flavour.content_item.id != int(d["contentItemId"]):
                    continue
                print("content match, checking flavours")

                print(sorted(content_and_flavour.flavours))
                print(sorted(d["flavours"]))
                print(sorted(content_and_flavour.flavours) == sorted(d["flavours"]))

                if sorted(content_and_flavour.flavours) != sorted(d["flavours"]):
                    continue
                match = True
                break

            if not match:
                continue

            # now we have to get the projects that match the config
            projects = (
                RecruitProject.objects.filter(
                    content_item=content_and_flavour.content_item
                )
                .filter(recruit_users__active=True)
                .filter(review_request_time__isnull=False)
                .filter(complete_time__isnull=True)
            )
            for project in projects:
                if not project.flavours_match(d["flavours"]):
                    continue
                # we have something to mark!!

                automark_project(project, mode)
