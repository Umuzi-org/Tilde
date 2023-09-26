from django.core.management.base import BaseCommand
from automarker_app.lib.marker import get_all_marker_configs
from automarker_app.lib.constants import CONFIG_STATUS_DEBUG, CONFIG_STATUS_PRODUCTION
from automarker_app.lib.marker import mark_project, get_steps_final_status

from ..utils import print_steps_result
import os

# System call
os.system("")


# Class of different styles
class style:
    GREEN = "\033[32m"
    WHITE = "\033[37m"
    RED = "\033[31m"


class Command(BaseCommand):
    def handle(self, *args, **options):
        good_configs = []
        bad_configs = []
        for config in get_all_marker_configs():
            if config.status in [
                CONFIG_STATUS_DEBUG,
                CONFIG_STATUS_PRODUCTION,
            ]:
                print(style.WHITE, "\n-------------------------\n")
                print(
                    style.WHITE,
                    "CHECKING:",
                    config.title,
                    config.flavours,
                    config.content_item_id,
                )
                print(style.WHITE, "\n-------------------------\n")
                try:
                    steps = mark_project(
                        content_item_id=config.content_item_id,
                        flavours=config.flavours[0],
                        self_test=True,
                        fail_fast=True,
                    )

                    if len(steps) == len(config.steps):
                        good_configs.append(
                            [
                                config.title,
                                config.flavours,
                                config.content_item_id,
                            ]
                        )
                    # os.system(
                    #     f"python manage.py check_project_configuration {config.content_item_id} {config.flavours[0][0]}"
                    # )

                except Exception as e:
                    bad_configs.append(
                        [config.title, config.flavours, config.content_item_id, e]
                    )
        for config in good_configs:
            print(style.GREEN, "\n-------------------------\n")
            print(style.GREEN, "PASS:", config)

        for config in bad_configs:
            print(style.RED, "\n-------------------------\n")
            print(
                style.RED,
                "FAIL:",
                config[:-1],
            )
            print()
            print(style.RED, "ERROR:", config[-1])
