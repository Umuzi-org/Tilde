from django.core.management.base import BaseCommand

from curriculum_tracking.models import RecruitProjectReview


class Command(BaseCommand):
    def handle(self, *args, **options):
        unstarted = RecruitProjectReview.objects.filter(
            recruit_project__start_time__isnull=True
        ).prefetch_related("recruit_project")

        count = unstarted.count()
        for i, o in enumerate(unstarted):
            print(f"{i+1} / {count}")
            project = o.recruit_project
            project.start_time = o.timestamp
            project.save()