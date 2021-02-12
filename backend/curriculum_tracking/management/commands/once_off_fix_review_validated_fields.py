from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProjectReview


class Command(BaseCommand):
    def handle(self, *args, **options):
        reviews = RecruitProjectReview.objects.order_by("pk")
        total = reviews.count()

        for i, review in enumerate(reviews):
            print(f"CLEARING: {i+1}/{total}: {review.id} {review}")
            review.validated = None
            review.save()

        for i, review in enumerate(reviews):
            print(f"PROPOGATING: {i+1}/{total}: {review.id} {review}")
            review.update_recent_validation_flags_for_project()