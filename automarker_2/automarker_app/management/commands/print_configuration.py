from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from automarker_app.lib.marker import get_all_marker_configs


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        for configuration in get_all_marker_configs():
            print(
                f"{configuration.title}[{configuration.content_item_id}] {configuration.flavours} {configuration.status}"
            )
