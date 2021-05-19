# from core.models import Curriculum
from django.core.management.base import BaseCommand
import frontmatter

from curriculum_tracking import models
from pathlib import Path
import yaml

DB_ID = "_db_id"
CONTENT_TYPE = "content_type"

COURSE = "course"

reverse_content_types = {t[1]: t[0] for t in models.ContentItem.CONTENT_TYPES}
reverse_submission_types = {
    t[1]: t[0] for t in models.ContentItem.PROJECT_SUBMISSION_TYPES
}

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def __unpack_flavours(self,flavours):
        self.flavours = flavours

    def recurse_get_all_content_index_file_paths(self,root_path=None):

        root_path = root_path or self.content_location
        assert root_path.is_dir(), root_path
        for child in root_path.iterdir():
            if child.is_dir():
                for path in self.recurse_get_all_content_index_file_paths(child):
                    yield path
            else:
                stem = child.stem
                if stem in ["_index","index"]:
                    yield child

    def get_page_url(self,file_path):
        url_end = str(file_path.parent)[len(str(self.path)):].strip('/')
        return f"{self.base_url.strip('/')}/{url_end}/"

    def _get_continue_from_repo(self,from_repo):
        if not from_repo:
            return 
        breakpoint()
        foo

    def save_content(self,file_path):
        print(f"processing {file_path}")
        content_item_post = frontmatter.load(file_path)
        meta = dict(content_item_post)

        url = self.get_page_url(file_path)
        actual_content_type = reverse_content_types[meta["content_type"]]

        project_submission_type = (
            reverse_submission_types[meta["submission_type"]]
            if "submission_type" in meta
            else None
        )

        defaults = {
            "content_type": actual_content_type,
            "title": meta["title"],
            "story_points": int(meta.get("story_points", 1)),
            "url": url,
            "topic_needs_review": meta.get("topic_needs_review", False),
            "project_submission_type": project_submission_type,
            "continue_from_repo": self._get_continue_from_repo(meta.get('from_repo')),
            "template_repo": meta.get("template_repo"),
        }

        if DB_ID in meta:
            content_item, created = models.ContentItem.get_or_create_or_update(
                pk=meta[DB_ID], defaults=defaults, overrides=defaults
            )
        else:
            try:
                content_item = models.ContentItem.objects.get(url=url)
            except models.ContentItem.DoesNotExist:
                content_item = models.ContentItem.objects.create(
                    id=models.ContentItem.get_next_available_id(), url=url
                )
            content_item.update(**defaults)
            content_item.save()

        set_flavours(
            content_item,
            meta.get("flavours", []),
            cls.available_content_flavours,
        )
        _update_tags(meta, content_item)
        content_item.save()

        content_item_post[DB_ID] = content_item.id

        with open(file_path, "wb") as f:
            frontmatter.dump(content_item_post, f)

        cls.content_items_seen_by_id[content_item.id] = content_item.url
        return content_item

    def save_all_content_items_with_known_ids(self):
        
        content_paths = self.recurse_get_all_content_index_file_paths()
        for file_path in content_paths:
            content_item_post = frontmatter.load(file_path)
            if DB_ID not in content_item_post:
                continue

            db_id = content_item_post[DB_ID]

            if content_item_post[CONTENT_TYPE] == COURSE: 
                seen_ids = self.seen_course_ids 
                content_type = "course"
                
            else:
                seen_ids = self.seen_content_ids 
                content_type = "content"

            assert (
                db_id not in seen_ids
            ), f"Same ID on two {content_type} items!!\n\tid={db_id}\n\t{seen_ids[db_id]}\n\t{file_path}"
            self.seen_ids[db_id] = file_path

            if content_item_post[CONTENT_TYPE] != COURSE: 
                self.save_content(
                    file_path=file_path,
                )

    def save_all_content_items_with_unknown_ids(self):

        content_paths = self.recurse_get_all_content_index_file_paths()
        for file_path in content_paths:
            content_item_post = frontmatter.load(file_path)
            if DB_ID in content_item_post:
                continue

            if content_item_post[CONTENT_TYPE] == COURSE: 
                continue 

            self.save_content(
                    file_path=file_path,
                )

    def setup(self, path):
        self.path = Path(path)
        settings_path = self.path / ".tilde.yaml"
        with open(settings_path, "r") as f:
            settings = yaml.load(f)
        self.content_location = self.path / settings["content_location"]
        self.base_url = settings["base_url"]
        self.flavours = self.__unpack_flavours(settings["flavours"])
        self.seen_content_ids = {}
        self.seen_course_ids = {}

    def handle(self, *args, **options):
        self.setup(options.get("path"))

        self.save_all_content_items_with_known_ids()
        self.save_all_content_items_with_unknown_ids()

        print("Processing prerequisites....")
        self.add_all_prerequisites()

        print("Processing Courses....")
        self.set_up_courses()

        self.remove_missing_content_items_from_db()

# # TODO: BUG: optional syllabus content requirements are skipped over
