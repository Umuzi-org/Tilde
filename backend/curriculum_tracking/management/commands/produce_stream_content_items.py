from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum, AgileCard, ContentItemAgileWeight
from core.models import StreamCurriculum
from pathlib import Path
import pandas as pd


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("stream", type=str)

    def handle(self, *args, **options):
        name = options["stream"]

        stream_curriculums = StreamCurriculum.objects.filter(stream__name=name)

        curriculum_list = []

        for stream_curriculum in stream_curriculums:
            curriculum_list.append(stream_curriculum.curriculum)

        print(curriculum_list)

        content_list = []

        for curriculum in curriculum_list:

            for x in get_ordered_content_items(curriculum):

                if x.content_item.content_type == "P":
                    content_list.append(
                        {
                            "content_id": x.content_item.id,
                            "title": x.content_item.title,
                            "flavours": str([str(s) for s in x.flavours]),
                        }
                    )

        content_df = pd.DataFrame(content_list)
        content_df.drop_duplicates(inplace=True)
        content_df.to_csv(f"gitignore/stream_{name}_content_items.csv")
