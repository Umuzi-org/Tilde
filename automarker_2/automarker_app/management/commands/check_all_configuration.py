from django.core.management.base import BaseCommand
from automarker_app.lib.marker import get_all_marker_configs
from automarker_app.lib.constants import CONFIG_STATUS_DEBUG, CONFIG_STATUS_PRODUCTION


class Command(BaseCommand):
    def handle(self, *args, **options):
        for configuration in get_all_marker_configs():
            if configuration.status in [CONFIG_STATUS_DEBUG, CONFIG_STATUS_PRODUCTION]:
                print(
                    f"{configuration.title}[{configuration.content_item_id}] {configuration.flavours} {configuration.status}"
                )
