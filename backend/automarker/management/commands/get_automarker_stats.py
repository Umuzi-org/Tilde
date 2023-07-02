from django.core.management.base import BaseCommand
from django.db.models import Q

from curriculum_tracking.models import RecruitProjectReview
from automarker.models import ContentItemAutoMarkerConfig
import json
from backend.settings import (
    CURRICULUM_TRACKING_REVIEW_BOT_EMAIL,
    CURRICULUM_TRACKING_TRUSTED_REVIEW_BOT_EMAIL,
)
from django.utils import timezone

from curriculum_tracking.constants import (
    COMPETENT,
    NOT_YET_COMPETENT,
    EXCELLENT,
    RED_FLAG,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        report = {}

        all_configs = ContentItemAutoMarkerConfig.objects.all()

        report["total_configs"] = all_configs.count()

        for mode, _ in ContentItemAutoMarkerConfig.MODES:
            report[f"total {mode} configs"] = all_configs.filter(mode=mode).count()

        # review counts

        cutoff_times_days = [30, 90]
        now = timezone.now()

        cutoff_timestamps = [
            now - timezone.timedelta(days=days) for days in cutoff_times_days
        ]

        # for email in [CURRICULUM_TRACKING_REVIEW_BOT_EMAIL,
        # CURRICULUM_TRACKING_TRUSTED_REVIEW_BOT_EMAIL]:

        all_reviews = RecruitProjectReview.objects.filter(
            Q(reviewer_user__email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL)
            | Q(reviewer_user__email=CURRICULUM_TRACKING_TRUSTED_REVIEW_BOT_EMAIL)
        )

        for days, timestamp in zip(cutoff_times_days, cutoff_timestamps):
            total = all_reviews.filter(timestamp__gte=timestamp)
            positive = total.filter(Q(status=COMPETENT) | Q(status=EXCELLENT))
            negative = total.filter(Q(status=NOT_YET_COMPETENT) | Q(status=RED_FLAG))

            report[f"bot_reviews_last_{days}_days_TOTAL"] = total.count()
            report[f"bot_reviews_last_{days}_days_POSITIVE"] = positive.count()
            report[f"bot_reviews_last_{days}_days_NEGATIVE"] = negative.count()

        print(json.dumps(report, indent=2, sort_keys=True))
