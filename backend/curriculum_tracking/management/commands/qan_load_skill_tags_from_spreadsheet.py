from django.core.management.base import BaseCommand
from google_helpers.utils import fetch_sheet
from curriculum_tracking.models import ContentItem
from taggit.models import Tag
from pathlib import Path
import frontmatter


def process_row(path_to_syllabus_repo):
    def _process_row(row):
        print(f"processing row {row}")
        content_item_id = int(row["id"])

        skill_names = row["skill_names"].replace(",", " ").split()
        skill_names = [f"skill/{clean}" for s in skill_names if (clean := s.strip())]
        if len(skill_names) == 0:
            return

        # update database
        # this only adds skill tags, it doesn't remove them

        content_item = ContentItem.objects.get(id=content_item_id)
        for name in skill_names:
            tag = Tag.objects.get_or_create(name=name)[0]
            content_item.tags.add(tag)

        # update syllabus files
        # this only adds skill tags, it does not remove them
        # url looks like: http://syllabus.africacode.net/{path}
        path_part = content_item.url[len("http://syllabus.africacode.net/") :]
        file_path = Path(path_to_syllabus_repo) / "content" / path_part / "_index.md"
        frontmatter_data = frontmatter.load(file_path)

        for name in skill_names:
            frontmatter_data["tags"] = frontmatter_data.get("tags", [])
            if name not in frontmatter_data["tags"]:
                frontmatter_data["tags"].append(name)

        with open(file_path, "wb") as f:
            frontmatter.dump(frontmatter_data, f)

    return _process_row


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path_to_syllabus_repo", type=str)

    def handle(self, *args, **options):
        path_to_syllabus_repo = options["path_to_syllabus_repo"]
        df = fetch_sheet(
            url="https://docs.google.com/spreadsheets/d/1g0Xtk_4q8LpK6dFj4o_3wAeaRAxTc1QhytoYZRMAKAE/edit#gid=0"
        )
        df = df.dropna(subset=["id"])
        df = df.dropna(subset=["skill_names"])
        df.apply(process_row(path_to_syllabus_repo=path_to_syllabus_repo), axis=1)
