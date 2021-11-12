from django.core.management.base import BaseCommand
from core.models import User
from curriculum_tracking.models import AgileCard, ContentItem
import csv


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)

    def handle(self, *args, **options):
        who = options["who"]
        users = User.get_users_from_identifier(who)

        result = []
        for user in users:
            print(user)
            for card in (
                AgileCard.objects.filter(assignees__in=[user])
                .filter(content_item__content_type=ContentItem.PROJECT)
                .filter(status=AgileCard.COMPLETE)
                .order_by("recruit_project__complete_time")
            ):
                print(card)
                result.append(
                    [
                        user.email,
                        card.title,
                        card.content_url,
                        ", ".join(card.tag_names),
                    ]
                )

        with open(f"gitignore/completed_projects_{who}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["email", "title", "url", "tags"])
            writer.writerows(result)
