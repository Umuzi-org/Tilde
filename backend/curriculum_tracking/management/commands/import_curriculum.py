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
        data = json.load(a)

    df_dict = {i: pd.DataFrame(data[i]) if i != 'curriculum' else pd.DataFrame(pd.Series(data[i])).transpose() for i in data}
    # dataframes present in dictionary `df_dict` (4) `content_item_orders`, `content_items`, `curriculum`, `curriculum_content_requirements`

    for i in df_dict:
        df = df_dict[i]


        for idx, row in df.iterrows():
            if i == 'content_item_orders'
                content_item_orders, created = ContentItemOrder.objects.get_or_create(
                    hard_requirement = row['hard_requirement']
                    post = row['post']
                    pre = row['pre']
                )
            
            elif i == 'content_items'
                _, created = MODEL.objects.get_or_create(_= row[''])

            elif i == 'curriculum'
                _, created = MODEL.objects.get_or_create(_= row[''])

            elif i == 'curriculum_content_requirements'
                _, created = MODEL.objects.get_or_create(_= row[''])