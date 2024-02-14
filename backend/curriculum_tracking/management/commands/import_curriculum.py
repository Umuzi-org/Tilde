"""
Takes a curriculum from a json file and stores it in the db. The curriculum would have been exported using the export_curriculum command

eg:
python manage.py import_curriculum dev_helpers/data/intro-to-tilde-course.json
python manage.py import_curriculum dev_helpers/data/data-eng-part-1.json

"""

from core.models import Curriculum
from curriculum_tracking.models import (
    CurriculumContentRequirement,
    ContentItemOrder,
    ContentItem,
)
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **options):
        save_curriculum_to_db(
            options["json_file"]
        )  # "dev_helpers/data/intro-to-tilde-course.json"


def save_curriculum_to_db(json_file):
    with open(json_file) as f:
        data = json.load(f)

    # keys in dictionary `data` (4) `content_item_orders`, `content_items`, `curriculum`, `curriculum_content_requirements`
    create_content_items(data["content_items"])
    create_content_item_orders(data["content_item_orders"])
    curriculum = create_curriculum(data["curriculum"])
    create_curriculum_content_requirements(
        data["curriculum_content_requirements"], data["curriculum"]["name"]
    )
    return curriculum


def get_content_item_from_url(url):
    if url:
        return ContentItem.objects.get(url=url)


def create_content_items(data):
    for content in data:
        content_item, created = ContentItem.objects.get_or_create(
            id=content["id"],
            content_type=content["content_type"],
            continue_from_repo=get_content_item_from_url(content["continue_from_repo"]),
            link_regex=content["link_regex"],
            project_submission_type=content["project_submission_type"],
            slug=content["slug"],
            # tags = ','.join(content['tags']),
            template_repo=content["template_repo"],
            title=content["title"],
            topic_needs_review=False,
            url=content["url"],
            raw_url=content["raw_url"],
            blurb=content["blurb"],
            link_name=content["link_name"],
            link_example=content["link_example"],
            link_message=content["link_message"],
        )

        for tag in content["tags"]:
            content_item.tags.add(tag)

        if content["flavours"]:
            content_item.set_flavours(content["flavours"])


def create_content_item_orders(data):
    for order in data:
        content_item_orders, created = ContentItemOrder.objects.get_or_create(
            hard_requirement=order["hard_requirement"],
            post=get_content_item_from_url(order["post"]),
            pre=get_content_item_from_url(order["pre"]),
        )


def create_curriculum(data):
    curriculum, created = Curriculum.objects.get_or_create(
        name=data["name"], id=data["id"], blurb=data["blurb"]
    )
    return curriculum


def create_curriculum_content_requirements(data, curriculum_name):
    curriculum = Curriculum.objects.get(name=curriculum_name)
    for requirement in data:
        (
            curriculum_content_requirements,
            created,
        ) = CurriculumContentRequirement.objects.get_or_create(
            content_item=get_content_item_from_url(requirement["content_item"]),
            # flavours = ','.join(requirement['flavours']),
            curriculum=curriculum,
            hard_requirement=requirement["hard_requirement"],
            order=requirement["order"],
        )

        curriculum_content_requirements.set_flavours(requirement["flavours"])
