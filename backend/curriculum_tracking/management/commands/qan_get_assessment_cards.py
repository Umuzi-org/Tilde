from django.core.management.base import BaseCommand
from core.models import User
from curriculum_tracking.models import RecruitProject
from taggit.models import Tag


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who", type=str)

    def handle(self, *args, **options):
        who = options["who"]
        users = User.get_users_from_identifier(who)
        tag = Tag.objects.get(name="technical-assessment")

        for user in users:
            print(user.email)

            assessments = RecruitProject.objects.filter(
                recruit_users__in=[user]
            ).filter(content_item__tags__in=[tag])
            for assessment in assessments:
                if assessment.complete_time:
                    status = "complete"
                elif assessment.review_request_time:
                    status = "in review"
                elif assessment.start_time:
                    status = "in progrogress"
                else:
                    status = "not started"
                print(f"\t{status} {assessment.title} {assessment.review_request_time}")
