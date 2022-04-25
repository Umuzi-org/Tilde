from core.models import *
from curriculum_tracking.models import *
from django.db.models import Q
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        teams = Team.objects.filter(name__startswith="E1")
        users = []

        for team in teams:
            users.extend(team.user_set.all())

        ip_cards = (
            AgileCard.objects.filter(assignees__in=users)
            .filter(
                Q(status=AgileCard.IN_PROGRESS)
                | Q(status=AgileCard.IN_REVIEW)
                | Q(status=AgileCard.REVIEW_FEEDBACK)
            )
            .prefetch_related("content_item")
        )

        backlog_cards = (
            AgileCard.objects.filter(assignees__in=users)
            .filter(Q(status=AgileCard.READY) | Q(status=AgileCard.BLOCKED))
            .order_by("order")
            .prefetch_related("content_item")
        )

        complete_cards = (
            AgileCard.objects.filter(assignees__in=users)
            .filter(status=AgileCard.COMPLETE)
            .prefetch_related("content_item")
        )

        # for item in set(backlog_cards):
        #     print(item)

        yielded = []

        for card in ip_cards | backlog_cards | complete_cards:
            item = card.content_item
            if item.id in yielded:
                continue
            else:
                yielded.append(item.id)

            url_end = item.url[len("http://syllabus.africacode.net/") :]
            full_url = f"https://github.com/Umuzi-org/ACN-syllabus/tree/develop/content/{url_end}_index.md"
            print(full_url)
