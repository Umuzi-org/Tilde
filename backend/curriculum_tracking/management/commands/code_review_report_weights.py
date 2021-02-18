from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProjectReview
from django.utils.timezone import timedelta
import pandas as pd
from django.utils import timezone


def generate_report():
    today = timezone.now().date()

    headings = ["date", "email", "is_staff", "story_points", "count"]

    df = pd.DataFrame(columns=headings)

    for day in range(7):
        maximum = today - timedelta(days=day)
        minimum = maximum - timedelta(days=1)
        # heading = minimum.strftime("%a %d %b")
        all_reviews = RecruitProjectReview.objects.filter(
            timestamp__gte=minimum
        ).filter(timestamp__lte=maximum)
        for o in all_reviews:
            df = df.append(
                [
                    {
                        "date": minimum,
                        "is_staff": o.reviewer_user.is_staff,
                        "email": o.reviewer_user.email,
                        "story_points": o.recruit_project.content_item.story_points,
                        "count": 1,
                    }
                ]
            )

    df_counts = (
        df.groupby(["date", "email"])
        .sum()
        .reset_index()
        .sort_values(by=["story_points", "count"], ascending=False)
    )
    df_counts["is_staff"] = df_counts.is_staff.astype("bool")
    return df_counts


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = timezone.now().date()

        df = generate_report()
        df.to_csv(f"gitignore/code_reviews {today.strftime('%a %d %b %Y')}.csv")
