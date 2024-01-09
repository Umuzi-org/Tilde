from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum
import csv
from pathlib import Path


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("curriculum", type=str)
        # parser.add_argument("as_csv", type=bool, default=False, nargs="?")

    def handle(self, *args, **options):
        name = options["curriculum"]
        curriculum = Curriculum.objects.get(name=name)

        headings = [
            "curriculum_name",
            "id",
            "title",
            "flavours",
            "tags",
            "url",
        ]
        with open(Path(f"gitignore/{curriculum}.csv"), "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)

            for x in get_ordered_content_items(curriculum):
                print(
                    f"{x.content_item.id} {x.content_item} - flavours {x.flavours} - tags {[str(s) for s in x.content_item.tags.all()]} {x.content_item.url}"
                )
                writer.writerow(
                    [
                        name,
                        x.content_item.id,
                        x.content_item,
                        x.flavours,
                        [str(s) for s in x.content_item.tags.all()],
                        x.content_item.url,
                    ]
                )
