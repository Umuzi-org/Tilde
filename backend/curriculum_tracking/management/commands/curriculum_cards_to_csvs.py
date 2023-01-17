from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum
import pandas as pd

from ..course_streams import COURSES_BY_STREAM


DEPRECATED


class Command(BaseCommand):
    def handle(self, *args, **options):
        for stream, curriculum_names in COURSES_BY_STREAM.items():
            for name in curriculum_names:
                print(name)
                Curriculum.objects.get(name=name)

        for stream, curriculum_names in COURSES_BY_STREAM.items():
            self.handle_single_stream(stream=stream, curriculum_names=curriculum_names)

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
                        "content_id": content_item.id,
                        "content_type": content_item.content_type,
                        "flavours": [o.name for o in x.flavours],
                        "flavours_str": str(sorted([o.name for o in x.flavours])),
                        "tags": ", ".join(content_item.tag_names),
                        "url": content_item.url,
                        "is_hard_milestone": x.is_hard_milestone,
                        "is_soft_milestone": x.is_soft_milestone,
                        "learning_outcomes": "\n".join(
                            [
                                f"[{outcome.name}] {outcome.description}"
                                for outcome in content_item.learning_outcomes.all()
                            ]
                        ),
                    }
                )

        df = pd.DataFrame(rows)
        df = df.drop_duplicates(subset=["url", "flavours_str"], keep="first")
        df = df[
            [
                "course name",
                "content_id",
                "content_type",
                "title",
                "flavours",
                "tags",
                "url",
                # "is_hard_milestone",
                # "is_soft_milestone",
                "learning_outcomes",
            ]
        ]
        df.to_csv(f"gitignore/{stream}_cards.csv")
