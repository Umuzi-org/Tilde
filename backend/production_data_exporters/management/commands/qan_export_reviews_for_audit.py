from django.core.management.base import BaseCommand

from core.models import Team
from curriculum_tracking.models import RecruitProjectReview
from git_real.models import PullRequestReview
from django.utils import timezone
import csv


WEEKS = 4


class Command(BaseCommand):
    def handle(self, *args, **options):
        team = Team.objects.get(name="Staff Tech Education")
        users = team.user_set.all()

        user_stats = []
        for user in users:
            print(user.email)
            reviews = RecruitProjectReview.objects.filter(reviewer_user=user)
            pr_reviews = PullRequestReview.objects.filter(user=user)

            row = [user.email]

            for week in range(WEEKS):
                end_date = timezone.now() - timezone.timedelta(days=7 * week)
                start_date = timezone.now() - timezone.timedelta(days=7 * (week + 1))

                week_pr_reviews = pr_reviews.filter(
                    submitted_at__range=(start_date, end_date)
                )

                week_reviews_total = reviews.filter(
                    timestamp__range=(start_date, end_date)
                )
                week_reviews_contradicted = week_reviews_total.filter(
                    validated=RecruitProjectReview.CONTRADICTED
                )
                week_reviews_correct = week_reviews_total.filter(
                    validated=RecruitProjectReview.CORRECT
                )
                week_reviews_incorrect = week_reviews_total.filter(
                    validated=RecruitProjectReview.INCORRECT
                )
                week_reviews_unknown = week_reviews_total.filter(validated__isnull=True)

                row.append(week_pr_reviews.count())
                row.append(week_reviews_total.count())
                row.append(week_reviews_contradicted.count())
                row.append(week_reviews_incorrect.count())
                row.append(week_reviews_correct.count())
                row.append(week_reviews_unknown.count())

            user_stats.append(row)

        headings = [
            "user",
        ]
        for week in range(WEEKS):
            start_date = timezone.now() - timezone.timedelta(days=7 * (week + 1))
            start_date = start_date.strftime("%Y-%m-%d")

            headings.extend(
                [
                    f"{start_date} - {s}"
                    for s in [
                        "pr reviews",
                        "total reviews",
                        "contradicted",
                        "incorrect",
                        "correct",
                        "unknown",
                    ]
                ]
            )

        with open("gitignore/review_stats.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows(user_stats)
