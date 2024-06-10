from django.core.management.base import BaseCommand
from django.db.models import Q
from curriculum_tracking.models import RecruitProjectReview, RecruitProject
from project_review_pricing.models import ProjectReviewPricingScore, reviewers
from django.utils import timezone

DAYS = 4 * 7  # (4 weeks)

SKIP_TAGS = ["ncit", "technical-assessment", "close_on_peer_reviews", "ncba"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff = timezone.now() - timezone.timedelta(days=DAYS)

        # first, calculate individual review scores
        # reviews = (
        #     RecruitProjectReview.objects.filter(
        #         timestamp__gte=cutoff
        #     )
        #     .filter(reviewer_user__email__in=reviewers)
        #     .order_by("timestamp")
        # )

        projects = (
            RecruitProject.objects.filter(complete_time__gte=cutoff)
            .filter(~Q(content_item__tags__name__in=SKIP_TAGS))
            .order_by("complete_time")
        )

        total = len(projects)
        for i, project in enumerate(projects):
            print(f"Scoring reviews for project {i+1}/{total}")
            if i <= 22:
                continue

            ProjectReviewPricingScore.calculate_weight_shares_for_project(project)
