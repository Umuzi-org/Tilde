from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from automarker_app.lib.marker import mark_project
from ..utils import print_steps_result, print_final_review


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("url", type=str)
        parser.add_argument("content_item_id", type=int)
        parser.add_argument("flavours", type=str, nargs="+")

    def handle(self, *args: Any, **options: Any) -> str | None:
        url = options["url"]
        content_item_id = options["content_item_id"]
        flavours = options["flavours"]
        steps = mark_project(content_item_id, flavours, url)

        print_steps_result(steps)
        print_final_review(steps)
