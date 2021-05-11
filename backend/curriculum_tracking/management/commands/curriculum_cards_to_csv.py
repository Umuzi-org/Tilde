from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum
from django.db.models import Q
import pandas as pd


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file_name", type=str)
        parser.add_argument("curriculums", type=str, nargs="*")

    def handle(self, *args, **options):
        # df = pd.DataFrame(columns=["curriculum", "title", "flavour", "tags", "url"])

        rows = []
        curriculum_names = options["curriculums"]
        for name in curriculum_names:
            print(f'curriculum name = "{name}"')
            curriculum = Curriculum.objects.get(Q(short_name=name) | Q(name=name))

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
        df.to_csv(f"gitignore/{options['file_name']}_curriculums.csv")


"""

python manage.py curriculum_cards_to_csv "web dev"  "Web development boot camp"   "Post Bootcamp Soft Skills" "NCIT - JavaScript" "Web Development - part 1" "Web Development - part 2"
python manage.py curriculum_cards_to_csv "data eng" "Data Engineering boot camp" "Post Bootcamp Soft Skills" "NCIT - Python" "Data Engineering - part 1" "Data Engineering - part 2"
python manage.py curriculum_cards_to_csv "web dev alumni" "Alumni Web developement Bootcamp" "Post Bootcamp Soft Skills" "Web Development - part 2"
python manage.py curriculum_cards_to_csv "data eng alumni" "Alumni Data Engineering Bootcamp" "Post Bootcamp Soft Skills" "Data Engineering - part 2"
python manage.py curriculum_cards_to_csv "java" "Java boot camp" "Post Bootcamp Soft Skills" "NCIT - Java" "Java Systems Development - part 1" "Java Systems Development - part 2"
python manage.py curriculum_cards_to_csv "java alumni" "Alumni Java Bootcamp" "Post Bootcamp Soft Skills" "Java Systems Development - part 2"
python manage.py curriculum_cards_to_csv "data sci"  "Data Science boot camp" "Post Bootcamp Soft Skills" "NCIT - Python" "Data Science"
"""