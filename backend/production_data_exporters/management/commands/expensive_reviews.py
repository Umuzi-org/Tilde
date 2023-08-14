from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProjectReview
from django.utils import timezone
from curriculum_tracking.constants import NOT_YET_COMPETENT
from django.db.models import Count, Sum
from backend.settings import CURRICULUM_TRACKING_REVIEW_BOT_EMAIL
from django.db.models import Q
from django.db.models.functions import Length

TODO: make use of pull request review comments 

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_reviews = (
            RecruitProjectReview.objects.filter(
                timestamp__gt=timezone.now() - timezone.timedelta(days=360)
            )
            .filter(status=NOT_YET_COMPETENT)
            .prefetch_related("recruit_project__content_item")
        )

        human_reviews = all_reviews.filter(
            ~Q(reviewer_user__email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL)
        )

        bot_reviews = all_reviews.filter(
            reviewer_user__email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL
        )

        for query, name in zip(
            [all_reviews, human_reviews, bot_reviews], ["all", "human", "bot"]
        ):
            print(f"\n{name}")

            counts = (
                query.values("recruit_project__content_item__title")
                .annotate(count=Count("recruit_project__content_item__title"))
                .order_by("-count")
            )

            for d in counts[:50]:
                print(
                    f"count={d['count']} title={d['recruit_project__content_item__title']}"
                )

        # assume that if people leave long reviews it's more effort.
        # so sum up the length of all the NYC comments

        human_reviews = human_reviews.annotate(comment_length=Length("comments"))
        lengths = (
            human_reviews.values("recruit_project__content_item__title")
            .annotate(total_length=Sum("comment_length"))
            .order_by("-total_length")
        )

        print(f"\nTotal comment length for human reviews")

        min = lengths[50]["total_length"]
        for d in lengths[:50]:
            print(
                f"normalised len={d['total_length']/min} title={d['recruit_project__content_item__title']}"
            )
