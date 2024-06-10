from django.core.management.base import BaseCommand

from curriculum_tracking.models import RecruitProjectReview
from project_review_pricing.models import ProjectReviewPricingScore, reviewers
from django.utils import timezone

DAYS = 4 * 7  # (4 weeks)


class Command(BaseCommand):
    def handle(self, *args, **options):

        # first, calculate individual review scores
        reviews = RecruitProjectReview.objects.filter(
            timestamp__gte=timezone.now() - timezone.timedelta(days=DAYS)
        ).filter(reviewer_user__email__in=reviewers)

        total = len(reviews)
        for i, review in enumerate(reviews):
            print(f"Scoring review {i+1}/{total}")
            ProjectReviewPricingScore.get_or_create_and_calculate_score(
                project_review=review
            )
