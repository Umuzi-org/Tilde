from django.core.management.base import BaseCommand
from curriculum_tracking.card_generation_helpers import get_ordered_content_items
from curriculum_tracking.models import Curriculum
from django.db.models import Q


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("curriculum", type=str)

    def handle(self, *args, **options):
        name = options["curriculum"]
        curriculum = Curriculum.objects.get(Q(short_name=name) | Q(name=name))

        for x in get_ordered_content_items(curriculum):
            print(f"{x.content_item.content_type} - {x.content_item} - {x.flavours}")
