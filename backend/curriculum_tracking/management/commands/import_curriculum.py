from core.models import Curriculum
from curriculum_tracking.models import (
    CurriculumContentRequirement,
    ContentItemOrder,
    ContentItem,
)
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
import json
from django.core.management.base import BaseCommand
import pandas as pd


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("curriculum", type=str)
    #     parser.add_argument("save_path", type=str)

    def handle(self, *args, **options):
        json_file = "dev_helpers/data/intro-to-tilde-course.json"
        save_curriculum_to_db(json_file)


def save_curriculum_to_db(json_file):
    with open(json_file) as f:
        data = json.load(f)

    df_dict = {i: pd.DataFrame(data[i]) if i != 'curriculum' else pd.DataFrame(pd.Series(data[i])).transpose() for i in data}
    # dataframes present in dictionary `df_dict` (4) `content_item_orders`, `content_items`, `curriculum`, `curriculum_content_requirements`

    for i in df_dict:
        df = df_dict[i]

        for idx, row in df.iterrows():
            if i == 'curriculum':
                curriculum, created = Curriculum.objects.get_or_create(
                    name = row['name'],
                    short_name = row['short_name']
                )

            elif i == 'content_items':
                content_items, created = ContentItem.objects.get_or_create(
                    # available_flavours = ','.join(row['available_flavours']),
                    content_type = row['content_type'],
                    continue_from_repo = find_url_index(row['continue_from_repo'], ContentItem),
                    link_regex = row['link_regex'],
                    project_submission_type = row['project_submission_type'],
                    slug = row['slug'],
                    story_points = row['story_points'],
                    # tags = ','.join(row['tags']),
                    template_repo = row['template_repo'],
                    title = row['title'],
                    topic_needs_review = row['topic_needs_review'],
                    url = row['url']
                )

            elif i == 'content_item_orders':
                content_item_orders, created = ContentItemOrder.objects.get_or_create(
                    hard_requirement = row['hard_requirement'],
                    post = find_url_index(row['post'], ContentItem),
                    pre = find_url_index(row['pre'], ContentItem)
                )
            
            # elif i == 'curriculum_content_requirements':
            #     curriculum_content_requirements, created = CurriculumContentRequirement.objects.get_or_create(
            #         content_item = find_url_index(url=row['content_item'], ContentItem),
            #         flavours = row['flavours'],
            #         hard_requirement = row['hard_requirement'],
            #         order = row['order']
            #     )

def find_url_index(link, model):
    if link == None:
        return 
    else:
        for index, value in enumerate(model.objects.all()):
            if value.url == link:
                return model.objects.filter(url=link).first()