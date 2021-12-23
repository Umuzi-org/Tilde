from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProjectReview, TopicReview
import curriculum_tracking.activity_log_entry_creators as creators
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    def handle(self, *args, **options):
        for review in RecruitProjectReview.objects.all():
            creators.log_project_competence_review_done(review)
        for review in TopicReview.objects.all():
            creators.log_project_competence_review_done(review)
