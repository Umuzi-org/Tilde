"""
There is some kind of bug that causes duplicate progress items to be created for some users. This script cleans those up.
"""
from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProject, TopicProgress
from core.models import User
from django.db.models import Count


def cleanup_duplicates(base_query):
    l = (
        base_query.values("content_item_id")
        .annotate(count=Count("content_item_id"))
        .filter(count__gt=1)
        .order_by("content_item_id")
    )
    for d in l:
        possible_matches = base_query.filter(content_item_id=d["content_item_id"])

        grouped_by_flavour = {}
        for p in possible_matches:
            flavours = ",".join(sorted(p.flavour_names))
            grouped_by_flavour[flavours] = grouped_by_flavour.get(flavours, []) + [p]

        for flavours, instances in grouped_by_flavour.items():
            if len(instances) > 1:
                deduplicate(instances)


def deduplicate(instances):
    for time_field in ["complete_time", "review_request_time", "start_time"]:
        timestamped = sorted(
            [i for i in instances if i.__getattribute__(time_field)],
            key=lambda x: x.__getattribute__(time_field),
        )
        if len(timestamped) > 1:
            keep = timestamped[0]
            to_delete = [o for o in instances if o != keep]
            # breakpoint()
            for o in to_delete:
                print(f"deleting {o}")
                o.delete()
            return


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str, nargs="?", default=None)

    def handle(self, *args, **options):
        if options["who"]:
            users = [
                o for o in User.get_users_from_identifier(options["who"]) if o.active
            ]
            total = len(users)
        else:
            users = User.objects.filter(active=True)
            total = users.count()
        for i, user in enumerate(users):
            print(f"checking user {i+1}/{total}: {user}")
            cleanup_duplicates(base_query=TopicProgress.objects.filter(user=user))
            cleanup_duplicates(
                base_query=RecruitProject.objects.filter(recruit_users=user)
            )
