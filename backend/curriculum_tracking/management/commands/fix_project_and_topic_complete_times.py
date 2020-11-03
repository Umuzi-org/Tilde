#update the completed time on all projects and topics

from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProject,AgileCard,RecruitProjectReview
from curriculum_tracking.constants import REVIEW_STATUS_CHOICES




def fix_complete_times():
    cards = AgileCard.objects.filter(status=AgileCard.COMPLETE)

    for card in cards:
        project = card.recruit_project
        topic = card.topic_progress
        if project:
            project.complete_time = project.latest_review()

        if topic:
            topic.complete_time = topic.latest_review()

        project.save()
        topic.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        fix_complete_times()