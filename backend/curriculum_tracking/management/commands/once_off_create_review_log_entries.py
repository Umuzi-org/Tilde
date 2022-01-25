from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProjectReview, TopicReview
import curriculum_tracking.activity_log_entry_creators as creators

# from django.contrib.contenttypes.models import ContentType

from git_real.models import PullRequestReview
from git_real.activity_log_creators import log_pr_reviewed


class Command(BaseCommand):
    def handle(self, *args, **options):
        # total = RecruitProjectReview.objects.count()
        # for i, review in enumerate(RecruitProjectReview.objects.all()):
        #     print(f"project review: {i+1}/{total}")
        #     creators.log_project_competence_review_done(review)

        # total = TopicReview.objects.count()
        # for i, review in enumerate(TopicReview.objects.all()):
        #     print(f"topic review: {i+1}/{total}")
        #     creators.log_topic_competence_review_done(review)

        total = PullRequestReview.objects.count()
        for i, review in enumerate(PullRequestReview.objects.all()):
            print(f"pr review: {i+1}/{total}")
            log_pr_reviewed(review)
