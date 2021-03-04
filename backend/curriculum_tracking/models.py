from typing import List
from django.db import models
from core.models import Curriculum, User, Team
from git_real import models as git_models
from taggit.managers import TaggableManager
from autoslug import AutoSlugField
from model_mixins import Mixins
from django.db.models import Q
from .validators import validate_content_item_url
from django.utils import timezone
import taggit
from django.core.exceptions import ValidationError
from social_auth import models as social_models
from git_real import helpers as git_helpers
from .constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
    RED_FLAG,
    EXCELLENT,
    REVIEW_STATUS_CHOICES,
)

from git_real.constants import GITHUB_BOT_USERNAME
import re

import logging

logger = logging.getLogger(__name__)


class ReviewableMixin:
    def is_trusted_reviewer(self, user):
        """should we take this user's review as the truth?"""
        if user.is_superuser:
            return True

        teams = self.get_teams()
        for team in teams:
            if user.has_perm(Team.PERMISSION_TRUSTED_REVIEWER, team):
                return True

        trusts = ReviewTrust.objects.filter(user=user, content_item=self.content_item)
        for trust in trusts:
            if trust.flavours_match(self.flavour_names):
                return True
        return False

    def cancel_request_review(self):
        self.review_request_time = None
        self.save()
        self.update_associated_card_status()

    def update_associated_card_status(self):
        try:
            card = self.agile_card
        except AgileCard.DoesNotExist:
            pass
        else:
            assert card is not None
            if card.status in [AgileCard.BLOCKED, AgileCard.READY]:
                return
            old_status = card.status
            if self.__class__ == RecruitProject:
                card.status = AgileCard.derive_status_from_project(self)
                progress_instance = card.recruit_project

            elif self.__class__ == TopicProgress:
                card.status = AgileCard.derive_status_from_topic(self, card)
                progress_instance = card.topic_progress

            else:
                raise Exception(f"Not implemented: {self.__class}")

            card.save()

    def latest_review(self, trusted=None, timestamp_greater_than=None):

        query = self.reviews_queryset()
        if trusted != None and self.__class__ == RecruitProject:
            query = query.filter(trusted=trusted)
        if timestamp_greater_than != None:
            query = query.filter(timestamp__gt=timestamp_greater_than)
        return query.order_by("timestamp").last()


class FlavourMixin:
    def flavours_match(self, flavour_strings: List[str]):
        return sorted(self.flavour_names) == sorted(flavour_strings)

    @property
    def flavour_names(self):
        return [o.name for o in self.flavours.all()]

    def set_flavours(self, flavour_strings):
        flavour_tags = [
            taggit.models.Tag.objects.get_or_create(name=name)[0]
            for name in flavour_strings
        ]

        for flavour in self.flavours.all():
            if flavour not in flavour_tags:
                self.flavours.remove(flavour)
        for tag in flavour_tags:
            if tag not in self.flavours.all():
                self.flavours.add(tag)


class ContentItemProxyMixin:
    @property
    def content_type_nice(self):
        return self.content_item.content_type_nice

    @property
    def content_type(self):
        return self.content_item.content_type

    @property
    def title(self):
        return self.content_item.title

    @property
    def content_url(self):
        return self.content_item.url

    @property
    def story_points(self):
        return self.content_item.story_points

    @property
    def tag_names(self):
        return self.content_item.tag_names

    @property
    def submission_type_nice(self):
        return self.content_item.project_submission_type_nice

    @property
    def topic_needs_review(self):
        return self.content_item.topic_needs_review

    @property
    def project_submission_type_nice(self):
        return self.content_item.project_submission_type_nice

    @property
    def topic_needs_review(self):
        return self.content_item.topic_needs_review


class TagMixin:
    @property
    def tag_names(self):
        return [o.name for o in self.tags.all()]


class CourseRegistration(models.Model):
    """associates a user with a curriculum"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="course_registrations"
    )
    curriculum = models.ForeignKey(Curriculum, on_delete=models.PROTECT)
    registration_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    suppress_card_generation = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ["order"]

    def __str__(self):
        return f"{self.user.email} - {self.curriculum.short_name}"


class ContentItemOrder(models.Model, Mixins):
    post = models.ForeignKey(
        "ContentItem", on_delete=models.PROTECT, related_name="pre_ordered_content"
    )
    pre = models.ForeignKey(
        "ContentItem", on_delete=models.PROTECT, related_name="post_ordered_content"
    )
    hard_requirement = models.BooleanField(default=True)

    class Meta:
        unique_together = [["pre", "post"]]

    @property
    def pre_title(self):
        return self.pre.title

    @property
    def post_title(self):
        return self.post.title


class ContentItem(models.Model, Mixins, FlavourMixin, TagMixin):
    # NQF_ASSESSMENT = "N"
    PROJECT = "P"
    TOPIC = "T"
    WORKSHOP = "W"

    CONTENT_TYPES = [
        # (NQF_ASSESSMENT, "NQF assessment"),
        (PROJECT, "project"),
        (TOPIC, "topic"),
        (WORKSHOP, "workshop"),
    ]

    REPOSITORY = "R"
    LINK = "L"
    CONTINUE_REPO = "C"
    NO_SUBMIT = "N"

    PROJECT_SUBMISSION_TYPES = [
        (REPOSITORY, "repo"),
        (LINK, "link"),
        (CONTINUE_REPO, "continue_repo"),
        (NO_SUBMIT, "nosubmit"),
    ]

    content_type = models.CharField(
        max_length=1, choices=CONTENT_TYPES, null=False, blank=False
    )
    title = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from="title", max_length=150)

    url = models.URLField(
        max_length=2083,
        blank=True,
        null=True,
        unique=True,
        validators=[validate_content_item_url],
    )

    story_points = models.SmallIntegerField(
        choices=((i, i) for i in [1, 2, 3, 5, 8, 13, 21, 34, 56, 89]), null=True
    )

    prerequisites = models.ManyToManyField(
        "ContentItem",
        related_name="unlocks",
        through="ContentItemOrder",
        symmetrical=False,
    )

    tags = TaggableManager(blank=True)

    flavours = models.ManyToManyField(
        taggit.models.Tag,
        blank=True,
        through="ContentAvailableFlavour",
        related_name="content_with_flavour",
    )
    topic_needs_review = models.BooleanField(default=False)

    project_submission_type = models.CharField(
        max_length=1, choices=PROJECT_SUBMISSION_TYPES, null=True, blank=True
    )
    continue_from_repo = models.ForeignKey(
        "ContentItem", null=True, blank=True, on_delete=models.PROTECT
    )
    template_repo = models.URLField(null=True, blank=True)  # should be a github repo
    link_regex = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        unique_together = [["content_type", "title"]]

    @classmethod
    def get_next_available_id(cls):
        """get the next available content item id"""
        from django.db.models import Max

        max_id = cls.objects.aggregate(Max("id"))["id__max"]
        return (max_id or 0) + 1

    def save(self, *args, **kwargs):
        if self.topic_needs_review:
            if self.content_type != self.TOPIC:
                raise ValidationError(
                    f"Cannot set `topic_needs_review` for non TOPIC item. content_type = {self.content_type}"
                )
        if self.content_type == self.PROJECT:
            if self.project_submission_type == None:
                raise ValidationError(
                    "Since this is a Project, the submission type cannot be null"
                )

            if self.template_repo:
                if self.project_submission_type != self.REPOSITORY:
                    raise ValidationError(
                        f"Can only set template repository for repo type submissions. This submission type is: {self.project_submission_type}"
                    )
            if self.project_submission_type == self.CONTINUE_REPO:
                if (
                    self.continue_from_repo == None
                    or self.continue_from_repo.content_type != self.PROJECT
                    or self.continue_from_repo.project_submission_type
                    != self.REPOSITORY
                ):
                    # breakpoint()
                    raise ValidationError(
                        f"cannot continue from a repo without specifying a valid repo to continue from! please point to a project content item that has a repo submission type\n\tcontinue_from_repo={self.continue_from_repo}"
                    )
        super(ContentItem, self).save(*args, **kwargs)

    def __str__(self):
        name = self.title or self.url or ""
        return f"{self.content_type}: {name}"

    @property
    def project_submission_type_nice(self):
        return dict(ContentItem.PROJECT_SUBMISSION_TYPES).get(
            self.project_submission_type
        )

    @property
    def content_type_nice(self):
        return dict(ContentItem.CONTENT_TYPES).get(self.content_type, "MISSING TYPE")

    def all_prerequisite_content_items(self):
        return [o.pre for o in self.pre_ordered_content.all()]

    def hard_prerequisite_content_items(self):
        return [o.pre for o in self.pre_ordered_content.filter(hard_requirement=True)]


class ContentAvailableFlavour(models.Model):
    tag = models.ForeignKey(taggit.models.Tag, on_delete=models.PROTECT)
    content_item = models.ForeignKey("ContentItem", on_delete=models.CASCADE)


class CurriculumContentRequirement(
    models.Model, Mixins, FlavourMixin, ContentItemProxyMixin
):
    content_item = models.ForeignKey(
        ContentItem,
        on_delete=models.CASCADE,
    )
    # TODO: protect
    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, related_name="content_requirements"
    )

    hard_requirement = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    # auto_added = models.BooleanField(default=False, editable=False)
    flavours = TaggableManager(blank=True)

    class Meta(object):
        ordering = ["order"]


class ReviewTrust(models.Model, FlavourMixin, ContentItemProxyMixin):
    content_item = models.ForeignKey(ContentItem, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    flavours = TaggableManager(blank=True)

    def __str__(self):
        return f"{self.content_item} {[f.name for f in self.flavours.all()]}"

    def update_previous_reviews(self):
        if self.content_item.content_type == ContentItem.TOPIC:
            raise NotImplementedError()

        previous_untrusted_reviews = RecruitProjectReview.objects.filter(
            reviewer_user=self.user,
            recruit_project__content_item=self.content_item,
            trusted=False,
        )

        previous_untrusted_reviews = [
            o
            for o in previous_untrusted_reviews
            if o.recruit_project.flavours_match([o.name for o in self.flavours.all()])
        ]

        for review in previous_untrusted_reviews:
            card = review.recruit_project.agile_card
            if card.status == AgileCard.IN_REVIEW:
                review.trusted = True
                review.save()
                review.recruit_project.update_associated_card_status()
                review.update_recent_validation_flags_for_project()


class RecruitProject(
    models.Model, Mixins, FlavourMixin, ReviewableMixin, ContentItemProxyMixin
):
    """what a recruit has done with a specific ContentItem"""

    content_item = models.ForeignKey(ContentItem, on_delete=models.PROTECT)
    complete_time = models.DateTimeField(null=True, blank=True)
    review_request_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    due_time = models.DateTimeField(null=True, blank=True)

    # deadline_status = models.CharField()
    repository = models.ForeignKey(
        git_models.Repository,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="recruit_projects",
    )
    link_submission = models.URLField(max_length=200, blank=True, null=True)

    recruit_users = models.ManyToManyField(User, related_name="recruit_projects")

    reviewer_users = models.ManyToManyField(
        User, related_name="projects_to_review", blank=True, default=list
    )
    ### below this line are our denormalised fields
    # latest_review = models.ForeignKey("RecruitProjectReview", null=True, blank=True)
    code_review_competent_since_last_review_request = models.IntegerField(default=0)
    code_review_excellent_since_last_review_request = models.IntegerField(default=0)
    code_review_red_flag_since_last_review_request = models.IntegerField(default=0)
    code_review_ny_competent_since_last_review_request = models.IntegerField(default=0)

    flavours = TaggableManager(blank=True)

    class Meta:
        unique_together = [
            ["content_item", "repository"],
        ]

    def get_teams(self):
        """return the teams of the users invoved in this project"""
        user_ids = [user.id for user in self.recruit_users.all()] + [
            user.id for user in self.reviewer_users.all()
        ]
        return Team.get_teams_from_user_ids(user_ids)

    def reviews_queryset(self):
        return self.project_reviews

    def save(self, *args, **kwargs):
        if self.content_item.project_submission_type == ContentItem.NO_SUBMIT:
            raise ValidationError(
                f"Nosubmit Project cant be submitted. So this instance makes no sense. {self.content_item}"
            )
        if self.link_submission and not self.link_submission_is_valid():
            raise ValidationError(self.link_submission_invalid_message())

        super(RecruitProject, self).save(*args, **kwargs)

    def link_submission_invalid_message(self, link_submission=None):
        link = link_submission or self.link_submission
        regex = self.content_item.link_regex or "^https{0,1}://.*"
        return f"link {link} does not match pattern: {regex}"

    def link_submission_is_valid(self, link_submission=None):
        link = link_submission or self.link_submission
        regex = self.content_item.link_regex or "^https{0,1}://.*"
        return bool(re.match(regex, link))

    def invite_github_collaborators_to_repo(self):
        from social_auth.github_api import Api
        from git_real.helpers import add_collaborator

        users = list(self.recruit_users.all()) + list(self.reviewer_users.all())
        assert len(users) >= 1, "This repo has no collaborators to add"
        api = Api(GITHUB_BOT_USERNAME)
        for user in users:
            add_collaborator(
                api, self.repository.full_name, user.social_profile.github_name
            )

    def create_repo_and_assign_collaborators(self, card_flavour_names):

        from git_real.constants import GITHUB_BOT_USERNAME, ORGANISATION

        github_auth_login = GITHUB_BOT_USERNAME

        assert (
            self.recruit_users.count() == 1
        ), f"There should be 1 assignee. No more and no less: {self.assignees.all()}"
        recruit_user = self.recruit_users.first()

        try:
            social = social_models.SocialProfile.objects.get(user=recruit_user)
        except social_models.SocialProfile.DoesNotExist:
            logger.error(f"{recruit_user.id} {recruit_user} has no github name")
            raise
        github_name = social.github_name
        assert github_name, f"{recruit_user.id} {recruit_user} has no github name"

        repo_name = self._generate_repo_name_for_project(
            user=recruit_user,
            flavour_names=card_flavour_names,
            content_item=self.content_item,
        )

        repo_full_name = f"{ORGANISATION}/{repo_name}"
        readme_text = "\n".join(
            [
                f"{self.content_item.title} ({self.content_item.id})",
                f"For raw project instructions see: {self.content_item.url}",
            ]
        )

        git_helpers.create_repo_and_assign_contributer(
            github_auth_login,
            repo_full_name,
            github_user_name=github_name,
            readme_text=readme_text,
        )

        repo_dict = git_helpers.get_repo(
            github_auth_login=github_auth_login, repo_full_name=repo_full_name
        )

        repo = git_helpers.save_repo(
            repo_dict
        )  # note thet the repo itself doesn't "belong" to anyone

        self.repository = repo
        self.invite_github_collaborators_to_repo()
        self.save()

    def __str__(self):
        users = ", ".join([str(o) for o in self.recruit_users.all()])
        s = f"{self.content_item} - {users}"
        flavours = [o.name for o in self.flavours.all()]
        if flavours:
            return f"{s} [{flavours}]"
        return s

    @staticmethod
    def _generate_repo_name_for_project(content_item, user, flavour_names):
        """when we create repos for recruit projects then we need names. for the repos. This creates those names"""
        clean_name = lambda s: "".join([c for c in s if c.isalnum()])
        slug = content_item.slug
        first_name = clean_name(user.first_name)
        last_name = clean_name(user.last_name)

        assert first_name, "user has no first name!"
        assert last_name, "user has no last name!"

        project_name = f"{first_name}-{last_name}-{content_item.id}-{slug}-{'-'.join(flavour_names)}"
        if len(project_name) > 100:

            diff = len(project_name) - 100
            slug = slug[:-diff]
            project_name = f"{first_name}-{last_name}-{slug}-{content_item.id}-{'-'.join(flavour_names)}"
            assert (
                len(project_name) == 100
            ), f"len({project_name}) ={len(project_name)}. Expected 100 "
        return project_name

    def request_review(self, force_timestamp=None):
        # self.review_request_time = (
        #     force_timestamp or self.review_request_time or timezone.now()
        # )
        assert self.start_time, "cannot request a review if the project isn't started"

        self.review_request_time = force_timestamp or timezone.now()

        self.code_review_competent_since_last_review_request = 0
        self.code_review_excellent_since_last_review_request = 0
        self.code_review_ny_competent_since_last_review_request = 0
        self.code_review_red_flag_since_last_review_request = 0
        self.save()
        self.update_associated_card_status()

    @property
    def recruit_user_names(self):
        return [o.email for o in self.recruit_users.all()]

    @property
    def reviewer_user_names(self):
        return [o.email for o in self.reviewer_users.all()]

    @property
    def agile_card_status(self):
        return self.agile_card.status


class RecruitProjectReview(models.Model, Mixins):

    INCORRECT = "i"
    CORRECT = "c"
    CONTRADICTED = "d"

    REVIEW_VALIDATED_STATUS_CHOICES = [
        (INCORRECT, "incorrect"),
        (CORRECT, "correct"),
        (CONTRADICTED, "contradicted"),
    ]

    status = models.CharField(
        max_length=3,
        choices=REVIEW_STATUS_CHOICES,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    recruit_project = models.ForeignKey(
        RecruitProject, on_delete=models.CASCADE, related_name="project_reviews"
    )
    reviewer_user = models.ForeignKey(User, on_delete=models.PROTECT)
    trusted = (
        models.BooleanField()
    )  # when this review was created, was the user trusted?

    validated = models.CharField(
        choices=REVIEW_VALIDATED_STATUS_CHOICES, max_length=1, null=True, blank=True
    )

    def __str__(self):
        # feel free to edit this
        return f"{self.recruit_project} = {self.status}"

    @property
    def reviewer_user_email(self):
        return self.reviewer_user.email

    def update_recent_validation_flags_for_project(self):
        """this review was just added. Look at recent reviews to see if there is agreement or contradiction"""
        reviews = RecruitProjectReview.objects.filter(
            recruit_project=self.recruit_project
        ).filter(timestamp__lt=self.timestamp)
        since_time = self.recruit_project.review_request_time
        if since_time:
            reviews = reviews.filter(timestamp__gte=since_time)

        for review in reviews:
            review.update_validated_from(self)

    def update_validated_from(self, other):
        positive = [COMPETENT, EXCELLENT]
        negative = [NOT_YET_COMPETENT, RED_FLAG]
        if other.trusted:
            if self.status in positive and other.status in positive:
                self.validated = RecruitProjectReview.CORRECT
            else:
                self.validated = RecruitProjectReview.INCORRECT
        else:
            if self.status in positive and other.status in negative:
                self.validated = RecruitProjectReview.CONTRADICTED
        self.save()


class TopicProgress(models.Model, Mixins, ContentItemProxyMixin, ReviewableMixin):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    content_item = models.ForeignKey(ContentItem, on_delete=models.PROTECT)
    due_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    complete_time = models.DateTimeField(blank=True, null=True)
    review_request_time = models.DateTimeField(blank=True, null=True)
    flavours = TaggableManager(blank=True)

    def reviews_queryset(self):
        return self.topic_reviews


class TopicReview(models.Model, Mixins):
    status = models.CharField(
        max_length=3,
        choices=REVIEW_STATUS_CHOICES,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    topic_progress = models.ForeignKey(
        TopicProgress, on_delete=models.CASCADE, related_name="topic_reviews"
    )
    reviewer_user = models.ForeignKey(User, on_delete=models.PROTECT)

    @property
    def reviewer_user_email(self):
        return self.reviewer_user.email


class WorkshopAttendance(models.Model, Mixins, ContentItemProxyMixin):
    timestamp = models.DateTimeField()
    content_item = models.ForeignKey(ContentItem, on_delete=models.PROTECT)
    attendee_user = models.ForeignKey(User, on_delete=models.PROTECT)
    flavours = TaggableManager(blank=True)


class AgileCard(models.Model, Mixins, FlavourMixin, ContentItemProxyMixin):
    BLOCKED = "B"
    READY = "R"
    IN_PROGRESS = "IP"
    REVIEW_FEEDBACK = "RF"
    IN_REVIEW = "IR"
    COMPLETE = "C"

    STATUS_CHOICES = [
        (BLOCKED, "Blocked"),
        (READY, "Ready"),
        (IN_PROGRESS, "In Progress"),
        (REVIEW_FEEDBACK, "Review Feedback"),
        (IN_REVIEW, "Review"),
        (COMPLETE, "Complete"),
    ]

    TRUSTED_REVIEW_STATUS_TO_CARD_STATUS = {
        NOT_YET_COMPETENT: REVIEW_FEEDBACK,
        RED_FLAG: REVIEW_FEEDBACK,
        COMPETENT: COMPLETE,
        EXCELLENT: COMPLETE,
    }

    content_item = models.ForeignKey(ContentItem, on_delete=models.PROTECT)
    flavours = TaggableManager(blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)

    workshop_attendance = models.OneToOneField(
        WorkshopAttendance,
        null=True,
        blank=True,
        unique=True,
        on_delete=models.SET_NULL,
        related_name="agile_card",
    )

    topic_progress = models.OneToOneField(
        TopicProgress,
        null=True,
        blank=True,
        unique=True,
        on_delete=models.SET_NULL,
        related_name="agile_card",
    )

    recruit_project = models.OneToOneField(
        RecruitProject,
        null=True,
        blank=True,
        unique=True,
        on_delete=models.SET_NULL,
        related_name="agile_card",
    )
    assignees = models.ManyToManyField(
        User,
        related_name="assigned_agile_cards",
        blank=True,
    )
    reviewers = models.ManyToManyField(
        User,
        related_name="agile_cards_to_review",
        blank=True,
    )

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    is_hard_milestone = (
        models.BooleanField()
    )  # is it a hard requirement of a curriculum
    is_soft_milestone = (
        models.BooleanField()
    )  # is it an optional requirement of a curriculum

    # if it is not an explicit goal then both are false

    requires_cards = models.ManyToManyField(
        "AgileCard", related_name="required_by_cards"
    )

    # cards are automatically generated and pruned based on what is in the user's
    # curriculum and what they h\ave done so far. Sometimes they really shouldn't be pruned.
    # this field is filled in by signals

    @property
    def progress_instance(self):
        if self.recruit_project_id:
            return self.recruit_project
        if self.topic_progress_id:
            return self.topic_progress
        if self.workshop_attendance_id:
            return self.workshop_attendance

    def save(self, *args, **kwargs):
        if self.content_item.project_submission_type == ContentItem.NO_SUBMIT:
            raise ValidationError(
                f"Nosubmit Project cannot be converted to a card. {self.content_item}"
            )
        super(AgileCard, self).save(*args, **kwargs)

    def status_ready_or_blocked(self):
        """if there was no progress on this card, would the status be READY or BLOCKED?It would be blocked if the prerequisites are not met"""
        from django.db.models import Q

        if self.requires_cards.filter(~Q(status=self.COMPLETE)).count():
            return self.BLOCKED
        return self.READY

    @property
    def due_time(self):
        if self.recruit_project:
            return self.recruit_project.due_time
        if self.topic_progress:
            return self.topic_progress.due_time

    @property
    def complete_time(self):
        if self.recruit_project:
            return self.recruit_project.complete_time
        if self.topic_progress:
            return self.topic_progress.complete_time

    @property
    def review_request_time(self):
        if self.recruit_project:
            return self.recruit_project.review_request_time
        if self.topic_progress:
            return self.topic_progress.review_request_time

    @property
    def start_time(self):
        if self.recruit_project:
            return self.recruit_project.start_time
        if self.topic_progress:
            return self.topic_progress.start_time

    @property
    def project_review_request_time(self):
        return self.recruit_project.review_request_time

    @property
    def project_link_submission(self):
        return self.project.link_submission

    def __str__(self):
        # feel free to edit this
        return f"{self.status}:{self.content_item}"

    @classmethod
    def _get_status_from_review(cls, get_trusted_review, get_untrusted_review):
        trusted_review = get_trusted_review()
        if trusted_review:
            return cls.TRUSTED_REVIEW_STATUS_TO_CARD_STATUS[trusted_review.status]

        untrusted_review = get_untrusted_review()
        if untrusted_review:
            status = untrusted_review.status
            if status in [
                NOT_YET_COMPETENT,
                RED_FLAG,
            ]:
                return cls.REVIEW_FEEDBACK

        return cls.IN_REVIEW

    @classmethod
    def derive_status_from_topic(cls, progress, card):
        if progress.complete_time:
            return cls.COMPLETE
        elif progress.review_request_time:

            get_trusted_review = lambda: progress.latest_review(
                timestamp_greater_than=progress.review_request_time
            )

            # get_untrusted_review = lambda:progress.latest_review(
            #     trusted=False, timestamp_greater_than=progress.review_request_time
            # )

            return cls._get_status_from_review(get_trusted_review, get_trusted_review)
        elif progress.start_time:
            return cls.IN_PROGRESS
        else:
            return card.status_ready_or_blocked()

    @classmethod
    def derive_status_from_project(cls, project):
        if not project.start_time:
            try:
                card = project.agile_card
                return card.status_ready_or_blocked()
            except AgileCard.DoesNotExist:
                pass

        if project.review_request_time:
            get_trusted_review = lambda: project.latest_review(
                trusted=True, timestamp_greater_than=project.review_request_time
            )

            get_untrusted_review = lambda: project.latest_review(
                trusted=False, timestamp_greater_than=project.review_request_time
            )

            return cls._get_status_from_review(get_trusted_review, get_untrusted_review)
        else:
            # could have been reviewed ahead of time by a trusted..
            review = project.latest_review(trusted=True)
            if review:
                return cls.TRUSTED_REVIEW_STATUS_TO_CARD_STATUS[review.status]

            return cls.IN_PROGRESS

    def set_instance_flavours_to_match(self, progress_instance):
        for flavour in self.flavours.all():
            progress_instance.flavours.add(flavour)
        for flavour in progress_instance.flavours.all():
            if flavour not in self.flavours.all():
                progress_instance.flavours.remove(flavour)

    def set_due_time(self, time):
        content_type = self.content_item.content_type
        if content_type == ContentItem.PROJECT:
            self._create_project_progress_if_not_exists()

            self.recruit_project.due_time = time
            self.recruit_project.save()

        elif content_type == ContentItem.TOPIC:

            self._create_topic_progress_if_not_exists()
            self.topic_progress.due_time = time
            self.topic_progress.save()
        else:
            raise NotImplemented(
                f"Can't set due time for content of type {content_type}"
            )

    def _create_project_progress_if_not_exists(self):

        if self.recruit_project:
            return
        project = RecruitProject.objects.create(content_item=self.content_item)

        project.recruit_users.set(self.assignees.all())
        project.reviewer_users.set(self.reviewers.all())
        project.save()
        self.recruit_project = project
        self.set_instance_flavours_to_match(self.recruit_project)
        self.save()

    def _get_repo_to_continue_from(self):
        card = self.requires_cards.get(
            content_item=self.content_item.continue_from_repo
        )
        repo = card.recruit_project.repository
        assert (
            repo is not None
        ), f"Cant continue: Repo is missing \n\tcurrent card id = {self.id} \n\tcontinue from card id = {card.id}"
        return repo

    def start_project(self):
        """the user has chosen to start a project. That means:
        - create the project (if not exists)
        - create the repo (ditto)
        - add assignees as collaborator
        """
        from .helpers import create_or_update_single_project_card
        from long_running_request_actors import add_collaborator_and_protect_master

        assert (
            self.assignees.count() == 1
        ), f"There should be 1 assignee. No more and no less: {self.assignees.all()}"

        self._create_project_progress_if_not_exists()

        if self.content_item.project_submission_type == ContentItem.REPOSITORY:
            self.recruit_project.create_repo_and_assign_collaborators(
                card_flavour_names=self.flavour_names
            )
            assert self.recruit_project.repository
            # retry it just in case of github having eventual consistency issues

            add_collaborator_and_protect_master.send_with_options(
                kwargs={"project_id": self.recruit_project.id},
                delay=10000,  # 10 seconds
            )

        elif self.content_item.project_submission_type == ContentItem.CONTINUE_REPO:
            self.recruit_project.repository = self._get_repo_to_continue_from()
            self.recruit_project.invite_github_collaborators_to_repo()

        elif self.content_item.project_submission_type == ContentItem.LINK:
            pass  # nothing to do
        else:
            raise NotImplemented(
                f"Cannot start project of type {self.content_item.project_submission_type}"
            )

        self.recruit_project.start_time = timezone.now()
        self.recruit_project.save()
        create_or_update_single_project_card(self.recruit_project)
        self.refresh_from_db()

    def can_start(self, force=False):
        """should the "start" button exist on this card?
        If force = True then assume the user has super access
        """
        if force:
            return self.status in [AgileCard.READY, AgileCard.BLOCKED]
        # TODO: this should do useful things...
        # only allow if active cards are minimal
        return self.status == AgileCard.READY

    def can_force_start(self):
        return self.can_start(force=True)

    def _create_topic_progress_if_not_exists(self):
        if self.topic_progress:
            return
        self.topic_progress = TopicProgress.objects.create(
            user=self.assignees.first(), content_item=self.content_item
        )
        self.set_instance_flavours_to_match(self.topic_progress)
        self.save()

    def start_topic(self):
        assert self.status == AgileCard.READY
        assert (
            self.assignees.count() == 1
        ), f"Assignee count is screwy: {self} - {self.assignees.all()}"
        assert (
            self.content_item.content_type == ContentItem.TOPIC
        ), f"{self.content_item.content_type}"

        self._create_topic_progress_if_not_exists()

        self.topic_progress.start_time = timezone.now()
        self.status = AgileCard.IN_PROGRESS
        self.save()
        self.topic_progress.save()

    def finish_topic(self):
        """This is called when a recruit says they are finished. There might still be a review stage"""
        assert self.status in [AgileCard.IN_PROGRESS, AgileCard.REVIEW_FEEDBACK]
        assert self.topic_progress != None, f"Topic hasn't been started"
        assert (
            self.content_item.content_type == ContentItem.TOPIC
        ), f"{self.content_item.content_type}"
        if self.content_item.topic_needs_review:
            self.topic_progress.review_request_time = timezone.now()
            self.topic_progress.save()
            self.status = AgileCard.IN_REVIEW
        else:
            self.topic_progress.complete_time = timezone.now()
            self.topic_progress.save()
            self.status = AgileCard.COMPLETE
        self.save()

    def stop_topic(self):
        assert self.status == AgileCard.IN_PROGRESS
        assert self.topic_progress != None, f"Topic hasn't been started"
        assert (
            self.content_item.content_type == ContentItem.TOPIC
        ), f"{self.content_item.content_type}"
        self.topic_progress.start_time = None
        self.topic_progress.save()
        self.status = AgileCard.READY
        self.save()

    def attended_workshop(self, timestamp):
        # if self.status == AgileCard.COMPLETE:
        #     return
        assert self.status in [AgileCard.READY, AgileCard.BLOCKED], self.status
        assert (
            self.content_item.content_type == ContentItem.WORKSHOP
        ), f"{self.content_item.content_type}"
        assert self.workshop_attendance == None, f"Workshop already attended"
        assert (
            self.assignees.count() == 1
        ), f"Assignee count is screwy: {self} - {self.assignees.all()}"

        self.workshop_attendance = WorkshopAttendance.objects.create(
            timestamp=timestamp,
            content_item=self.content_item,
            attendee_user=self.assignees.first(),
        )
        self.status = AgileCard.COMPLETE
        self.set_instance_flavours_to_match(self.workshop_attendance)

        self.save()

    def delete_workshop_attendance(self):
        assert self.status == AgileCard.COMPLETE
        assert (
            self.content_item.content_type == ContentItem.WORKSHOP
        ), f"{self.content_item.content_type}"
        assert self.workshop_attendance != None, f"Workshop not yet attended"

        attendance = self.workshop_attendance
        self.workshop_attendance = None
        self.status = AgileCard.READY
        self.save()
        attendance.delete()

    @property
    def repository(self):
        return self.recruit_project.repository

    @property
    def assignee_names(self):
        return [o.email for o in self.assignees.all()]

    @property
    def reviewer_names(self):
        return [o.email for o in self.reviewers.all()]

    @property
    def content_item_url(self):
        return self.content_item.url

    @property
    def code_review_competent_since_last_review_request(self):
        if self.recruit_project:
            return self.recruit_project.code_review_competent_since_last_review_request
        return 0

    @property
    def code_review_excellent_since_last_review_request(self):
        if self.recruit_project:
            return self.recruit_project.code_review_excellent_since_last_review_request
        return 0

    @property
    def code_review_red_flag_since_last_review_request(self):
        if self.recruit_project:
            return self.recruit_project.code_review_red_flag_since_last_review_request
        return 0

    @property
    def code_review_ny_competent_since_last_review_request(self):
        if self.recruit_project:
            return (
                self.recruit_project.code_review_ny_competent_since_last_review_request
            )
        return 0
