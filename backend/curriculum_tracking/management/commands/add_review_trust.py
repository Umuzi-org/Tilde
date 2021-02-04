from django.core.management.base import BaseCommand
from curriculum_tracking.models import ContentItem, ReviewTrust

# from core.models import Team, User
from ..helpers import get_users


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
        update_previous_reviews = options["update_previous_reviews"]

        users = get_users(who)

        content_item = ContentItem.objects.get(title=content_item_title)
        available_flavours = content_item.flavours.all()
        available_flavour_names = [o.name for o in available_flavours]
        for flavour_name in flavours:
            assert (
                flavour_name in available_flavour_names
            ), f"{flavour_name} not allowed. choose from {available_flavour_names}"
        final_flavours = [o for o in available_flavours if o.name in flavours]

        trust_instances = []

        for user in users:
            trusts = ReviewTrust.objects.filter(content_item=content_item, user=user)
            found = False
            for trust in trusts:
                if trust.flavours_match(flavours):
                    found = True
                    trust_instances.append(trust)
                    break
            if not found:
                trust = ReviewTrust.objects.create(content_item=content_item, user=user)
                for flavour in final_flavours:
                    trust.flavours.add(flavour)
                trust_instances.append(trust)

        if update_previous_reviews:
            for trust in trust_instances:
                trust.update_previous_reviews()