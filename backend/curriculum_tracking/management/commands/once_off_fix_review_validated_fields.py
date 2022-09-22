from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProjectReview


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("id__gte", type=int, nargs="?", default=1)

    def handle(self, *args, **options):

        reviews = RecruitProjectReview.objects.order_by("pk").filter(
            id__gte=options["id__gte"]
        )
        total = reviews.count()

        # reviews.update(validated=None)

        for i, review in enumerate(reviews):
            print(f"PROPAGATING: {i+1}/{total}: [{review.id}] {review}")
            review.update_recent_validation_flags_for_project()
