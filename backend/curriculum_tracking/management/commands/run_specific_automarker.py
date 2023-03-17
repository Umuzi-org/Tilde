"""
example usage

python manage.py run_specific_automarker "simple-calculator part 1" ""
python manage.py run_specific_automarker "Person" ""
python manage.py run_specific_automarker "password-checker" ""
"""
from django.core.management.base import BaseCommand
from curriculum_tracking.models import ContentItem


from curriculum_tracking.management.automarker_utils import (
    get_cards_needing_review,
    automark_card,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("content_item", type=str)
        parser.add_argument("flavours", type=str, default="")
        parser.add_argument("debug", type=int, default=1)

    def handle(self, *args, **options):
        content_item_title = options["content_item"]
        flavours = [s.strip() for s in options["flavours"].split(",") if s]
        debug_mode = bool(options["debug"])

        content_item = ContentItem.objects.get(title=content_item_title)

        for card in get_cards_needing_review(
            content_item=content_item, flavours=flavours
        ):

            automark_card(card, debug_mode)
