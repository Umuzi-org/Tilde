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
            curriculum = Curriculum.objects.get(short_name=curriculum_arg)
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
            "short_name": curriculum.short_name,
            "name": curriculum.name,
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
                "content_type": o.content_type,
                "title": o.title,
                "slug": o.slug,
                "url": o.url,
                "story_points": o.story_points,
                "tags": o.tag_names,
                "flavours": o.flavour_names,
                "topic_needs_review": o.topic_needs_review,
                "project_submission_type": o.project_submission_type,
                "continue_from_repo": o.continue_from_repo and o.continue_from_repo.url,
                "template_repo": o.template_repo,
                "link_regex": o.link_regex,
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