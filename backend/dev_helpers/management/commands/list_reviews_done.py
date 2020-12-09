from django.core.management.base import BaseCommand
from core.models import UserGroupMembership
from curriculum_tracking.models import RecruitProjectReview
from django.utils import timezone
from collections import namedtuple

cutoff = timezone.now() - timezone.timedelta(days=1, hours=6)


Result = namedtuple("Result", "email count weight")


def get_reviews_for_group(group_name):
    members = UserGroupMembership.objects.filter(group__name=group_name)

    for member in members:
        reviews = RecruitProjectReview.objects.filter(
            timestamp__gte=cutoff, reviewer_user=member.user
        )
        weight = sum(
            [review.recruit_project.content_item.story_points for review in reviews]
        )
        count = reviews.count()
        yield Result(member.user.email, count, weight)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("group_names", type=str, nargs="*")
        # parser.add_argument("da")

    def handle(self, *args, **options):
        # group = UserGroup.objects.get(name=options["group_name"])
        # print(options["group_names"])

        results = []
        for name in options["group_names"]:
            results.extend(get_reviews_for_group(name))

        results.sort(key=lambda o: o.weight)
        for result in results:
            print(result)
