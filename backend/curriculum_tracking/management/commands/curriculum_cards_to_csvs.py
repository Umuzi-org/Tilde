from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum
import pandas as pd

from ..course_streams import COURSES_BY_STREAM


class Command(BaseCommand):
    def handle(self, *args, **options):
        for stream, Curriculum_names in COURSES_BY_STREAM.items():
            self.handle_single_stream(stream=stream, curriculum_names=Curriculum_names)

    def handle_single_stream(self, stream, curriculum_names):
        rows = []
        for name in curriculum_names:
            print(f'curriculum name = "{name}"')
            curriculum = Curriculum.objects.get(name=name)

            for x in get_ordered_content_items(curriculum):
                content_item = x.content_item
                print(
                    f"{x.content_item} - flavours {x.flavours} - tags {[str(s) for s in x.content_item.tags.all()]} {x.content_item.url}"
                )
                rows.append(
                    {
                        "course name": curriculum.name,
                        "title": content_item.title,
                        "flavours": [o.name for o in x.flavours],
                        "flavours_str": str(sorted([o.name for o in x.flavours])),
                        "tags": ", ".join(content_item.tag_names),
                        "url": content_item.url,
                    }
                )

        df = pd.DataFrame(rows)
        df = df.drop_duplicates(subset=["url", "flavours_str"], keep="first")
        df = df[["course name", "title", "flavours", "tags", "url"]]
        df.to_csv(f"gitignore/{stream}_cards.csv")
