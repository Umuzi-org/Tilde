"""

"""
from django.core.management.base import BaseCommand, CommandParser
from automarker_app.lib.marker import mark_project
from ..utils import print_steps_result


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("content_item_id", type=int)
        parser.add_argument("flavours", type=str, nargs="+")

    def handle(self, *args, **options):
        content_item_id = options["content_item_id"]
        flavours = options["flavours"]
        steps = mark_project(
            content_item_id=content_item_id,
            flavours=flavours,
            self_test=True,
            fail_fast=True,
        )
        print_steps_result(steps)
