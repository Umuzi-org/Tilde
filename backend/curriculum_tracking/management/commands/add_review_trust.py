from django.core.management.base import BaseCommand
from curriculum_tracking.models import ReviewTrust


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)
        parser.add_argument("content_item_title", type=str)
        parser.add_argument("flavour", type=str)
        parser.add_argument("update_previous_reviews", type=int)

    def handle(self, *args, **options):
        who = options["who"]
        content_item_title = options["content_item_title"]
        flavours = [s for s in options["flavour"].split(",") if s]
        update_previous_reviews = bool(options["update_previous_reviews"])

        ReviewTrust.add_specific_trust_instances(
            who=who,
            content_item_title=content_item_title,
            flavours=flavours,
            update_previous_reviews=update_previous_reviews,
        )
