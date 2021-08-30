from django.test import TestCase
from curriculum_tracking.tests.factories import RecruitProjectFactory
from curriculum_tracking.models import (
    AgileCard,
    RecruitProject,
    TopicProgress,
    WorkshopAttendance,
    ContentItem,
    TopicReview,
)
from . import factories
from core.tests.factories import UserFactory
from datetime import timedelta

from curriculum_tracking.constants import (
    RED_FLAG,
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)
from django.utils import timezone

TYPESCRIPT = "ts"
JAVASCRIPT = "js"



class OldestOpenPrUpdatedTimeTests(TestCase):

    def setUp(self):

        self.card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.IN_PROGRESS,
        )

        self.project = RecruitProjectFactory(content_item=self.card.content_item)
        self.user = UserFactory()
        self.card.assignees.set([self.user])
        self.today = timezone.now()
        self.yesterday = self.today - timezone.timedelta(days=1)
        self.assertIsNotNone(self.card.recruit_project)
        self.assertEqual(self.card.status, AgileCard.IN_PROGRESS)
        self.assertEqual(self.project.content_item, self.card.content_item)

    def test_initial(self):
        print('**************************************************')
        print('Current status of the card:')
        print(self.card.status)
        print('Name of the project:')
        print(self.project)
        print('Name of the content item:')
        print(f'{self.card.content_item} = {self.project.content_item}')
        print('Who is assigned to the card:')
        print(self.card.assignees)
        print('**************************************************', end='\n')
        print('\n')

        self.project.start_time = timezone.now() - timedelta(days=15)
        self.project.save()

        print('\n')
        self.assertEqual(AgileCard.derive_status_from_project(self.project), AgileCard.IN_PROGRESS)

        # Creating the 1st of three reviews
        review = factories.RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT,
            recruit_project=self.project,
            reviewer_user=self.user,
        )
        print('\n')
        print('***Details after 1st review requested***')
        print(f'Status = {review.status}')
        print(f'Project reviewed = {review.recruit_project}')
        print(f'Person who reviewed = {review.reviewer_user}')

        print(AgileCard.finding_latest_reviewer_ids(self.project))


    """
    def test_users_same(self, card, project):
        card_assignees = sorted([o.id for o in card.assignees.all()])
        card_reviewers = sorted([o.id for o in card.reviewers.all()])
        project_reviewers = sorted([o.id for o in project.reviewer_users.all()])
        project_assignees = sorted([o.id for o in project.recruit_users.all()])
        for assignee, reviewer in (card_assignees, card_reviewers):
            print(assignee)
            print(reviewer)
            print("next batch of assignee's and reviewers")
        print('', end='\n')
    """

    """
    @mock.patch("git_real.helpers.get_repo")
    @mock.patch.object(RecruitProject, "setup_repository")
    def test_start_project_creates_project_if_not_exists(self, get_repo, *_):

        card = factories.AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=None,
            content_item=factories.ProjectContentItemFactory(
                project_submission_type=ContentItem.REPOSITORY
            ),
            assignees=[SocialProfileFactory().user],
        )

        self.assertIsNone(card.recruit_project)

        get_repo.return_value = {
            "full_name": "me/kiff",
            "owner": {"login": "me"},
            "ssh_url": "https://whatever.git",
            "private": True,
            "created_at": timezone.now().strftime(GITHUB_DATETIME_FORMAT),
            "archived": False,
        }

        card.start_project()

        self.assertIsNotNone(card.recruit_project)
        project = card.recruit_project

        card.refresh_from_db()
        project.refresh_from_db()

        self.assert_users_same(card=card, project=project)
        self.assertEqual(project.content_item, card.content_item)
        self.assertTrue(project.setup_repository.called)
        self.assertEqual(card.status, AgileCard.IN_PROGRESS)
        self.assertIsNotNone(project.start_time)    
    """


    """
    @mock.patch("social_auth.github_api.Api")
    @mock.patch("git_real.helpers.add_collaborator")
    @mock.patch.object(RecruitProject, "setup_repository")
    @mock.patch("git_real.helpers.get_repo")
    def test_that_project_submission_type_REPOSITORY_creates_a_repo_with_flavourful_name(
        self, get_repo, *_
    ):
        content_item = factories.ProjectContentItemFactory(
            flavours=[TYPESCRIPT, JAVASCRIPT]
        )

        card_ts = factories.AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=None,
            content_item=content_item,
            flavours=[TYPESCRIPT],
            assignees=[SocialProfileFactory().user],
        )

        card_js = factories.AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=None,
            content_item=content_item,
            flavours=[JAVASCRIPT],
            assignees=[SocialProfileFactory().user],
        )

        self.assertIsNone(card_js.recruit_project)

        card_ts.start_project()
        card_js.start_project()

        self.assertNotEqual(card_ts.recruit_project, card_js.recruit_project)

        ts_project_flavours = [o.name for o in card_ts.recruit_project.flavours.all()]
        self.assertEqual(ts_project_flavours, [TYPESCRIPT])

        js_project_flavours = [o.name for o in card_js.recruit_project.flavours.all()]
        self.assertEqual(js_project_flavours, [JAVASCRIPT])
    """

"""
class Project_set_due_time_Tests(TestCase):
    def make_topic_card(self):
        self.card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.READY,
        )
        self.card.assignees.set([UserFactory()])

    def make_project_card(self):
        self.card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.READY,
        )
        self.card.assignees.set([UserFactory()])

    def test_set_due_time_on_PROJECT_no_instance(self):
        self.make_project_card()
        self.card.set_due_time(timezone.now())

        self.assertEqual(self.card.status, AgileCard.READY)
        self.assertIsNotNone(self.card.recruit_project.due_time)

    def test_set_due_time_on_TOPIC_no_instance(self):
        self.make_topic_card()
        self.card.set_due_time(timezone.now())
        self.assertEqual(self.card.status, AgileCard.READY)
        self.assertIsNotNone(self.card.topic_progress.due_time)

    def test_set_due_time_on_PROJECT_with_instance(self):
        self.make_project_card()
        self.card.start_project()
        self.card.set_due_time(timezone.now())

        self.assertEqual(self.card.status, AgileCard.IN_PROGRESS)
        self.assertIsNotNone(self.card.recruit_project.due_time)

    def test_set_due_time_on_TOPIC_with_instance(self):
        self.make_topic_card()
        self.card.start_topic()
        self.card.set_due_time(timezone.now())
        self.assertEqual(self.card.status, AgileCard.IN_PROGRESS)
        self.assertIsNotNone(self.card.topic_progress.due_time)
"""


"""
class TopicMovementTestCase(TestCase):
    def setUp(self):
        self.card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.READY,
        )
        self.card.assignees.set([UserFactory()])

    def test_start(self):
        card = self.card
        card.start_topic()
        self.assertEqual(card.status, AgileCard.IN_PROGRESS)
        self.assertEqual(card.topic_progress.user, card.assignees.first())
        self.assertEqual(card.topic_progress.content_item, card.content_item)
        self.assertIsNone(card.topic_progress.complete_time)
        self.assertIsNotNone(card.topic_progress.start_time)

    def test_stop(self):
        self.card.start_topic()
        self.card.stop_topic()

        self.assertEqual(self.card.status, AgileCard.READY)
        self.assertIsNotNone(self.card.topic_progress)
        self.assertIsNone(self.card.topic_progress.start_time)

    def test_finish(self):
        self.card.start_topic()
        self.card.finish_topic()

        self.assertEqual(self.card.status, AgileCard.COMPLETE)
        self.assertEqual(self.card.topic_progress.user, self.card.assignees.first())
        self.assertEqual(self.card.topic_progress.content_item, self.card.content_item)
        self.assertIsNotNone(self.card.topic_progress.complete_time)
        self.assertIsNotNone(self.card.topic_progress.start_time)
        self.assertIsNone(self.card.topic_progress.review_request_time)

    def test_finish_when_review_needed(self):
        content_item = self.card.content_item
        content_item.topic_needs_review = True
        content_item.save()

        self.card.start_topic()
        self.card.finish_topic()

        self.assertIsNone(self.card.topic_progress.complete_time)
        self.assertIsNotNone(self.card.topic_progress.review_request_time)
        self.assertIsNotNone(self.card.topic_progress.start_time)
        self.assertEqual(self.card.status, AgileCard.IN_REVIEW)

    def test_start_topic_when_due_date_already_set(self):
        self.card.set_due_time(timezone.now())

        self.card.start_topic()
        self.assertEqual(self.card.status, AgileCard.IN_PROGRESS)
        self.assertEqual(self.card.topic_progress.user, self.card.assignees.first())
        self.assertEqual(self.card.topic_progress.content_item, self.card.content_item)
        self.assertIsNone(self.card.topic_progress.complete_time)
        self.assertIsNotNone(self.card.topic_progress.start_time)

    def test_add_COMPETENT_review(self):

        self.card.content_item.topic_needs_review = True
        self.card.content_item.save()
        self.card.start_topic()
        self.card.finish_topic()

        self.assertEqual(self.card.status, AgileCard.IN_REVIEW)

        review = TopicReview.objects.create(
            status=COMPETENT,
            topic_progress=self.card.topic_progress,
            reviewer_user=UserFactory(),
        )
        self.card.refresh_from_db()
        self.assertEqual(self.card.status, AgileCard.COMPLETE)

    def test_add_NOT_YET_COMPETENT_review(self):
        self.card.content_item.topic_needs_review = True
        self.card.content_item.save()
        self.card.start_topic()
        self.card.finish_topic()

        self.assertEqual(self.card.status, AgileCard.IN_REVIEW)

        review = TopicReview.objects.create(
            status=NOT_YET_COMPETENT,
            topic_progress=self.card.topic_progress,
            reviewer_user=UserFactory(),
        )
        self.card.refresh_from_db()
        self.assertEqual(self.card.status, AgileCard.REVIEW_FEEDBACK)

    def test_add_EXCELLENT_review(self):
        self.card.content_item.topic_needs_review = True
        self.card.content_item.save()
        self.card.start_topic()
        self.card.finish_topic()

        self.assertEqual(self.card.status, AgileCard.IN_REVIEW)

        review = TopicReview.objects.create(
            status=EXCELLENT,
            topic_progress=self.card.topic_progress,
            reviewer_user=UserFactory(),
        )
        self.card.refresh_from_db()
        self.assertEqual(self.card.status, AgileCard.COMPLETE)

    def test_add_RED_FLAG_review(self):
        self.card.content_item.topic_needs_review = True
        self.card.content_item.save()
        self.card.start_topic()
        self.card.finish_topic()

        self.assertEqual(self.card.status, AgileCard.IN_REVIEW)

        review = TopicReview.objects.create(
            status=RED_FLAG,
            topic_progress=self.card.topic_progress,
            reviewer_user=UserFactory(),
        )
        self.card.refresh_from_db()
        self.assertEqual(self.card.status, AgileCard.REVIEW_FEEDBACK)

    def test_that_start_topic_cant_make_duplicates(self):
        content_item = self.card.content_item
        content_item.topic_needs_review = True
        content_item.save()

        get_count = lambda: TopicProgress.objects.filter(
            content_item=content_item, user=self.card.assignees.first()
        ).count()
        topic_progress_count = get_count()

        self.assertEqual(topic_progress_count, 0)
        self.card.start_topic()

        topic_progress_count = get_count()

        self.assertEqual(topic_progress_count, 1)

        self.card.status = AgileCard.READY
        self.card.start_topic()

        topic_progress_count = get_count()
        self.assertEqual(topic_progress_count, 1)
"""
