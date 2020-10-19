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
    def handle(self, *args, **options):
        json_file = "dev_helpers/data/intro-to-tilde-course.json"
        save_curriculum_to_db(json_file)


def save_curriculum_to_db(json_file):
    with open(json_file) as f:
        data = json.load(f)

    # keys in dictionary `data` (4) `content_item_orders`, `content_items`, `curriculum`, `curriculum_content_requirements`
    create_content_items(data['content_items'])
    create_content_item_orders(data['content_item_orders'])
    create_curriculum(data['curriculum'])
    create_curriculum_content_requirements(data['curriculum_content_requirements'])

def find_url_index(link, model):
    if link == None:
        return 
    else:
        for index, value in enumerate(model.objects.all()):
            if value.url == link:
                return model.objects.filter(url=link).first()

def create_content_items(data):
    for content in data:
        content_items, created = ContentItem.objects.get_or_create(
            # available_flavours = ','.join(content['available_flavours']),
            content_type = content['content_type'],
            continue_from_repo = find_url_index(content['continue_from_repo'], ContentItem),
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
            post = find_url_index(order['post'], ContentItem),
            pre = find_url_index(order['pre'], ContentItem)
        )


def create_curriculum(data):
    curriculum, created = Curriculum.objects.get_or_create(
        name = data['name'],
        short_name = data['short_name']
    )

def create_curriculum_content_requirements(data):
    for requirement in data:
        curriculum_content_requirements, created = CurriculumContentRequirement.objects.get_or_create(
            content_item = find_url_index(requirement['content_item'], ContentItem),
            # flavours = requirement['flavours'],
            curriculum = Curriculum.objects.filter(short_name='tilde intro student').first(),
            hard_requirement = requirement['hard_requirement'],
            order = requirement['order']
        )