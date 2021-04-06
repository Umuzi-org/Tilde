from django.core.management.base import BaseCommand

# from core.models import User
from curriculum_tracking.models import AgileCard, RecruitProject


class Command(BaseCommand):
    def handle(self, *args, **options):

        # if a user is inactive and is meant to review a card or project, then remove them
        for card in AgileCard.objects.filter(reviewers__active__in=[False]):
            for user in card.reviewers.filter(active=False):
                # breakpoint()
                card.reviewers.remove(user)

        for project in RecruitProject.objects.filter(
            reviewer_users__active__in=[False]
        ):
            for user in project.reviewer_users.filter(active=False):
                project.reviewer_users.remove(user)

        # if a project or card is assigned to a user that is not active, noboduy needs to review it
        for project in RecruitProject.objects.filter(recruit_users__active__in=[False]):
            project.reviewer_users.set([])

        for card in AgileCard.objects.filter(assignees__active__in=[False]):
            card.reviewers.set([])
