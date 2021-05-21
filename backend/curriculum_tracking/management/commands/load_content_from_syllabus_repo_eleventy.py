# from core.models import Curriculum
from django.core.management.base import BaseCommand
import frontmatter
import taggit

from curriculum_tracking import models
from pathlib import Path
import yaml

DB_ID = "_db_id"
CONTENT_TYPE = "content_type"
TAGS = "tags"

COURSE = "course"

reverse_content_types = {t[1]: t[0] for t in models.ContentItem.CONTENT_TYPES}
reverse_submission_types = {
    t[1]: t[0] for t in models.ContentItem.PROJECT_SUBMISSION_TYPES
}

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def setup(self, path):
        self.path = Path(path)
        settings_path = self.path / ".tilde.yaml"
        with open(settings_path, "r") as f:
            settings = yaml.load(f)
        self.content_location = self.path / settings["content_location"]
        self.base_url = settings["base_url"]
        self.setup_flavours(settings["flavours"])
        
        self.seen_content_ids = {}
        self.seen_course_ids = {}        

    def setup_flavours(self,flavours):
        self.flavours = {
            d['name'] : d['includes']
            for d in flavours
        }

    def set_content_flavours(self,content_item, raw_flavours):

        right_hand_side = [i for l in self.flavours.values() for i in l]

        flavours = []
        for flavour in raw_flavours:
            if flavour in right_hand_side:
                flavours.append(flavour)
            else:
                flavours.extend(self.flavours[flavour])
        # if (
        #     content_item.content_type == content_item.PROJECT
        #     and content_item.project_submission_type != content_item.NO_SUBMIT
        # ):
        #     assert (
        #         flavours
        #     ), f"no available flavours specified. Be explicit. Perhaps you forgot to say flavours: ['none']\n\t{content_item.url}"

        if "none" in flavours:
            assert (
                len(flavours) == 1
            ), f"either it is None or it isn't!\n\t{content_item.url}"
            return  # nothing to do

        tags = [
            t[0]
            for t in [
                taggit.models.Tag.objects.get_or_create(name=tag_name)
                for tag_name in flavours
            ]
        ]

        for tag in tags:

            models.ContentAvailableFlavour.objects.get_or_create(
                tag=tag, content_item=content_item
            )

        # remove the unnecessary ones
        for tag in content_item.flavours.all():
            if tag not in tags:
                models.ContentAvailableFlavour.objects.get(
                    tag=tag, content_item=content_item
                ).delete()

        # sanity check
        final = sorted([o.name for o in content_item.flavours.all()])
        assert final == sorted(
            flavours
        ), f"Flavours dont match: Expected {flavours} but got {final}"

    def update_tags(self,meta,content_item):
        # todo_tag, _ = taggit.models.Tag.objects.get_or_create(name=TODO)
        # ready = meta.get("ready", False)
        # if ready:
        #     assert ready == True, f"{ready} {type(ready)}"
        #     content_item.tags.remove(todo_tag)
        # else:
        #     content_item.tags.add(todo_tag)
        # if meta.get(TODO):
        #     content_item.tags.add(todo_tag)

        tags = []
        for tag_str in meta.get(TAGS, []):
            tag, _ = taggit.models.Tag.objects.get_or_create(name=tag_str.lower())
            content_item.tags.add(tag)
            tags.append(tag)

        for tag in list(content_item.tags.all()):
            if tag not in tags:
                content_item.tags.remove(tag)
                # models.ContentAvailableFlavour.objects.get(
                #     tag=tag, content_item=content_item
                # ).delete()

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

        directory_path = self.path / from_repo 
        matching_paths = [s for s in directory_path.iterdir() if s.stem in ['index','_index']]
        assert len(matching_paths) == 1, f"invalid directory structure: {matching_paths}"
        # breakpoint()         

        continue_from_repo = self.save_content(file_path=matching_paths[0])
        assert continue_from_repo
        return continue_from_repo

    def save_content(self,file_path):
        print(f"processing {file_path}")

        content_item_post = frontmatter.load(file_path)
        meta = dict(content_item_post)

        title = meta["title"].strip()
        assert title

        url = self.get_page_url(file_path)
        meta_content_type = meta["content_type"] 
        if meta_content_type == 'none':
            assert DB_ID not in meta, f"this is in the database, but probebaly shouldn't be: {file_path}"
            return
        actual_content_type = reverse_content_types[meta_content_type]

        project_submission_type = (
            reverse_submission_types[meta["submission_type"]]
            if "submission_type" in meta
            else None
        )

        defaults = {
            "content_type": actual_content_type,
            "title": title,
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

        self.set_content_flavours(
            content_item,
            meta.get("flavours", []),
        )
        self.update_tags(meta, content_item)
        content_item.save()

        content_item_post[DB_ID] = content_item.id

        with open(file_path, "wb") as f:
            frontmatter.dump(content_item_post, f)

        self.seen_content_ids[content_item.id] = content_item.url
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
            self.seen_content_ids[db_id] = file_path

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


    def add_all_prerequisites(self):
        woo



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
