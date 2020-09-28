from django.core.management.base import BaseCommand

from curriculum_tracking.models import RecruitProject, RecruitProjectReview
from curriculum_tracking.constants import (
    RED_FLAG,
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for project in RecruitProject.objects.all().prefetch_related("project_reviews"):

            if project.review_request_time == None:
                continue
            counts = {status[0]: 0 for status in RecruitProjectReview.STATUS_CHOICES}
            reviews = project.project_reviews.filter(
                timestamp__gt=project.review_request_time
            )
            for o in reviews:
                if o.status == "":
                    continue
                counts[o.status] += 1

            # now assign the count values to the right fields

            project.code_review_competent_since_last_review_request = counts[COMPETENT]
            project.code_review_excellent_since_last_review_request = counts[EXCELLENT]
            project.code_review_red_flag_since_last_review_request = counts[RED_FLAG]
            project.code_review_ny_competent_since_last_review_request = counts[
                NOT_YET_COMPETENT
            ]
            project.save()

