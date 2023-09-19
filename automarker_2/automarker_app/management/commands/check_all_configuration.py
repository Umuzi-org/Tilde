from django.core.management.base import BaseCommand
from automarker_app.lib.marker import get_all_marker_configs
from automarker_app.lib.constants import CONFIG_STATUS_DEBUG, CONFIG_STATUS_PRODUCTION
from automarker_app.lib.marker import mark_project


# TODO: FIX adapters missing in some configs
class Command(BaseCommand):
    def handle(self, *args, **options):
        debug_and_prod_configs = []
        all_configs = list(get_all_marker_configs())
        # count = 0
        for config in all_configs:
            if config.status in [CONFIG_STATUS_DEBUG, CONFIG_STATUS_PRODUCTION]:
                try:
                    # print(config.flavours)
                    steps = mark_project(
                        content_item_id=config.content_item_id,
                        flavours=config.flavours[0],
                        self_test=True,
                        fail_fast=True,
                    )
                    # print_steps_result(steps)
                    print("GOOD", config.title, config.flavours, config.content_item_id)
                except Exception as e:
                    # continue
                    print("BAD", config.title, config.flavours, config.content_item_id)
                    print()
                    print("Exception:", str(e))
                    print()
