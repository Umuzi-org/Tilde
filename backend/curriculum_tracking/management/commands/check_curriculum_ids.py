"""
print out all the curriculums mentioned in the repo alongside database data for each curriculum. This is so that a human can look at the names and titles and suchlike and see if there is anything inconsistent going on
"""

from curriculum_tracking.models import Curriculum
import frontmatter
from django.core.management.base import BaseCommand
from pathlib import Path


TITLE = "title"
DB_ID = "_db_id"


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path_to_tech_dept_repo", type=str)

    def get_content_data(self, path_to_repo):
        result = {}
        curriculums_base_dir = path_to_repo / "content/syllabuses"
        for child in curriculums_base_dir.iterdir():
            if child.is_dir():
                raise Exception(child)
            name = child.name
            if name.startswith("_"):
                continue
            if not name.endswith(".md"):
                continue

            front = frontmatter.load(child)
            title = front.get(TITLE)
            db_id = front.get(DB_ID)
            result[db_id or title] = {"frontmatter title": title}
        return result

    def get_db_data(self):
        return {
            o.id: {"name": o.name, "short_name": o.short_name}
            for o in Curriculum.objects.all()
        }

    def handle(self, *args, **options):
        path_to_repo = Path(options.get("path_to_tech_dept_repo"))
        content_data = self.get_content_data(path_to_repo)
        db_data = self.get_db_data()

        for db_id, db_instance_data in db_data.items():
            if db_id not in content_data:
                continue
            # content_data[db_id] = content_data.get(db_id, {})
            content_data[db_id] = dict(
                list(content_data[db_id].items()) + list(db_instance_data.items())
            )

        import pprint

        pprint.pprint(content_data)
