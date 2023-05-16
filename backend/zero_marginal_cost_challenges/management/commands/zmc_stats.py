from django.core.management.base import BaseCommand

from zero_marginal_cost_challenges.models import ChallengeRegistration
from curriculum_tracking.models import (
    Curriculum,
    RecruitProject,
    ContentItem,
    TopicProgress,
)
from django.db.models import Avg, F, Max
from sql_util.utils import SubqueryAggregate
import json


def get_progress(item):
    if item.content_type == ContentItem.PROJECT:
        return RecruitProject.objects.filter(content_item=item)
    if item.content_type == ContentItem.TOPIC:
        return TopicProgress.objects.filter(content_item=item)


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("group_name", type=str)
    #     parser.add_argument("activate", type=bool, default=True, nargs="?")

    def handle(self, *args, **options):
        # for now we only have one challenge so we just add some sanity checking. This check will fail once we have more than one challenge
        curriculum = Curriculum.objects.get(pk=90)
        assert (
            ChallengeRegistration.objects.all().count()
            == ChallengeRegistration.objects.filter(curriculum_id=curriculum.id).count()
        ), "looks like we have multiple challenges. yay. Implement better stats now"

        registrations = ChallengeRegistration.objects.all()

        content_items = [
            o.content_item
            for o in curriculum.content_requirements.prefetch_related("content_item")
        ]

        step_data = {}
        for item in content_items:
            progress = get_progress(item).order_by("start_time")
            complete_progress = progress.filter(complete_time__isnull=False).annotate(
                duration=F("complete_time") - F("start_time")
            )

            step_data[item.id] = {
                "title": item.title,
                "content_type": item.content_type,
                "total_progress": progress.count(),
                "completed_progress": complete_progress.count(),
                "average_duration": complete_progress.aggregate(Avg("duration")),
            }

            if item.content_type == ContentItem.PROJECT:
                review_requested_progress = (
                    progress.filter(review_request_time__isnull=False)
                    .annotate(
                        latest_review_time=SubqueryAggregate(
                            "project_reviews__timestamp", aggregate=Max
                        )
                    )
                    .annotate(
                        review_wait_time=F("latest_review_time")
                        - F("review_request_time")
                    )
                )

                step_data[item.id][
                    "average_review_wait_time"
                ] = review_requested_progress.aggregate(Avg("review_wait_time"))

                # (review_wait_time=F("review_request_time"))

        # REPORT STARTS HERE

        print(f"Total registrations: {registrations.count()}")

        import pprint

        pprint.pprint(step_data)
