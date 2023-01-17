"""
Export info about curriculums so that their modular nature is clear. Exported data will be in csv format and will include:

- Streams
- Curriculums
- Individual pieces of content
- Outcomes met 

"""

from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum
from core.models import Stream
import csv
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):

        content_rows = []
        curriculum_outcomes = {
            # curriculum_id : [outcomes]
        }

        for curriculum in Curriculum.objects.all():
            curriculum_outcomes[curriculum.name] = []

            for x in get_ordered_content_items(curriculum):
                content_item = x.content_item
                print(
                    f"{x.content_item} - flavours {x.flavours} - tags {[str(s) for s in x.content_item.tags.all()]} {x.content_item.url}"
                )

                curriculum_outcomes[curriculum.name].extend(
                    [
                        o
                        for o in content_item.learning_outcomes.all()
                        if o not in curriculum_outcomes[curriculum.name]
                    ]
                )

                content_rows.append(
                    {
                        "course name": curriculum.name,
                        "title": content_item.title,
                        "content_id": content_item.id,
                        "content_type": content_item.content_type,
                        "flavours": [o.name for o in x.flavours],
                        # "flavours_str": str(sorted([o.name for o in x.flavours])),
                        "tags": ", ".join(content_item.tag_names),
                        "url": content_item.url,
                        # "is_hard_milestone": x.is_hard_milestone,
                        # "is_soft_milestone": x.is_soft_milestone,
                        "learning_outcomes": _format_outcomes(
                            content_item.learning_outcomes.all()
                        ),
                    }
                )

        stream_rows = []
        for stream in Stream.objects.all():

            for stream_curriculum in stream.stream_curriculums.all():
                curriculum = stream_curriculum.curriculum
                stream_rows.append(
                    [
                        stream.name,
                        curriculum.name,
                        _format_outcomes(curriculum_outcomes[curriculum.name]),
                    ]
                )

        today = timezone.now().date().strftime("%a %d %b %Y")

        headings = content_rows[0].keys()

        with open(f"gitignore/{today}_content_items.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for row in content_rows:
                writer.writerow([row[key] for key in headings])

        with open(f"gitignore/{today}_curriculums.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["course name", "outcomes"])
            for name, outcomes in curriculum_outcomes.items():
                writer.writerow([name, _format_outcomes(outcomes)])

        with open(f"gitignore/{today}_streams.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["stream name", "course name", "outcomes"])


def _format_outcomes(outcomes):
    result = "\n- ".join(
        [f"[{outcome.name}]: {outcome.description}" for outcome in outcomes]
    )
    return f"- {result}"
