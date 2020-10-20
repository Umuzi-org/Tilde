from core.models import Curriculum
from curriculum_tracking.models import (
    CurriculumContentRequirement,
    ContentItemOrder,
    ContentItem,
)
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **options):  
        save_curriculum_to_db(options["json_file"]) #"dev_helpers/data/intro-to-tilde-course.json"


def save_curriculum_to_db(json_file):
    with open(json_file) as f:
        data = json.load(f)

    # keys in dictionary `data` (4) `content_item_orders`, `content_items`, `curriculum`, `curriculum_content_requirements`
    create_content_items(data['content_items'])
    create_content_item_orders(data['content_item_orders'])
    create_curriculum(data['curriculum'])
    create_curriculum_content_requirements(data['curriculum_content_requirements'],data['curriculum']['short_name'])

def get_content_item_from_url(url):
    if url:
        return ContentItem.objects.get(url=url)

def create_content_items(data):
    for content in data:
        content_items, created = ContentItem.objects.get_or_create(
            # available_flavours = ','.join(content['available_flavours']),
            content_type = content['content_type'],
            continue_from_repo = get_content_item_from_url(content['continue_from_repo']),
            link_regex = content['link_regex'],
            project_submission_type = content['project_submission_type'],
            slug = content['slug'],
            story_points = content['story_points'],
            # tags = ','.join(content['tags']),
            template_repo = content['template_repo'],
            title = content['title'],
            topic_needs_review = content['topic_needs_review'],
            url = content['url']
        )


def create_content_item_orders(data):
    for order in data:
        content_item_orders, created = ContentItemOrder.objects.get_or_create(
            hard_requirement = order['hard_requirement'],
            post = get_content_item_from_url(order['post']),
            pre = get_content_item_from_url(order['pre'])
        )


def create_curriculum(data):
    curriculum, created = Curriculum.objects.get_or_create(
        name = data['name'],
        short_name = data['short_name']
    )

def create_curriculum_content_requirements(data, curriculum_name):
    curriculum = Curriculum.objects.get(short_name=curriculum_name)
    for requirement in data:
        curriculum_content_requirements, created = CurriculumContentRequirement.objects.get_or_create(
            content_item = get_content_item_from_url(requirement['content_item']),
            # flavours = ','.join(requirement['flavours']),
            curriculum = curriculum,
            hard_requirement = requirement['hard_requirement'],
            order = requirement['order']
        )