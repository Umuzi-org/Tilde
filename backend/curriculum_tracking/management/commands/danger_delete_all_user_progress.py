from django.core.management.base import BaseCommand
from curriculum_tracking import models

from core.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)

    def handle(self, *args, **options):
        user = None
        who = options["who"]

        user = User.objects.get(email=who)
        models.AgileCard.objects.filter(assignees__in=[user]).delete()
        models.RecruitProject.objects.filter(recruit_users__in=[user]).delete()
        models.TopicProgress.objects.filter(user=user).delete()
        models.WorkshopAttendance.objects.filter(attendee_user=user).delete()
