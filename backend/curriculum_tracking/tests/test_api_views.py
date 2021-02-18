from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from core.tests.factories import UserFactory
from django.urls import reverse
from . import factories
from core.tests import factories as core_factories
from django.utils.timezone import datetime
from datetime import timedelta
from curriculum_tracking.models import ContentItem, RecruitProjectReview
from django.utils import timezone
from taggit.models import Tag


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
    ]

    def verbose_instance_factory(self):
        project = factories.RecruitProjectFactory(
            due_time=timezone.now(), review_request_time=timezone.now()
        )
        card = factories.AgileCardFactory(recruit_project=project)
        card.reviewers.add(core_factories.UserFactory())
        card.assignees.add(core_factories.UserFactory())
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
    ]

    def verbose_instance_factory(self):
        project = factories.RecruitProjectFactory()
        card = factories.AgileCardFactory(recruit_project=project)
        card.reviewers.add(core_factories.UserFactory())
        card.assignees.add(core_factories.UserFactory())

        card.flavours.add(Tag.objects.create(name="asdsasa"))

        return card

    def test_set_project_card_due_time_permissions(self):
        card = factories.AgileCardFactory(
            content_item=factories.ProjectContentItemFactory(), recruit_project=None
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

        card = factories.AgileCardFactory(
            content_item=content_item,
            # content_type= ContentItem.PROJECT,
        )

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
        project = factories.RecruitProjectInRevewColumnFactory(
            content_item=factories.ProjectContentItemFactory(
                project_submission_type=ContentItem.REPOSITORY,
            )
        )
        factories.RecruitProjectReviewFactory(recruit_project=project)
        project.reviewer_users.add(core_factories.UserFactory())
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

    # def test_recruit_permissions_on_object(self):
    #     return  # TODO
    #     recruit1 = UserFactory(is_superuser=False, is_staff=False)
    #     recruit2 = UserFactory(is_superuser=False, is_staff=False)

    #     project1 = factories.RecruitProjectFactory(recruit_users=[recruit1])
    #     project2 = factories.RecruitProjectFactory(recruit_users=[recruit2])

    #     self.login(recruit1)

    #     url = self.get_list_url()
    #     response = self.client.get(f"{url}{project1.id}/")

    #     self.assertEqual(response.status_code, 200)

    #     response = self.client.get(f"{url}{project2.id}/")
    #     self.assertEqual(response.status_code, 403)


class RecruitProjectReviewViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "recruitprojectreview-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    FIELDS_THAT_CAN_BE_FALSEY = ["agile_card"]

    def verbose_instance_factory(self):
        return factories.RecruitProjectReviewFactory(
            trusted=True, validated=RecruitProjectReview.CORRECT
        )


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
        item = factories.ProjectContentItemFactory(story_points=5)
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
