"""
Takes a curriculum and turns it into a json object. That object could be imported using import_curriculum.

This exists to help set up demo data for for easy dev.

eg:

python manage.py export_curriculum 33 dev_helpers/data/intro-to-tilde-course.json
python manage.py export_curriculum 4 dev_helpers/data/data-eng-part-1.json
python manage.py export_curriculum 81 dev_helpers/data/web-dev-bootcamp-automarked.json

"""

from core.models import Curriculum
from curriculum_tracking.models import (
    CurriculumContentRequirement,
    ContentItemOrder,
)
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("curriculum", type=str)
        parser.add_argument("save_path", type=str)

    def handle(self, *args, **options):
        curriculum_arg = options["curriculum"]
        if curriculum_arg.isdigit():
            curriculum = Curriculum.objects.get(pk=int(curriculum_arg))
        else:
            curriculum = Curriculum.objects.get(name=curriculum_arg)
        d = get_export_dict(curriculum)

        with open(options["save_path"], "w") as f:
            json.dump(d, f, indent=2, sort_keys=True)


def get_export_dict(curriculum):
    content_requirements = CurriculumContentRequirement.objects.filter(
        curriculum=curriculum
    )
    all_content_items = [o.content_item for o in get_ordered_content_items(curriculum)]

    export = {
        "curriculum": {
            "name": curriculum.name,
            "blurb": curriculum.blurb,
            "id": curriculum.id,
        },
        "curriculum_content_requirements": [
            {
                "content_item": o.content_item.url,
                "hard_requirement": o.hard_requirement,
                "order": o.order,
                "flavours": o.flavour_names,
            }
            for o in content_requirements
        ],
        "content_items": [
            {
                "id": o.id,
                "content_type": o.content_type,
                "title": o.title,
                "slug": o.slug,
                "url": o.url,
                "raw_url": o.raw_url,
                "tags": o.tag_names,
                "flavours": o.flavour_names,
                "topic_needs_review": False,
                "project_submission_type": o.project_submission_type,
                "continue_from_repo": o.continue_from_repo and o.continue_from_repo.url,
                "template_repo": o.template_repo,
                "link_regex": o.link_regex,
                "blurb": o.blurb,
                "link_name": o.link_name,
                "link_example": o.link_example,
                "link_message": o.link_message,
            }
            for o in all_content_items
        ],
        "content_item_orders": [],
    }
    for item in all_content_items:
        for o in ContentItemOrder.objects.filter(post=item):
            export["content_item_orders"].append(
                {
                    "post": o.post.url,
                    "pre": o.pre.url,
                    "hard_requirement": o.hard_requirement,
                }
            )
    return export
