from django.core.management.base import BaseCommand

from zero_marginal_cost_challenges.models import ChallengeRegistration
from curriculum_tracking.models import (
    Curriculum,
    RecruitProject,
    ContentItem,
    TopicProgress,
)
from django.db.models import Avg, F, Max
from sql_util.utils import SubqueryAggregate
import json
from django.db.models import Q

from curriculum_tracking.constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
    RED_FLAG,
)

WAITING = "waiting"
STARTED = "started"
COMPLETE = "complete"


def get_progress(item):
    if item.content_type == ContentItem.PROJECT:
        return RecruitProject.objects.filter(content_item=item)
    if item.content_type == ContentItem.TOPIC:
        return TopicProgress.objects.filter(content_item=item)


def get_user(progress):
    if progress.content_type == ContentItem.PROJECT:
        return progress.recruit_users.first()
    else:
        return progress.user


def get_review_count(progress):
    """returns total, positive, negative"""
    if progress.content_type == ContentItem.PROJECT:
        positive = progress.project_reviews.filter(
            Q(status=COMPETENT) | Q(status=EXCELLENT)
        ).count()
        negative = progress.project_reviews.filter(
            Q(status=NOT_YET_COMPETENT) | Q(status=RED_FLAG)
        ).count()
        return progress.project_reviews.count(), positive, negative
    return 0, 0, 0


class Command(BaseCommand):
    def handle(self, *args, **options):
        # for now we only have one challenge so we just add some sanity checking. This check will fail once we have more than one challenge
        curriculum = Curriculum.objects.get(pk=90)
        assert (
            ChallengeRegistration.objects.all().count()
            == ChallengeRegistration.objects.filter(curriculum_id=curriculum.id).count()
        ), "looks like we have multiple challenges. yay. Implement better stats now"

        registrations = ChallengeRegistration.objects.all()
        users = {o.user.email: {} for o in registrations}

        content_items = [
            o.content_item
            for o in curriculum.content_requirements.order_by("order").prefetch_related(
                "content_item"
            )
        ]

        # step_data = {}

        for i, item in enumerate(content_items):
            print(f"{i+1}/{len(content_items)} {item.title}")

            step = f"{i+1}"
            if len(step) == 1:
                step = f"0{step}"
            title = f"{step}. {item.title}"
            for email in users:
                users[email][title] = {"status": WAITING}

            progress = get_progress(item)

            for p in progress:
                user = get_user(p)
                total_reviews, positive, negative = get_review_count(p)
                users[user.email][title] = {
                    "total_reviews": total_reviews,
                    "positive_reviews": positive,
                    "negative_reviews": negative,
                }
                if p.complete_time:
                    users[user.email][title]["status"] = COMPLETE
                elif p.start_time:
                    users[user.email][title]["status"] = STARTED

        # import pprint

        # pprint.pprint(users)

        total_complete = 0

        for user in users:
            number_of_steps = len(users[user])
            number_complete = sum(
                [1 for o in users[user].values() if o["status"] == COMPLETE]
            )

            completed = f"completed: {number_complete}/{number_of_steps}"
            total_reviews_str = f"total reviews: {sum([o.get('total_reviews',0) for o in users[user].values()])}"
            negative_reviews_str = f"negative reviews: {sum([o.get('negative_reviews',0) for o in users[user].values()])}"
            positive_reviews_str = f"positive reviews: {sum([o.get('positive_reviews',0) for o in users[user].values()])}"

            print(
                "\n\t".join(
                    [
                        user,
                        completed,
                        total_reviews_str,
                        negative_reviews_str,
                        positive_reviews_str,
                    ]
                )
            )
            total_complete += number_complete

        print(f"TOTAL COMPLETED: {total_complete}")
        print(f"TOTAL REGISTRATIONS: {registrations.count()}")
