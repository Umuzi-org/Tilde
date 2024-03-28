from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum
import csv
from pathlib import Path
from core.models import Stream


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("stream", type=str)

    def handle(self, *args, **options):
        stream_name = options["stream"]
        stream = Stream.objects.get(name=stream_name)

        headings = [
            "stream_name",
            "curriculum_name",
            "id",
            "title",
            "type",
            "flavours",
            "tags",
            "url",
        ]

        seen = []

        with open(Path(f"gitignore/{stream_name}.csv"), "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)

            for stream_curriculum in stream.stream_curriculums.order_by("order"):
                curriculum = stream_curriculum.curriculum

                for x in get_ordered_content_items(curriculum):
                    identity = f"{x.content_item.id} {x.content_item.title} {sorted(x.flavours)}"
                    if identity not in seen:
                        seen.append(identity)
                        print(identity)
                        writer.writerow(
                            [
                                stream_name,
                                curriculum.name,
                                x.content_item.id,
                                x.content_item.title,
                                x.content_item.content_type,
                                " ".join([f.name for f in x.flavours]),
                                [str(s) for s in x.content_item.tags.all()],
                                x.content_item.url,
                            ]
                        )
