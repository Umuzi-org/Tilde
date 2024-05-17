from factory.django import DjangoModelFactory
import factory

from curriculum_tracking import models
from curriculum_tracking.constants import NOT_YET_COMPETENT
from core.tests.factories import UserFactory, CurriculumFactory
from git_real.tests.factories import RepositoryFactory
from datetime import timedelta
from django.utils import timezone
from test_factories_common import FlavourMixin


def _content_url_generator():
    i = 1
    while True:
        yield f"https://raw.githubusercontent.com/Umuzi-org/tech-department/master/content/projects/tdd/simple-calculator/part-{i}/_index.md"
        i += 1


_content_url_iterator = _content_url_generator()


def _content_name_generator():
    i = 1
    while True:
        yield f"something awesome part {i}"
        i += 1


_content_name_iterator = _content_name_generator()


def _tag_name_generator():
    i = 1
    while True:
        yield f"tag{i}"
        i += 1


_tag_name_iterator = _tag_name_generator()


def _next_int_generator():
    i = 1
    while True:
        yield i
        i += 1


_next_int_iterator = _next_int_generator()


class TagMixin:
    @staticmethod
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(TagFactory())


class TagFactory(DjangoModelFactory):
    class Meta:
        model = "taggit.Tag"

    name = factory.LazyAttribute(lambda *args, **kwargs: next(_tag_name_iterator))


class ProjectContentItemFactory(DjangoModelFactory, TagMixin, FlavourMixin):
    class Meta:
        model = "curriculum_tracking.ContentItem"

    id = factory.LazyAttribute(
        lambda *args, **kwargs: models.ContentItem.get_next_available_id()
    )
    content_type = models.ContentItem.PROJECT
    title = factory.lazy_attribute(lambda *args, **kwargs: next(_content_name_iterator))
    url = factory.lazy_attribute(lambda *args, **kwargs: next(_content_url_iterator))
    project_submission_type = models.ContentItem.REPOSITORY
    template_repo = "https://github.com/Umuzi-org/bwahahhahaaaa"

    @factory.post_generation
    def flavours(self, *args, **kwargs):
        FlavourMixin.flavours(self, *args, **kwargs)

    @factory.post_generation
    def tags(self, *args, **kwargs):
        TagMixin.tags(self, *args, **kwargs)


class ContentItemFactory(DjangoModelFactory, FlavourMixin):
    class Meta:
        model = "curriculum_tracking.ContentItem"

    id = factory.LazyAttribute(
        lambda *args, **kwargs: models.ContentItem.get_next_available_id()
    )

    content_type = models.ContentItem.TOPIC
    title = factory.lazy_attribute(lambda *args, **kwargs: next(_content_name_iterator))
    url = factory.lazy_attribute(lambda *args, **kwargs: next(_content_url_iterator))

    @factory.post_generation
    def flavours(self, *args, **kwargs):
        FlavourMixin.flavours(self, *args, **kwargs)

    @factory.post_generation
    def tags(self, *args, **kwargs):
        TagMixin.tags(self, *args, **kwargs)


class ReviewTrustFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.ReviewTrust"

    user = factory.SubFactory(UserFactory)
    content_item = factory.SubFactory(ContentItemFactory)

    @factory.post_generation
    def flavours(self, *args, **kwargs):
        FlavourMixin.flavours(self, *args, **kwargs)


class RecruitProjectFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.RecruitProject"

    content_item = factory.SubFactory(ProjectContentItemFactory)
    due_time = timezone.now() + timedelta(days=1)
    repository = factory.SubFactory(RepositoryFactory)

    @factory.post_generation
    def reviewer_users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.reviewer_users.add(user)

    @factory.post_generation
    def recruit_users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.recruit_users.add(user)
        else:
            self.recruit_users.add(UserFactory())

    @factory.post_generation
    def flavours(self, *args, **kwargs):
        FlavourMixin.flavours(self, *args, **kwargs)


class RecruitProjectInReviewFactory(RecruitProjectFactory):
    start_time = factory.lazy_attribute(
        lambda *a, **k: timezone.now() - timedelta(days=15)
    )
    review_request_time = factory.lazy_attribute(
        lambda *a, **k: timezone.now() - timedelta(days=10)
    )

    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     manager = cls._get_manager(model_class)

    # agile_card = factory.SubFactory(AgileCardFactory)


#     project = RecruitProjectFactory(*args, **kwargs)
#     project.project.request_review(force_timestamp=timezone.now() + timedelta(days=10))
#     project.save()
#     return project


class RecruitProjectReviewFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.RecruitProjectReview"

    status = NOT_YET_COMPETENT
    timestamp = factory.lazy_attribute(
        lambda o: timezone.now()
    )  # TODO: sheena timestamp not being used properly in factory
    comments = "something seriously useful"
    recruit_project = factory.SubFactory(RecruitProjectInReviewFactory)
    reviewer_user = factory.SubFactory(UserFactory)


class TopicProgressFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.TopicProgress"

    user = factory.SubFactory(UserFactory)
    content_item = factory.SubFactory(ContentItemFactory)

    # due_time
    # start_time
    # complete_time
    # review_request_time
    @factory.post_generation
    def flavours(self, *args, **kwargs):
        FlavourMixin.flavours(self, *args, **kwargs)


class TopicReviewFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.TopicReview"

    status = NOT_YET_COMPETENT
    timestamp = timezone.now()
    comments = "something seriously useful"
    topic_progress = factory.SubFactory(TopicProgressFactory)
    reviewer_user = factory.SubFactory(UserFactory)


class ContentItemOrderFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.ContentItemOrder"

    pre = factory.SubFactory(ContentItemFactory)
    post = factory.SubFactory(ContentItemFactory)
    hard_requirement = True


class AgileCardFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.AgileCard"

    status = models.AgileCard.IN_PROGRESS
    is_hard_milestone = True
    is_soft_milestone = True
    recruit_project = factory.SubFactory(
        RecruitProjectFactory, start_time=timezone.now()
    )

    content_item = factory.LazyAttribute(
        lambda o: (
            o.recruit_project.content_item
            if o.recruit_project
            else ContentItemFactory()
        )
    )
    order = 1

    # assignees = factory.LazyAttribute(
    #     lambda o: o.recruit_project.recruit_users.all() if o.recruit_project else []
    # )
    # @factory.post_generation
    # def assignees(self, *args, **kwargs):
    #     xxx
    #     FlavourMixin.flavours(self, *args, **kwargs)

    @factory.post_generation
    def flavours(self, *args, **kwargs):
        FlavourMixin.flavours(self, *args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        instance = manager.create(*args, **kwargs)
        if instance.recruit_project:
            instance.assignees.set(instance.recruit_project.recruit_users.all())
            flavour_names = (
                instance.flavour_names + instance.recruit_project.flavour_names
            )
            instance.set_flavours(flavour_names)
            instance.recruit_project.set_flavours(flavour_names)
        return instance

    @factory.post_generation
    def assignees(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # print(f"extracted = {extracted}")
            for user in extracted:
                self.assignees.add(user)
        elif self.recruit_project:
            for user in self.recruit_project.recruit_users.all():
                # print("here")
                self.assignees.add(user)
        elif self.topic_progress:
            todo
        elif self.workshop_attendance:
            todo
        else:
            self.assignees.set([UserFactory()])

    @factory.post_generation
    def reviewers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.reviewers.add(user)
        else:
            self.reviewers.add(UserFactory())


class RepoProjectAgileCardFactory(AgileCardFactory):
    class Meta:
        model = "curriculum_tracking.AgileCard"

    def create(user):
        repository = RepositoryFactory(user=user)
        recruit_project = RecruitProjectFactory(
            recruit_users=[user], repository=repository
        )
        card = AgileCardFactory(
            recruit_project=recruit_project,
            assignees=[user],
        )

        return card


class CurriculumContentRequirementFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.CurriculumContentRequirement"

    content_item = factory.SubFactory(ContentItemFactory)
    curriculum = factory.SubFactory(CurriculumFactory)
    hard_requirement = True
    order = factory.LazyAttribute(lambda o: next(_next_int_iterator))

    @factory.post_generation
    def flavours(self, *args, **kwargs):
        FlavourMixin.flavours(self, *args, **kwargs)


class CourseRegistrationFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.CourseRegistration"

    user = factory.SubFactory(UserFactory)
    curriculum = factory.SubFactory(CurriculumFactory)
    registration_date = factory.Faker("date")
    active = True
    suppress_card_generation = False
    order = factory.LazyAttribute(lambda o: next(_next_int_iterator))


class WorkshopAttendanceFactory(DjangoModelFactory):
    class Meta:
        model = "curriculum_tracking.WorkshopAttendance"

    attendee_user = factory.SubFactory(UserFactory)
    content_item = factory.SubFactory(ProjectContentItemFactory)
    timestamp = timezone.now()


class BurndownSnapshotFactory(DjangoModelFactory):
    class Meta:
        model = models.BurndownSnapshot

    user = factory.SubFactory(UserFactory)
    timestamp = timezone.now()
    cards_total_count = 10
    project_cards_total_count = 20
    cards_in_complete_column_total_count = 30
    project_cards_in_complete_column_total_count = 40


class ContentItemAgileWeightFactory(DjangoModelFactory):
    class Meta:
        model = models.ContentItemAgileWeight

    weight = 1
    content_item = factory.SubFactory(ContentItemFactory)

    @factory.post_generation
    def flavours(self, *args, **kwargs):
        FlavourMixin.flavours(self, *args, **kwargs)
