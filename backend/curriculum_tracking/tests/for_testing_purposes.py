from curriculum_tracking.tests.factories import (
    ContentItemFactory,
    AgileCardFactory,
    RecruitProjectReviewFactory,
)
from curriculum_tracking.constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)
from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
)
from social_auth.tests.factories import SocialProfileFactory, GithubOAuthTokenFactory
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase


class CreatingDataForTesting:

    # One card with 4 reviews to follow
    card_1 = AgileCardFactory(
        status=AgileCard.IN_PROGRESS,
    )

    project_1 = card_1.recruit_project
    user = card_1.assignees.first()
    assert card_1.status == AgileCard.IN_PROGRESS
    assert project_1.content_item == card_1.content_item

    project_1.start_time = timezone.now() - timedelta(days=5)
    project_1.save()
    assert AgileCard.derive_status_from_project(project_1) == AgileCard.IN_PROGRESS

    request_review_time = project_1.start_time + timedelta(1)
    project_1.request_review(force_timestamp=request_review_time)
    time_one = project_1.start_time - timedelta(days=6)
    time_two = project_1.start_time + timedelta(days=4)
    time_three = project_1.start_time + timedelta(days=3)
    time_four = project_1.start_time + timedelta(days=2)

    # Four reviews are made at different times
    review_1 = RecruitProjectReviewFactory(
        status=NOT_YET_COMPETENT,
        recruit_project=project_1,
        timestamp=time_one
    )
    review_1.timestamp = time_one
    review_1.save()

    review_2 = RecruitProjectReviewFactory(
        status=COMPETENT,
        recruit_project=project_1,
    )
    review_2.timestamp = time_two
    review_2.save()

    review_3 = RecruitProjectReviewFactory(
        status=EXCELLENT,
        recruit_project=project_1,
    )
    review_3.timestamp = time_three
    review_3.save()

    review_4 = RecruitProjectReviewFactory(
        status=NOT_YET_COMPETENT,
        recruit_project=project_1,
    )
    review_4.timestamp = time_four
    review_4.save()


    # Three cards in the IN_PROGRESS column
    content_item = ContentItemFactory(
        content_type=ContentItem.PROJECT,
        project_submission_type=ContentItem.REPOSITORY,
    )

    card_2 = ContentItemFactory(
        content_item=content_item,
        status=AgileCard.IN_PROGRESS,
        recruit_project=None,
    )

    card_3 = AgileCardFactory(
        content_item=content_item,
        status=AgileCard.IN_PROGRESS,
        recruit_project=None,
    )

    card_4 = AgileCardFactory(
        content_item=content_item,
        status=AgileCard.IN_PROGRESS,
        recruit_project=None,
    )

    assignee = SocialProfileFactory().user
    card_2.assignees.set([assignee])
    card_3.assignees.set([assignee])
    card_4.assignees.set([assignee])

    card_2.start_project()
    card_3.start_project()
    card_4.start_project()


    # Four cards in the COMPLETE column
    content_item = ContentItemFactory(
        content_type=ContentItem.TOPIC,
        project_submission_type=ContentItem.REPOSITORY,
    )

    card_5 = AgileCardFactory(
        content_item=content_item,
        status=AgileCard.COMPLETE,
        recruit_project=None,
    )

    card_6 = AgileCardFactory(
        content_item=content_item,
        status=AgileCard.COMPLETE,
        recruit_project=None,
    )

    card_7 = AgileCardFactory(
        content_item=content_item,
        status=AgileCard.COMPLETE,
        recruit_project=None,
    )

    card_8 = AgileCardFactory(
        content_item=content_item,
        status=AgileCard.COMPLETE,
        recruit_project=None,
    )

    assignee_ = SocialProfileFactory().user
    card_5.assignees.set([assignee_])
    card_6.assignees.set([assignee_])
    card_7.assignees.set([assignee_])
    card_8.assignees.set([assignee_])


    # Two cards in the IN_REVIEW column
    content_item = ContentItemFactory(
        content_type=ContentItem.TOPIC,
        project_submission_type=ContentItem.REPOSITORY,
    )

    card_9 = AgileCardFactory(
        content_item=content_item,
        status=AgileCard.IN_REVIEW,
        recruit_project=None,
    )

    card_10 = AgileCardFactory(
        content_item=content_item,
        status=AgileCard.IN_REVIEW,
        recruit_project=None,
    )

    assignee_ = SocialProfileFactory().user
    card_9.assignees.set([assignee_])
    card_10.assignees.set([assignee_])