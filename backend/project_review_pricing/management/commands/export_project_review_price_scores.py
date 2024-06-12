from django.core.management.base import BaseCommand

from project_review_pricing.models import ProjectReviewPricingScore
import csv

DATETIME_FORMAT = "%m/%d/%Y, %H:%M:%S"


class Command(BaseCommand):
    def handle(self, *args, **options):
        score_instances = (
            ProjectReviewPricingScore.objects.filter(
                project_review__recruit_project__complete_time__isnull=False
            )
            .order_by("project_review__timestamp")
            .prefetch_related("project_review")
            .prefetch_related("project_review__recruit_project")
        )

        with open("gitignore/review_work_scores.csv", "w") as f:
            writer = csv.writer(f)
            headings = [
                "review timestamp",
                "project complete timestamp",
                "title",
                "flavours",
                "reviewer",
                "score",
                "weight",
            ]
            writer.writerow(headings)
            for o in score_instances:
                review = o.project_review
                project = review.recruit_project
                writer.writerow(
                    [
                        review.timestamp.strftime(DATETIME_FORMAT),
                        project.complete_time.strftime(DATETIME_FORMAT),
                        project.content_item.title,
                        ",".join(project.flavour_names),
                        review.reviewer_user.email,
                        o.score,
                        o.weight_share,
                    ]
                )
