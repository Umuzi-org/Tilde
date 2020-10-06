from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProjectReview, AgileCard, ContentItem
from core.models import RecruitCohort, User
from django.utils.timezone import datetime, timedelta
import os
from pathlib import Path
import csv

today = datetime.now().date()


def recruit_report():
    results = []
    # date_headings = []

    today = datetime.now().date()

    for recruit_cohort in (
        RecruitCohort.objects.filter(user__active=True)
        .filter(cohort__active=True)
        .prefetch_related("user")
        .prefetch_related("cohort")
        .prefetch_related("cohort__cohort_curriculum")
    ):
        user = recruit_cohort.user
        if not user.active:
            continue

        print(user)

        user_data = {
            "user": user.email,
            "cohort": str(recruit_cohort.cohort),
            "employer_partner": recruit_cohort.employer_partner,
            "in review card_count": (
                AgileCard.objects.filter(status=AgileCard.IN_REVIEW)
                .filter(reviewers__in=[user])
                .count()
            ),
            "complete project card_count": (
                AgileCard.objects.filter(status=AgileCard.IN_REVIEW)
                .filter(assignees__in=[user])
                .filter(content_item__content_type=ContentItem.PROJECT)
                .count()
            ),
        }
        add_daily_review_counts(user, user_data)

        # total = 0
        # for day in range(7):
        #     maximum = today - timedelta(days=day)
        #     minimum = maximum - timedelta(days=1)
        #     count = (
        #         RecruitProjectReview.objects.filter(reviewer_user=user)
        #         .filter(timestamp__gte=minimum)
        #         .filter(timestamp__lte=maximum)
        #         .count()
        #     )
        #     # if count:
        #     #     breakpoint()
        #     heading = minimum.strftime("%a %d %b")
        #     date_headings.append(heading)
        #     user_data[heading] = count
        #     total = total + count

        # user_data["total reviews"] = total

        results.append(user_data)

    os.makedirs("gitignore", exist_ok=True)
    results.sort(key=lambda d: d["total reviews"])
    with open(
        Path(f"gitignore/recruit_reviews_{today.strftime('%a %d %b %Y')}.csv"), "w"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(user_data.keys())
        writer.writerows([d.values() for d in results])


def add_daily_review_counts(user, user_data):
    total = 0
    for day in range(7):
        maximum = today - timedelta(days=day)
        minimum = maximum - timedelta(days=1)
        count = (
            RecruitProjectReview.objects.filter(reviewer_user=user)
            .filter(timestamp__gte=minimum)
            .filter(timestamp__lte=maximum)
            .count()
        )
        # if count:
        #     breakpoint()
        heading = minimum.strftime("%a %d %b")
        # date_headings.append(heading)
        user_data[heading] = count
        total = total + count

    user_data["total reviews"] = total


def staff_report():
    # date_headings = []
    results = []
    for user in User.objects.filter(is_staff=True, active=True):
        print(user)
        user_data = {
            "user": user.email,
        }

        add_daily_review_counts(user, user_data)

        results.append(user_data)

    os.makedirs("gitignore", exist_ok=True)
    results.sort(key=lambda d: d["total reviews"])
    with open(
        Path(f"gitignore/staff_reviews_{today.strftime('%a %d %b %Y')}.csv"), "w"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(user_data.keys())
        writer.writerows([d.values() for d in results])


class Command(BaseCommand):
    def handle(self, *args, **options):
        recruit_report()
        staff_report()
