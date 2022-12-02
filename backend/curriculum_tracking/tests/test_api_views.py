# from backend.curriculum_tracking.models import AgileCard
from git_real.models import PullRequestReview
from git_real.tests.factories import PullRequestFactory, PullRequestReviewFactory
from rest_framework.test import APITestCase
from guardian.shortcuts import assign_perm
from test_mixins import APITestCaseMixin
from core.tests.factories import UserFactory, TeamFactory
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from . import factories
from datetime import timedelta
from curriculum_tracking.models import (
    ContentItem,
    RecruitProjectReview,
    AgileCard,
    ContentItemAgileWeight,
    RecruitProject,
)
from taggit.models import Tag
from curriculum_tracking.constants import NOT_YET_COMPETENT
from . import factories
from curriculum_tracking.tests.factories import (
    RecruitProjectFactory,
    AgileCardFactory,
    TagFactory,
)
from curriculum_tracking.management.helpers import get_team_cards
from core.models import Team
from django.contrib.auth.models import Group


class CardSummaryViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "cardsummary-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    FIELDS_THAT_CAN_BE_FALSEY = [
        "code_review_competent_since_last_review_request",
        "code_review_excellent_since_last_review_request",
        "code_review_red_flag_since_last_review_request",
        "code_review_ny_competent_since_last_review_request",
        "due_time",
        "complete_time",
        "review_request_time",
        "start_time",
        "open_pr_count",
        "oldest_open_pr_updated_time",
    ]

    def verbose_instance_factory(self):
        project = factories.RecruitProjectFactory(
            due_time=timezone.now(), review_request_time=timezone.now()
        )
        card = factories.AgileCardFactory(recruit_project=project)
        card.reviewers.add(UserFactory())
        card.assignees.add(UserFactory())
        return card


class TopicProgressViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "topicprogress-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    FIELDS_THAT_CAN_BE_FALSEY = [
        "due_time",
        "start_time",
        "complete_time",
        "review_request_time",
        "topic_reviews",
    ]

    def verbose_instance_factory(self):

        topic_progress = factories.TopicProgressFactory()
        content = topic_progress.content_item
        content.topic_needs_review = True
        content.save()
        return topic_progress


class RequestAndCancelReviewViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True
    FIELDS_THAT_CAN_BE_FALSEY = [
        "code_review_competent_since_last_review_request",
        "code_review_excellent_since_last_review_request",
        "code_review_red_flag_since_last_review_request",
        "code_review_ny_competent_since_last_review_request",
        "requires_cards",
        "required_by_cards",
        "project_submission_type_nice",
        "topic_needs_review",
        "topic_progress",
        "due_time",
        "complete_time",
        "review_request_time",
        "start_time",
        "tag_names",
        "can_start",
        "can_force_start",
        # "open_pr_count",
    ]

    def setUp(self):
        self.content_item = factories.ProjectContentItemFactory(
            project_submission_type=ContentItem.LINK, template_repo=None
        )
        self.card_1 = factories.AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=factories.RecruitProjectFactory(
                content_item=self.content_item
            ),
            content_item=self.content_item,
        )

        self.card_2 = factories.AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=factories.RecruitProjectFactory(
                content_item=self.content_item
            ),
            content_item=self.content_item,
        )

        self.card_1.start_project()
        self.card_2.start_project()

        self.login_as_superuser()
        request_review_url = f"{self.get_instance_url(self.card_2.id)}request_review/"
        self.client.post(request_review_url)
        self.card_2.refresh_from_db()

    def test_request_review_permissions_non_superuser_staff(self):
        self.assertEqual(self.card_1.status, AgileCard.IN_PROGRESS)
        staff_user = factories.UserFactory(is_superuser=False, is_staff=True)
        self.login(staff_user)

        request_review_url = f"{self.get_instance_url(self.card_1.id)}request_review/"
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        self.card_1.refresh_from_db()
        self.assertEqual(self.card_1.status, AgileCard.IN_PROGRESS)

    def test_request_review_permissions_non_assignee(self):
        self.assertEqual(self.card_1.status, AgileCard.IN_PROGRESS)
        recruit_user_non_card_assignee = factories.UserFactory(
            is_superuser=False, is_staff=False
        )
        self.login(recruit_user_non_card_assignee)
        request_review_url = f"{self.get_instance_url(self.card_1.id)}request_review/"
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        self.card_1.refresh_from_db()
        self.assertEqual(self.card_1.status, AgileCard.IN_PROGRESS)

    def test_request_review_permissions_superuser(self):
        self.assertEqual(self.card_1.status, AgileCard.IN_PROGRESS)
        superuser = factories.UserFactory(is_superuser=True, is_staff=False)
        self.login(superuser)
        request_review_url = f"{self.get_instance_url(self.card_1.id)}request_review/"
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 200)

        self.card_1.refresh_from_db()
        self.assertEqual(self.card_1.status, AgileCard.IN_REVIEW)

    def test_request_review_permissions_assignee(self):
        self.assertEqual(self.card_1.status, AgileCard.IN_PROGRESS)
        self.login(self.card_1.assignees.first())
        request_review_url = f"{self.get_instance_url(self.card_1.id)}request_review/"
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 200)

        self.card_1.refresh_from_db()
        self.assertEqual(self.card_1.status, AgileCard.IN_REVIEW)

    def test_cancel_request_review_permissions_non_superuser_staff(self):
        self.assertEqual(self.card_2.status, AgileCard.IN_REVIEW)

        staff_user = factories.UserFactory(is_superuser=False, is_staff=True)
        self.login(staff_user)

        cancel_request_review_url = (
            f"{self.get_instance_url(self.card_2.id)}cancel_review_request/"
        )
        response = self.client.post(cancel_request_review_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        self.card_2.refresh_from_db()
        self.assertEqual(self.card_2.status, AgileCard.IN_REVIEW)

    def test_cancel_request_review_permissions_non_assignee(self):
        self.assertEqual(self.card_2.status, AgileCard.IN_REVIEW)
        recruit_user_non_card_assignee = factories.UserFactory(
            is_superuser=False, is_staff=False
        )
        self.login(recruit_user_non_card_assignee)

        cancel_request_review_url = (
            f"{self.get_instance_url(self.card_2.id)}cancel_review_request/"
        )
        response = self.client.post(cancel_request_review_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        self.card_2.refresh_from_db()
        self.assertEqual(self.card_2.status, AgileCard.IN_REVIEW)

    def test_cancel_request_review_permissions_superuser(self):
        self.assertEqual(self.card_2.status, AgileCard.IN_REVIEW)
        superuser = factories.UserFactory(is_superuser=True, is_staff=False)
        self.login(superuser)
        cancel_request_review_url = (
            f"{self.get_instance_url(self.card_2.id)}cancel_review_request/"
        )
        response = self.client.post(cancel_request_review_url)

        self.assertEqual(response.status_code, 200)

        self.card_2.refresh_from_db()
        self.assertEqual(self.card_2.status, AgileCard.IN_PROGRESS)

    def test_cancel_request_review_permissions_assignee(self):
        self.assertEqual(self.card_2.status, AgileCard.IN_REVIEW)
        self.login(self.card_2.assignees.first())
        request_review_url = (
            f"{self.get_instance_url(self.card_2.id)}cancel_review_request/"
        )
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 200)

        self.card_2.refresh_from_db()
        self.assertEqual(self.card_2.status, AgileCard.IN_PROGRESS)

    def test_cancel_request_review_card_with_review_feedback(self):
        self.assertEqual(self.card_2.status, AgileCard.IN_REVIEW)

        add_review_url = f"{self.get_instance_url(self.card_2.id)}add_review/"
        response = self.client.post(
            add_review_url, data={"status": NOT_YET_COMPETENT, "comments": "boooo"}
        )
        self.assertEqual(response.status_code, 200)

        self.card_2.refresh_from_db()
        self.assertEqual(self.card_2.status, AgileCard.REVIEW_FEEDBACK)

        request_review_url = f"{self.get_instance_url(self.card_2.id)}request_review/"
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 200)

        self.card_2.refresh_from_db()
        self.assertEqual(self.card_2.status, AgileCard.IN_REVIEW)

        cancel_request_review_url = (
            f"{self.get_instance_url(self.card_2.id)}cancel_review_request/"
        )
        response = self.client.post(cancel_request_review_url)

        self.assertEqual(response.status_code, 200)

        self.card_2.refresh_from_db()
        self.assertEqual(self.card_2.status, AgileCard.REVIEW_FEEDBACK)


class AgileCardViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    FIELDS_THAT_CAN_BE_FALSEY = [
        "code_review_competent_since_last_review_request",
        "code_review_excellent_since_last_review_request",
        "code_review_red_flag_since_last_review_request",
        "code_review_ny_competent_since_last_review_request",
        "requires_cards",
        "required_by_cards",
        "project_submission_type_nice",
        "topic_needs_review",
        "topic_progress",
        "due_time",
        "complete_time",
        "review_request_time",
        "start_time",
        "tag_names",
        "can_start",
        "can_force_start",
        "project_link_submission",
        # "open_pr_count",
        "users_that_reviewed_open_prs",
        "users_that_reviewed_open_prs_emails",
    ]

    def verbose_instance_factory(self):
        project = factories.RecruitProjectFactory()
        card = factories.AgileCardFactory(recruit_project=project)
        card.reviewers.add(UserFactory())
        card.assignees.add(UserFactory())
        card.flavours.add(Tag.objects.create(name="asdsasa"))
        project.review_request_time = timezone.now() - timedelta(days=5)
        project.save()
        review = factories.RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT,
            recruit_project=project,
        )
        review.timestamp = timezone.now() - timedelta(days=1)
        review.save()

        PullRequestFactory(repository=project.repository)

        return card

    def test_set_project_card_due_time_permissions(self):
        card = factories.AgileCardFactory(
            content_item=factories.ProjectContentItemFactory(),
            recruit_project=None,  # things can have due dates even when not started
        )
        self._test_set_due_time_permissions(card, lambda card: card.recruit_project)

    def test_set_topic_card_due_time_permissions(self):
        card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC)
        )
        self._test_set_due_time_permissions(card, lambda card: card.topic_progress)

    def _test_set_due_time_permissions(self, card, get_progress):
        recruit = UserFactory()

        staff_member = UserFactory(is_staff=True)

        card.assignees.add(recruit)

        due_time_1 = timezone.now() + timedelta(days=7)
        due_time_2 = timezone.now() + timedelta(days=1)

        url = reverse("agilecard-set-card-due-time", kwargs={"pk": card.id})

        self.login(UserFactory())

        response = self.client.post(url, data={"due_time": due_time_1})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        self.login(recruit)

        response = self.client.post(url, data={"due_time": due_time_1})

        self.assertEqual(response.status_code, 200)

        card.refresh_from_db()
        progress = get_progress(card)

        self.assertEqual(progress.due_time.strftime("%c"), due_time_1.strftime("%c"))

        response = self.client.post(url, data={"due_time": due_time_1})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        self.login(staff_member)
        response = self.client.post(url, data={"due_time": due_time_2})

        self.assertEqual(response.status_code, 200)

        progress.refresh_from_db()
        self.assertEqual(progress.due_time.strftime("%c"), due_time_2.strftime("%c"))

    def test_list_assignees_permissions_on_list(self):
        recruit = UserFactory(is_superuser=False, is_staff=False)
        self.login(recruit)
        url = self.get_list_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        url2 = f"{url}?assignees=12345"
        response = self.client.get(url2)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        url3 = f"{url}?assignees={recruit.id}"
        response = self.client.get(url3)
        self.assertEqual(response.status_code, 200)

    def test_list_reviewers_permissions_on_list(self):
        recruit = UserFactory(is_superuser=False, is_staff=False)
        self.login(recruit)
        url = self.get_list_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        url2 = f"{url}?reviewers=12345"
        response = self.client.get(url2)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        url3 = f"{url}?reviewers={recruit.id}"
        response = self.client.get(url3)
        self.assertNotIn("detail", response.data)
        self.assertEqual(response.status_code, 200)

    def test_set_project_link(self):
        content_item = factories.ContentItemFactory(
            content_type=ContentItem.PROJECT, project_submission_type=ContentItem.LINK
        )

        recruit = UserFactory(is_superuser=False, is_staff=False)

        card = factories.AgileCardFactory(content_item=content_item)

        card.assignees.add(recruit)

        url = f"{self.get_list_url()}{card.id}/set_project_link/"

        link_1 = "https://wnning.com"
        link_2 = "https://wnning.com/boom"
        self.login(recruit)

        response = self.client.post(url, data={"link_submission": link_1})
        self.assertEqual(response.status_code, 200)

        project = card.recruit_project
        project.refresh_from_db()
        self.assertEqual(project.link_submission, link_1)

        response = self.client.post(url, data={"link_submission": link_2})
        project.refresh_from_db()
        self.assertEqual(project.link_submission, link_2)

        other_recruit = UserFactory(is_superuser=False, is_staff=False)

        self.login(other_recruit)
        response = self.client.post(url, data={"link_submission": link_1})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        project.refresh_from_db()
        self.assertEqual(project.link_submission, link_2)


class RecruitProjectViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "recruitproject-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    FIELDS_THAT_CAN_BE_FALSEY = ["link_submission", "complete_time"]

    def verbose_instance_factory(self):
        project = factories.RecruitProjectInReviewFactory(
            content_item=factories.ProjectContentItemFactory(
                project_submission_type=ContentItem.REPOSITORY,
            )
        )
        factories.RecruitProjectReviewFactory(recruit_project=project)
        project.reviewer_users.add(UserFactory())
        factories.AgileCardFactory(recruit_project=project)
        return project

    def test_list_recruit_permissions_on_list(self):
        recruit = UserFactory(is_superuser=False, is_staff=False)
        self.login(recruit)
        url = self.get_list_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        url2 = f"{url}?recruit_users=12345"
        response = self.client.get(url2)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")

        url3 = f"{url}?recruit_users={recruit.id}"
        response = self.client.get(url3)
        self.assertNotIn("detail", response.data)
        self.assertEqual(response.status_code, 200)


class PullRequestReviewQualityViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "pullrequestreviewquality-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    FIELDS_THAT_CAN_BE_FALSEY = ["agile_card"]

    def verbose_instance_factory(self):
        pr_review = PullRequestReviewFactory(validated=PullRequestReview.CONTRADICTED)
        project = RecruitProjectFactory(repository=pr_review.pull_request.repository)
        project.set_flavours(["js"])

        weight = factories.ContentItemAgileWeightFactory(
            content_item=project.content_item
        )
        weight.set_flavours(["js"])
        return pr_review


class RecruitProjectReviewQualityViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "recruitprojectreviewquality-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    FIELDS_THAT_CAN_BE_FALSEY = ["agile_card"]

    def verbose_instance_factory(self):
        review = factories.RecruitProjectReviewFactory(
            trusted=True, validated=RecruitProjectReview.CORRECT
        )
        review.complete_review_cycle = True
        review.save()
        project: RecruitProject = review.recruit_project
        project.set_flavours(["js"])

        weight = factories.ContentItemAgileWeightFactory(
            content_item=project.content_item
        )
        weight.set_flavours(["js"])

        return review


class RecruitProjectReviewViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "recruitprojectreview-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    FIELDS_THAT_CAN_BE_FALSEY = ["agile_card"]

    def verbose_instance_factory(self):
        review = factories.RecruitProjectReviewFactory(
            trusted=True, validated=RecruitProjectReview.CORRECT
        )
        project: RecruitProject = review.recruit_project
        project.set_flavours(["js"])

        return review


class RecruitTopicReviewViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "topicreview-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        return factories.TopicReviewFactory()


class ContentItemViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "contentitem-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    NUMBER_OF_INSTANCES_CREATED_BY_VERBOSE_FACTORY = 3
    FIELDS_THAT_CAN_BE_FALSEY = [
        "flavour_names",
        "topic_needs_review",
        "continue_from_repo",
        "project_submission_type_nice",
    ]

    def verbose_instance_factory(self):
        item = factories.ProjectContentItemFactory()
        factories.ContentItemOrderFactory(post=item)
        factories.ContentItemOrderFactory(pre=item)
        item.tags.add(factories.TagFactory())
        return item


# class ContentItemOrderViewsetTests(APITestCase, APITestCaseMixin):
#     LIST_URL_NAME = "contentitemorder-list"
#     SUPPRESS_TEST_POST_TO_CREATE = True     TODO

#     def verbose_instance_factory(self):
#         return factories.ContentItemOrderFactory()


class WorkshopAttendanceViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "workshopattendance-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        workshop = factories.ContentItemFactory(content_type=ContentItem.WORKSHOP)
        workshop_attendance = factories.WorkshopAttendanceFactory(content_item=workshop)
        content = workshop_attendance.content_item
        content.topic_needs_review = False
        content.save()
        return workshop_attendance

    def test_get_instance_permissions(self):
        attendee_user = UserFactory(is_superuser=False, is_staff=False)
        workshop_attendance = factories.WorkshopAttendanceFactory(
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.WORKSHOP
            ),
            timestamp=timezone.now(),
            attendee_user=attendee_user,
        )

        self.login(attendee_user)
        url = self.get_list_url()
        response = self.client.get(f"{url}{workshop_attendance.id}", follow=True)
        self.assertEqual(response.status_code, 200)

        random_human = UserFactory(is_superuser=False, is_staff=False)
        self.login(random_human)
        response = self.client.get(f"{url}{workshop_attendance.id}", follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["detail"].code, "permission_denied")


class ReviewerTrustViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "reviewtrust-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        review_trust_object = factories.ReviewTrustFactory()
        review_trust_object.flavours.add(Tag.objects.create(name="anything_really"))
        return review_trust_object

    def setUp(self):
        self.api_url = self.get_list_url()

    def test_staff_member_can_view_all_trusted_reviewer_objects(self):
        staff_member = UserFactory(is_superuser=False, is_staff=True)
        self.login(staff_member)
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 200)

    def test_admin_user_can_view_all_trusted_reviewer_objects(self):
        staff_member_superuser = UserFactory(is_superuser=True, is_staff=False)
        self.login(staff_member_superuser)
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 200)

    def test_normal_user_cannot_view_other_user_trusted_review_objects(self):
        review_trust_object = factories.ReviewTrustFactory()
        recruit = UserFactory(is_superuser=False, is_staff=False)
        self.login(recruit)
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 403)
        self.assertNotIn(str(review_trust_object.content_item), response.data)

    def test_users_can_view_their_own_reviewer_trusts(self):
        review_trust_object = factories.ReviewTrustFactory(
            user=factories.UserFactory(is_superuser=False, is_staff=False)
        )
        self.login(review_trust_object.user)
        response = self.client.get(f"{self.api_url}?user={review_trust_object.user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[0].get("content_item_title"),
            review_trust_object.content_item.title,
        )


class BurndownSnapShotViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "burndownsnapshot-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        return factories.BurndownSnapshotFactory()

    def setUp(self):
        self.api_url = self.get_list_url()
        self.team1 = TeamFactory()
        self.team1_users = [UserFactory() for _ in range(3)]

    def test_staff_member_can_view_all_burndown_snapshot_objects(self):
        staff_member = UserFactory(is_superuser=False, is_staff=True)
        self.login(staff_member)
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)

    def test_users_can_view_their_own_burndown_snapshot_objects(self):
        burndown_snapshot_object = factories.BurndownSnapshotFactory(
            user=UserFactory(is_superuser=False, is_staff=False)
        )
        self.login(burndown_snapshot_object.user)
        response = self.client.get(
            f"{self.api_url}?user__id={burndown_snapshot_object.user.id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0].get("user"), burndown_snapshot_object.user.id)

    def test_team_members_can_view_burndown_snapshot_objects_of_fellow_team_members(
        self,
    ):
        for user in self.team1_users:
            self.login(user)
            response = self.client.get(f"{self.api_url}?user__id={user.id}")
            self.assertEqual(response.status_code, 200)

    def test_team1_users_cannot_view_team2_burndown_snapshot_objects(self):
        team2 = TeamFactory()
        team2_users = [UserFactory() for _ in range(3)]

        for user in self.team1_users:
            self.login(user)
            response = self.client.get(
                f"{self.api_url}?user__id={[user.id for user in team2_users]}"
            )
            self.assertEqual(response.status_code, 403)


class TestBulkSetDueDatesApi(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "team-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    def setUp(self):
        self.blue_team = TeamFactory(name="BLUE TEAM")
        self.red_team = TeamFactory(name="RED TEAM")
        self.user_one_blue = UserFactory(
            first_name="one_blue", is_superuser=False, is_staff=False
        )
        self.user_two_blue = UserFactory(
            first_name="two_blue", is_superuser=False, is_staff=False
        )
        self.user_one_red = UserFactory(
            first_name="one_red", is_superuser=False, is_staff=False
        )
        self.user_two_red = UserFactory(
            first_name="two_red", is_superuser=False, is_staff=False
        )
        self.super_user = UserFactory(
            first_name="super_user", is_superuser=True
        )

        self.blue_team.user_set.add(self.user_one_blue)
        self.blue_team.user_set.add(self.user_two_blue)
        self.red_team.user_set.add(self.user_one_red)
        self.red_team.user_set.add(self.user_two_red)

    def test_team_members_cannot_bulk_set_due_dates_for_the_team_they_belong_to(self):
        project = RecruitProjectFactory(due_time=None)
        card = AgileCardFactory(recruit_project=project)
        card.reviewers.add(self.user_one_red)
        card.assignees.add(self.user_two_red)
        self.login(self.user_two_red)
        url = f"{self.get_instance_url(pk=self.red_team.id)}bulk_set_due_dates/"
        response = self.client.post(
            path=url,
            format="json",
            data={
                "due_time": "2021-12-03T14:17",
                "content_item": card.content_item.id,
                "flavours": [1, 2, 3],
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_team_members_cannot_bulk_set_due_dates_for_teams_they_dont_belong_to(self):

        project = RecruitProjectFactory(due_time=None)
        card = AgileCardFactory(recruit_project=project)
        card.reviewers.add(self.user_one_blue)
        card.assignees.add(self.user_one_red)
        self.login(self.user_one_blue)
        url = f"{self.get_instance_url(pk=self.red_team.id)}bulk_set_due_dates/"
        response = self.client.post(
            path=url,
            format="json",
            data={
                "due_time": "2021-12-03T14:17",
                "content_item": "2",
                "team": str(self.red_team.id),
                "flavours": [1, 2, 3],
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_super_user_can_bulk_set_due_dates_for_a_team(self):

        project = RecruitProjectFactory(due_time=None)
        card = AgileCardFactory(
            recruit_project=project, flavours=["JAVASCRIPT", "PYTHON"]
        )
        card.reviewers.add(self.user_one_blue)
        card.assignees.add(self.user_two_blue)
        self.assertIsNone(card.due_time)
        self.login(self.super_user)
        url = f"{self.get_instance_url(pk=self.blue_team.id)}bulk_set_due_dates/"
        due_date = "2021-12-03T14:17"
        response = self.client.post(
            path=url,
            format="json",
            data={
                "due_time": due_date,
                "content_item": card.content_item.id,
                "team": str(self.blue_team.id),
                "flavours": [card.flavours.first().id, card.flavours.last().id],
            },
        )

        self.assertEqual(response.status_code, 200)
        card.refresh_from_db()
        date_expected = parse_datetime(due_date).replace(tzinfo=timezone.utc)
        self.assertEqual(card.due_time, date_expected)

    def test_bulk_set_due_date_happened_for_every_card_with_the_same_content_item_for_the_team(
        self,
    ):
        """
        Three cards, two with the same content_item and one with a different content_item.  The one with the
        different content_item should not have it's due_time updated, it should be left as it is.
        """
        project = RecruitProjectFactory(due_time=None)
        card_1 = AgileCardFactory(recruit_project=project, flavours=["JAVASCRIPT"])
        card_1.assignees.add(self.user_one_red)
        card_2 = AgileCardFactory(
            recruit_project=RecruitProjectFactory(due_time=None),
            content_item=card_1.content_item,
            flavours=["JAVASCRIPT"],
        )
        card_2.assignees.add(self.user_two_red)
        card_3 = AgileCardFactory(
            recruit_project=RecruitProjectFactory(due_time=None),
            flavours=["JAVASCRIPT"],
        )
        card_3.assignees.add(self.user_two_red)
        self.assertEqual(card_1.content_item, card_2.content_item)
        self.assertNotEqual(card_1.content_item, card_3.content_item)

        self.login(self.super_user)
        url = f"{self.get_instance_url(pk=self.red_team.id)}bulk_set_due_dates/"
        due_date = "2021-12-03T14:17"
        response = self.client.post(
            path=url,
            format="json",
            data={
                "due_time": due_date,
                "content_item": card_1.content_item.id,
                "team": str(self.red_team.id),
                "flavours": [card_1.flavours.first().id],
            },
        )
        self.assertEqual(response.status_code, 200)

        team_cards = get_team_cards(self.red_team, card_1.content_item)
        self.assertIn(card_1, team_cards)
        self.assertIn(card_2, team_cards)
        self.assertNotIn(card_3, team_cards)

        for card in team_cards:
            card.refresh_from_db()
            date_expected = parse_datetime(due_date).replace(tzinfo=timezone.utc)
            self.assertTrue(card.due_time, date_expected)

        self.assertIsNone(card_3.due_time)

    def test_due_date_not_set_if_flavour_name_differs_to_request(self):
        """
        Three cards (1 'js' flavour & 2 'python' flavoured); the request is for team_cards with a 'js' flavour to have
        their due dates set and all other flavoured cards to not have their due dates altered.
        """
        project = RecruitProjectFactory(due_time=None)
        card_1 = AgileCardFactory(recruit_project=project, flavours=["JAVASCRIPT"])
        card_1.assignees.add(self.user_one_red)
        card_2 = AgileCardFactory(
            recruit_project=RecruitProjectFactory(due_time=None),
            content_item=card_1.content_item,
            flavours=["PYTHON"],
        )
        card_2.assignees.add(self.user_two_red)
        card_3 = AgileCardFactory(
            recruit_project=RecruitProjectFactory(due_time=None),
            content_item=card_1.content_item,
            flavours=["PYTHON"],
        )
        card_3.assignees.add(self.user_two_red)
        self.assertEqual(card_1.content_item, card_2.content_item)
        self.assertEqual(card_1.content_item, card_3.content_item)
        self.login(self.super_user)
        url = f"{self.get_instance_url(pk=self.red_team.id)}bulk_set_due_dates/"
        due_date = "2022-01-20T12:17"
        response = self.client.post(
            path=url,
            format="json",
            data={
                "due_time": due_date,
                "content_item": card_1.content_item.id,
                "flavours": [card_1.flavours.first().id],
            },
        )
        self.assertEqual(response.status_code, 200)

        card_1.refresh_from_db()
        card_2.refresh_from_db()
        card_3.refresh_from_db()
        date_expected = parse_datetime(due_date).replace(tzinfo=timezone.utc)
        self.assertEqual(card_1.due_time, date_expected)
        self.assertIsNone(card_2.due_time)
        self.assertIsNone(card_3.due_time)


class ContentItemAgileWeightTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "contentitemagileweight-list"

    def verbose_instance_factory(self):
        return factories.ContentItemAgileWeightFactory(flavours=["python"])

    def generate_post_create_data(self):
        item = factories.ContentItemFactory(flavours=["python", "javascript", "ts"])
        return {
            "content_item": item.id,
            "flavour_names": ["python", "ts"],
            "weight": 123,
        }

    def test_attributes_set_on_post(self):
        data = self.generate_post_create_data()
        self.login_as_superuser()
        url = self.get_list_url()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        new_instance = ContentItemAgileWeight.objects.first()
        self.assertEqual(new_instance.content_item.id, data["content_item"])
        self.assertEqual(new_instance.weight, data["weight"])
        self.assertEqual(new_instance.flavour_names, data["flavour_names"])


class TestCourseRegistrationViewSet(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "courseregistration-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        course_registration = factories.CourseRegistrationFactory()
        return course_registration


class TestPullRequestReviewQueueViewSet(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "pullrequestreviewqueue-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    FIELDS_THAT_CAN_BE_FALSEY = [
        "review_request_time",
        "users_that_reviewed_since_last_review_request",
        "users_that_reviewed_since_last_review_request_emails",
    ]

    def verbose_instance_factory(self):
        card = AgileCardFactory()
        project = card.recruit_project
        project.set_flavours(["foo"])
        project.content_item.tags.add(TagFactory())
        project.code_review_competent_since_last_review_request = 12
        project.code_review_excellent_since_last_review_request = 12
        project.code_review_red_flag_since_last_review_request = 12
        project.code_review_ny_competent_since_last_review_request = 12
        project.reviewer_users.add(UserFactory())

        pr = PullRequestFactory(state="open")
        project.repository = pr.repository
        project.save()

        pr = PullRequestFactory(state="closed")
        card = AgileCardFactory()
        card.recruit_project.repository = pr.repository

        return project


class TestCompetenceReviewQueueViewSet(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "competencereviewqueue-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    FIELDS_THAT_CAN_BE_FALSEY = [
        "open_pr_count",
        "oldest_open_pr_updated_time",
        "users_that_reviewed_since_last_review_request",
        "users_that_reviewed_since_last_review_request_emails",
    ]

    def verbose_instance_factory(self):
        RecruitProjectFactory()
        RecruitProjectFactory()
        card = AgileCardFactory()

        project = card.recruit_project
        project.request_review()
        project.set_flavours(["foo"])
        project.content_item.tags.add(TagFactory())
        project.code_review_competent_since_last_review_request = 12
        project.code_review_excellent_since_last_review_request = 12
        project.code_review_red_flag_since_last_review_request = 12
        project.code_review_ny_competent_since_last_review_request = 12
        project.reviewer_users.add(UserFactory())
        project.save()

        return project

    def test_list_filters_by_what_the_user_is_meant_to_see(self):
        cards = [AgileCardFactory() for _ in range(10)]
        for card in cards:
            project = card.recruit_project
            project.reviewer_users.add(UserFactory())
            project.request_review()

        teams = [TeamFactory() for _ in range(5)]

        teams[0].user_set.add(cards[0].recruit_project.recruit_users.first())
        teams[1].user_set.add(cards[1].recruit_project.recruit_users.first())
        teams[2].user_set.add(cards[2].recruit_project.reviewer_users.first())
        teams[3].user_set.add(cards[3].recruit_project.reviewer_users.first())
        teams[4].user_set.add(cards[4].recruit_project.reviewer_users.first())

        manager_user = UserFactory()

        assign_perm(Team.PERMISSION_MANAGE_CARDS, manager_user, teams[0])
        assign_perm(Team.PERMISSION_VIEW_ALL, manager_user, teams[1])
        assign_perm(Team.PERMISSION_REVIEW_CARDS, manager_user, teams[2])
        assign_perm(Team.PERMISSION_TRUSTED_REVIEWER, manager_user, teams[3])

        url = self.get_list_url()

        # superusers can see everything
        self.login_as_superuser()
        response = self.client.get(url)
        queue = response.data
        self.assertEqual(len(queue), 10)
        self.assertEqual(
            [d["id"] for d in queue], [card.recruit_project.id for card in cards]
        )

        # random users can't see anything
        self.login(UserFactory())
        response = self.client.get(url)
        queue = response.data
        self.assertEqual(len(queue), 0)

        # users can see their own projects
        self.login(cards[5].recruit_project.reviewer_users.first())
        response = self.client.get(url)
        queue = response.data
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0]["id"], cards[5].recruit_project.id)

        # if you have any kind of view access over a team then you can see those projects
        self.login(manager_user)
        response = self.client.get(url)
        queue = response.data
        self.assertEqual(len(queue), 4)
        self.assertEqual(
            [d["id"] for d in queue], [card.recruit_project.id for card in cards[:4]]
        )


class CurriculumContentRequirementViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "curriculumcontentrequirement-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        return factories.CurriculumContentRequirementFactory()


class TestTeamViewSet(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "team-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        team = TeamFactory()
        user = factories.UserFactory()
        team.user_set.add(user)
        return team

    def test_only_returns_teams_i_can_see(self):

        url = self.get_list_url()
        super_user = factories.UserFactory(is_superuser=True)
        staff_user = factories.UserFactory(is_staff=True)
        normal_user = factories.UserFactory()

        team_1 = TeamFactory()
        TeamFactory()

        self.login(super_user)

        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

        self.login(staff_user)

        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

        for permission, _ in Team._meta.permissions:
            # make sure that users can read what they need to
            user = factories.UserFactory()
            assign_perm(permission, user, team_1)
            self.login(user)

            response = self.client.get(url)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["id"], team_1.id)

            # check that it works for groups as well
            group = Group.objects.create(name=f"{permission} group")
            user = factories.UserFactory()
            group.user_set.add(user)
            assign_perm(permission, group, team_1)

            self.login(user)

            response = self.client.get(url)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["id"], team_1.id)

        self.login(normal_user)

        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

    def test_staff_users_cant_see_all_teams(self):
        user = factories.UserFactory(is_superuser=False, is_staff=True)

        TeamFactory()

        self.login(user)
        url = self.get_list_url()
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

