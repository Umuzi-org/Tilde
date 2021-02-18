from django.test import TestCase

from curriculum_tracking.card_generation_helpers import (
    generate_all_content_cards_for_user,
    update_topic_card_progress,
    update_project_card_progress,
    update_workshop_card_progress,
    FlavourProgressMismatchError,
)


from .factories import (
    CourseRegistrationFactory,
    ContentItemFactory,
    CurriculumContentRequirementFactory,
    ProjectContentItemFactory,
)
from curriculum_tracking.constants import NOT_YET_COMPETENT, COMPETENT
from curriculum_tracking import models
from curriculum_tracking.tests import factories
from core.tests import factories as core_factories

import taggit
from django.utils import timezone
from datetime import timedelta

JAVASCRIPT = "JAVASCRIPT"
TYPESCRIPT = "TYPESCRIPT"


class generate_all_content_cards_for_user_Tests(TestCase):
    def setUp(self):
        registration1 = CourseRegistrationFactory()
        self.user = registration1.user
        registration2 = CourseRegistrationFactory(user=self.user)

        self.topic1 = ContentItemFactory(content_type=models.ContentItem.TOPIC)
        self.project1 = ProjectContentItemFactory(
            content_type=models.ContentItem.PROJECT,
        )
        self.workshop1 = ContentItemFactory(content_type=models.ContentItem.WORKSHOP)

        self.topic1.set_flavours([JAVASCRIPT, TYPESCRIPT])
        self.project1.set_flavours([JAVASCRIPT, TYPESCRIPT])
        self.workshop1.set_flavours([JAVASCRIPT, TYPESCRIPT])

        self.topic2 = ContentItemFactory(content_type=models.ContentItem.TOPIC)
        self.project2 = ProjectContentItemFactory(
            content_type=models.ContentItem.PROJECT
        )
        self.workshop2 = ContentItemFactory(content_type=models.ContentItem.WORKSHOP)

        self.flavoured_content = [self.topic1, self.project1, self.workshop1]
        self.unflavoured_content = [self.topic2, self.project2, self.workshop2]

        for content in self.flavoured_content:

            CurriculumContentRequirementFactory(
                content_item=content,
                curriculum=registration1.curriculum,
                flavours=[JAVASCRIPT],
            )

            CurriculumContentRequirementFactory(
                content_item=content,
                curriculum=registration2.curriculum,
                flavours=[TYPESCRIPT],
            )

        for content in self.unflavoured_content:

            CurriculumContentRequirementFactory(
                content_item=content,
                curriculum=registration1.curriculum,
            )

            CurriculumContentRequirementFactory(
                content_item=content,
                curriculum=registration2.curriculum,
            )

    def test_two_courses_with_overlapping_content_and_no_project_or_content_progress(
        self,
    ):
        generate_all_content_cards_for_user(self.user)

        for content in self.unflavoured_content:
            count = len(models.AgileCard.objects.filter(content_item=content))
            self.assertEqual(count, 1)

        for content in self.flavoured_content:
            cards = models.AgileCard.objects.filter(content_item=content)
            self.assertEqual(len(cards), 2)
            # for card in cards:

            options = [card.flavour_names for card in cards]
            option_counts = [len(l) for l in options]
            self.assertEqual(option_counts, [1, 1])
            flat_options = sorted([s for l in options for s in l])
            self.assertEqual(flat_options, [JAVASCRIPT, TYPESCRIPT])

            # [o.content_options for o in models.AgileCard.objects.filter(content_item=content)

        cards = models.AgileCard.objects.all()
        self.assertEqual(
            len(cards), 9
        )  # 3 for each course + 3 for the stuff that overlaps

    def test_card_prerequisites_take_options_into_account(self):

        models.ContentItemOrder.objects.create(post=self.project1, pre=self.topic1)
        models.ContentItemOrder.objects.create(post=self.project1, pre=self.topic2)
        models.ContentItemOrder.objects.create(post=self.project2, pre=self.topic2)

        generate_all_content_cards_for_user(self.user)

        # project 2 has no options. So there will only be one and it will have only one prereq
        project2_card = models.AgileCard.objects.get(content_item=self.project2)
        project2_requirement = project2_card.requires_cards.get()
        # self.assertEqual(len(project2_requirement), 1)
        self.assertEqual(project2_requirement.content_item, self.topic2)
        self.assertEqual(project2_card.flavour_names, [])
        self.assertEqual(project2_requirement.flavour_names, [])

        # project 1 has pre-req and two different flavours
        project1_cards = models.AgileCard.objects.filter(content_item=self.project1)

        for card in project1_cards:
            # they both require topic 1, topic1 has no options so it's the same card
            self.assertTrue(project2_requirement in card.requires_cards.all())

        ts_project_card = [
            card for card in project1_cards if TYPESCRIPT in card.flavour_names
        ][0]

        js_project_card = [
            card for card in project1_cards if JAVASCRIPT in card.flavour_names
        ][0]

        ts_required_card = ts_project_card.requires_cards.filter(
            content_item=self.topic1
        ).get()
        self.assertEqual(ts_required_card.flavour_names, [TYPESCRIPT])

        js_required_card = js_project_card.requires_cards.filter(
            content_item=self.topic1
        ).get()
        self.assertEqual(js_required_card.flavour_names, [JAVASCRIPT])


class update_topic_card_progress_Tests(TestCase):
    def setUp(self):
        self.user = core_factories.UserFactory()

    def test_no_flavours(self):

        content_item = factories.ContentItemFactory(
            content_type=models.ContentItem.TOPIC
        )

        card = factories.AgileCardFactory(content_item=content_item)
        card.assignees.add(self.user)

        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, card.READY)

        progress = models.TopicProgress(
            content_item=content_item, user=self.user, due_time=timezone.now()
        )
        progress.save()

        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, card.READY)

        progress.start_time = timezone.now()
        progress.save()

        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, card.IN_PROGRESS)

        progress.review_request_time = timezone.now()
        progress.save()

        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, card.IN_REVIEW)

        progress.complete_time = timezone.now()
        progress.save()

        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, card.COMPLETE)

    def test_with_flavours(self):
        content_item = factories.ContentItemFactory(
            content_type=models.ContentItem.TOPIC,
            flavours=[JAVASCRIPT, TYPESCRIPT],
        )

        card_ts = factories.AgileCardFactory(
            content_item=content_item, flavours=[TYPESCRIPT]
        )
        card_ts.assignees.add(self.user)

        card_js = factories.AgileCardFactory(
            content_item=content_item, flavours=[JAVASCRIPT]
        )
        card_js.assignees.add(self.user)

        progress = models.TopicProgress(
            content_item=content_item, user=self.user, start_time=timezone.now()
        )
        progress.save()
        progress.flavours.add(
            taggit.models.Tag.objects.get_or_create(name=TYPESCRIPT)[0]
        )

        update_topic_card_progress(self.user)
        card_ts.refresh_from_db()
        card_js.refresh_from_db()

        self.assertEqual(card_js.status, card_ts.READY)
        self.assertEqual(card_ts.status, card_ts.IN_PROGRESS)

    def test_error_gets_raised_if_card_has_flavours_but_progress_doesnt(self):
        content_item = factories.ContentItemFactory(
            content_type=models.ContentItem.TOPIC,
            flavours=[JAVASCRIPT, TYPESCRIPT],
        )

        card_ts = factories.AgileCardFactory(
            content_item=content_item, flavours=[TYPESCRIPT]
        )
        card_ts.assignees.add(self.user)

        progress = models.TopicProgress(content_item=content_item, user=self.user)
        progress.save()

        with self.assertRaises(FlavourProgressMismatchError):
            update_topic_card_progress(self.user)

    def test_unstarted_topic_with_due_time_ready_to_ip(self):
        tomorrow = timezone.now() + timedelta(days=1)
        content_item = factories.ContentItemFactory(
            content_type=models.ContentItem.TOPIC,
        )

        card = factories.AgileCardFactory(content_item=content_item)
        card.assignees.add(self.user)

        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.READY)

        card.set_due_time(tomorrow)

        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.READY)

        card.start_topic()

        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.IN_PROGRESS)
        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.IN_PROGRESS)

        card.stop_topic()
        card.refresh_from_db()
        self.assertEqual(card.topic_progress.start_time, None)
        self.assertEqual(card.topic_progress.due_time, tomorrow)
        self.assertEqual(card.status, models.AgileCard.READY)

        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.READY)

        card.start_topic()
        card.finish_topic()

        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.COMPLETE)
        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.COMPLETE)

    def test_topic_needing_review_gets_correct_status_over_time(self):
        content_item = factories.ContentItemFactory(
            content_type=models.ContentItem.TOPIC, topic_needs_review=True
        )

        card = factories.AgileCardFactory(content_item=content_item)
        card.assignees.add(self.user)

        update_topic_card_progress(self.user)
        card.refresh_from_db()

        self.assertEqual(card.status, models.AgileCard.READY)

        card.start_topic()
        card.finish_topic()

        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.IN_REVIEW)
        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.IN_REVIEW)

        factories.TopicReviewFactory(
            topic_progress=card.topic_progress, status=NOT_YET_COMPETENT
        )

        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.REVIEW_FEEDBACK)
        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.REVIEW_FEEDBACK)

        card.finish_topic()

        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.IN_REVIEW)
        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.IN_REVIEW)

        factories.TopicReviewFactory(
            topic_progress=card.topic_progress, status=COMPETENT
        )

        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.COMPLETE)
        update_topic_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.COMPLETE)


class update_workshop_card_progress_Tests(TestCase):
    def setUp(self):
        self.user = core_factories.UserFactory()

    def test_no_flavours(self):

        content_item = factories.ContentItemFactory(
            content_type=models.ContentItem.WORKSHOP
        )

        card = factories.AgileCardFactory(content_item=content_item)
        card.assignees.add(self.user)

        update_workshop_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, card.READY)

        progress = factories.WorkshopAttendanceFactory(
            content_item=content_item, attendee_user=self.user
        )
        progress.save()

        update_workshop_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, card.COMPLETE)

    def test_with_flavours(self):
        content_item = factories.ContentItemFactory(
            content_type=models.ContentItem.WORKSHOP,
            flavours=[JAVASCRIPT, TYPESCRIPT],
        )

        card_ts = factories.AgileCardFactory(
            content_item=content_item, flavours=[TYPESCRIPT]
        )
        card_ts.assignees.add(self.user)

        card_js = factories.AgileCardFactory(
            content_item=content_item, flavours=[JAVASCRIPT]
        )
        card_js.assignees.add(self.user)

        progress = factories.WorkshopAttendanceFactory(
            content_item=content_item, attendee_user=self.user
        )
        progress.save()
        progress.flavours.add(
            taggit.models.Tag.objects.get_or_create(name=TYPESCRIPT)[0]
        )

        update_workshop_card_progress(self.user)
        card_ts.refresh_from_db()
        card_js.refresh_from_db()

        self.assertEqual(card_js.status, card_ts.READY)
        self.assertEqual(card_ts.status, card_ts.COMPLETE)

    def test_error_gets_raised_if_card_has_flavours_but_progress_doesnt(self):
        content_item = factories.ContentItemFactory(
            content_type=models.ContentItem.WORKSHOP,
            flavours=[JAVASCRIPT, TYPESCRIPT],
        )

        card_ts = factories.AgileCardFactory(
            content_item=content_item, flavours=[TYPESCRIPT]
        )
        card_ts.assignees.add(self.user)

        progress = factories.WorkshopAttendanceFactory(
            content_item=content_item, attendee_user=self.user
        )
        progress.save()

        with self.assertRaises(FlavourProgressMismatchError):
            update_workshop_card_progress(self.user)


class update_project_card_progress_Tests(TestCase):
    def setUp(self):
        self.user = core_factories.UserFactory()

    def test_no_flavours(self):

        content_item = factories.ProjectContentItemFactory()

        card = factories.AgileCardFactory(
            content_item=content_item, recruit_project=None
        )
        card.assignees.add(self.user)

        self.assertIsNone(card.recruit_project)

        update_project_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, card.READY)

        progress = factories.RecruitProjectFactory(
            content_item=content_item,
            review_request_time=timezone.now() - timezone.timedelta(days=1),
            start_time=timezone.now() - timezone.timedelta(days=2),
        )
        progress.recruit_users.add(self.user)

        factories.RecruitProjectReviewFactory(
            recruit_project=progress,
            status=NOT_YET_COMPETENT,
            timestamp=timezone.now(),
        )

        update_project_card_progress(self.user)
        card.refresh_from_db()
        self.assertEqual(card.status, models.AgileCard.REVIEW_FEEDBACK)

    def test_with_flavours(self):
        content_item = factories.ProjectContentItemFactory(
            content_type=models.ContentItem.PROJECT,
            flavours=[JAVASCRIPT, TYPESCRIPT],
        )

        card_ts = factories.AgileCardFactory(
            content_item=content_item,
            flavours=[TYPESCRIPT],
            recruit_project=None,
        )
        card_ts.assignees.add(self.user)

        card_js = factories.AgileCardFactory(
            content_item=content_item,
            flavours=[JAVASCRIPT],
            recruit_project=None,
        )
        card_js.assignees.add(self.user)

        progress = factories.RecruitProjectFactory(
            content_item=content_item,
            review_request_time=None,
            start_time=timezone.now() - timezone.timedelta(days=2),
        )
        progress.recruit_users.add(self.user)
        progress.flavours.add(
            taggit.models.Tag.objects.get_or_create(name=TYPESCRIPT)[0]
        )

        update_project_card_progress(self.user)
        card_ts.refresh_from_db()
        card_js.refresh_from_db()

        self.assertEqual(card_js.status, card_js.READY)
        self.assertEqual(card_ts.status, card_ts.IN_PROGRESS)


class RegenerateCardTests(TestCase):
    def setUp(self):
        self.topic = ContentItemFactory(content_type=models.ContentItem.TOPIC)
        self.project = ProjectContentItemFactory(
            content_type=models.ContentItem.PROJECT,
            project_submission_type=models.ContentItem.REPOSITORY,
        )
        self.workshop = ContentItemFactory(content_type=models.ContentItem.WORKSHOP)

        self.topic.set_flavours([JAVASCRIPT, TYPESCRIPT])
        self.project.set_flavours([JAVASCRIPT, TYPESCRIPT])
        self.workshop.set_flavours([JAVASCRIPT, TYPESCRIPT])

        self.js_curriculum = core_factories.CurriculumFactory()
        self.ts_curriculum = core_factories.CurriculumFactory()

        for o in [self.topic, self.project, self.workshop]:
            js_req = models.CurriculumContentRequirement.objects.create(
                content_item=o,
                curriculum=self.js_curriculum,
            )
            js_req.flavours.add(JAVASCRIPT)

            ts_req = models.CurriculumContentRequirement.objects.create(
                content_item=o,
                curriculum=self.ts_curriculum,
            )
            ts_req.flavours.add(TYPESCRIPT)

    def test_generate_cards_twice_for_one_course(self):
        registration = CourseRegistrationFactory(curriculum=self.js_curriculum)
        user = registration.user
        generate_all_content_cards_for_user(user)
        self.assertEqual(
            models.AgileCard.objects.filter(assignees__in=[user]).count(), 3
        )
        generate_all_content_cards_for_user(user)
        self.assertEqual(
            models.AgileCard.objects.filter(assignees__in=[user]).count(), 3
        )

    def test_generate_cards_twice_for_one_course(self):
        registration = CourseRegistrationFactory(curriculum=self.js_curriculum)
        user = registration.user
        registration = CourseRegistrationFactory(
            user=user, curriculum=self.ts_curriculum
        )

        generate_all_content_cards_for_user(user)
        self.assertEqual(
            models.AgileCard.objects.filter(assignees__in=[user]).count(), 6
        )
        generate_all_content_cards_for_user(user)
        self.assertEqual(
            models.AgileCard.objects.filter(assignees__in=[user]).count(), 6
        )
