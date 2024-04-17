from datetime import timedelta, datetime
from typing import List
from django.db import models
from core.models import Curriculum, User, Team, TagMixin
from curriculum_tracking import helpers
from git_real import models as git_models
from taggit.managers import TaggableManager
from autoslug import AutoSlugField
from model_mixins import Mixins, FlavourMixin
from django.utils import timezone
import taggit
from django.core.exceptions import ValidationError
from social_auth import models as social_models
from .constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
    RED_FLAG,
    EXCELLENT,
    REVIEW_STATUS_CHOICES,
    POSITIVE_REVIEW_STATUS_CHOICES,
    NEGATIVE_REVIEW_STATUS_CHOICES,
)
from git_real.constants import GIT_REAL_BOT_USERNAME
import re
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)


class ReviewableMixin:
    def is_trusted_reviewer(self, user):
        """should we take this user's review as the truth?"""
        if user.is_superuser:
            return True

        if not self.content_item.title.startswith("Assessment"):
            # assessment cards need to have individual trust applied
            teams = self.get_teams(assignees_only=True)
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
            # old_status = card.status
            if self.__class__ == RecruitProject:
                card.status = AgileCard.derive_status_from_project(self)
                # progress_instance = card.recruit_project

            elif self.__class__ == TopicProgress:
                card.status = AgileCard.derive_status_from_topic(self, card)
                # progress_instance = card.topic_progress

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
    def tag_names(self):
        return self.content_item.tag_names

    @property
    def submission_type_nice(self):
        return self.content_item.project_submission_type_nice

    @property
    def project_submission_type_nice(self):
        return self.content_item.project_submission_type_nice

    @property
    def protect_main_branch(self):
        return self.content_item.protect_main_branch


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
        return f"{self.user.email} - {self.curriculum.name}"


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


class LearningOutcome(models.Model, Mixins):
    name = models.CharField(max_length=256)
    description = models.TextField()

    @classmethod
    def get_next_available_id(cls):
        """get the next available content item id"""
        from django.db.models import Max

        max_id = cls.objects.aggregate(Max("id"))["id__max"]
        return (max_id or 0) + 1


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
    blurb = models.TextField(null=True, blank=True)

    slug = AutoSlugField(populate_from="title", max_length=150)

    url = models.URLField(
        max_length=2083,
        blank=True,
        null=True,
        unique=True,
    )

    raw_url = models.URLField(
        max_length=2083,
        blank=True,
        null=True,
        unique=True,
    )

    prerequisites = models.ManyToManyField(
        "ContentItem",
        related_name="unlocks",
        through="ContentItemOrder",
        symmetrical=False,
    )

    tags = TaggableManager(blank=True)
    learning_outcomes = models.ManyToManyField(
        "LearningOutcome", blank=True, related_name="content_items"
    )

    flavours = models.ManyToManyField(
        taggit.models.Tag,
        blank=True,
        through="ContentAvailableFlavour",
        related_name="content_with_flavour",
    )

    project_submission_type = models.CharField(
        max_length=1, choices=PROJECT_SUBMISSION_TYPES, null=True, blank=True
    )
    continue_from_repo = models.ForeignKey(
        "ContentItem", null=True, blank=True, on_delete=models.PROTECT
    )
    template_repo = models.URLField(null=True, blank=True)  # should be a github repo

    link_regex = models.CharField(max_length=250, null=True, blank=True)
    link_name = models.CharField(max_length=250, null=True, blank=True)
    link_example = models.CharField(max_length=250, null=True, blank=True)
    link_message = models.TextField(null=True, blank=True)

    protect_main_branch = models.BooleanField(
        default=True
    )  # this is used in repo projects. If this is True then standard branch protection rules are applied. Otherwise they are not.

    class Meta:
        unique_together = [["content_type", "title"]]

    @classmethod
    def get_next_available_id(cls):
        """get the next available content item id"""
        from django.db.models import Max

        max_id = cls.objects.aggregate(Max("id"))["id__max"]
        return (max_id or 0) + 1

    def save(self, *args, **kwargs):
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

    class Meta:
        unique_together = [["tag", "content_item"]]


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
            # raise NotImplementedError()
            return

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

        previous_untrusted_reviews = [
            o
            for o in previous_untrusted_reviews
            if o.recruit_project.review_request_time
            and o.recruit_project.review_request_time < o.timestamp
        ]

        for review in previous_untrusted_reviews:
            try:
                card = review.recruit_project.agile_card
            except AgileCard.DoesNotExist:
                continue
            if card.status == AgileCard.IN_REVIEW:
                review.trusted = True
                review.save()
                review.recruit_project.update_associated_card_status()
                review.update_recent_validation_flags_for_project()

    @classmethod
    def add_specific_trust_instances(
        cls,
        who: str,
        content_item_title: str,
        flavours: List[str],
        update_previous_reviews: bool = False,
    ):
        """
        Create ReviewTrust instances for users. This function will not add duplicates.

        :param who: email address or team name. The users included here will each have a matching trust instance by the end
        :param content_item_title: nuf sed
        :param flavours: this needs to EXACTLY match the flavours on a card or associated reviews will not be trusted
        :param update_previous_reviews: if True then reviews that match these criteria are revisitted and marked as competent. Cards might move as a result
        """
        print(f"Adding trust for {who} `{content_item_title}` {flavours}")
        users = User.get_users_from_identifier(who)
        content_item = ContentItem.objects.get(title=content_item_title)
        if content_item.content_type != ContentItem.PROJECT:
            raise Exception(
                f"Can't add trust for non-project content: {content_item_title}"
            )
        available_flavours = content_item.flavours.all()
        available_flavour_names = [o.name for o in available_flavours]
        for flavour_name in flavours:
            assert (
                flavour_name in available_flavour_names
            ), f"{flavour_name} not allowed. choose from {available_flavour_names}"
        final_flavours = [o for o in available_flavours if o.name in flavours]

        trust_instances = []

        for user in users:
            trusts = cls.objects.filter(content_item=content_item, user=user)
            found = False
            for trust in trusts:
                if trust.flavours_match(flavours):
                    found = True
                    trust_instances.append(trust)
                    break
            if not found:
                # we make one
                trust = cls.objects.create(content_item=content_item, user=user)
                for flavour in final_flavours:
                    trust.flavours.add(flavour)
                trust_instances.append(trust)

        if update_previous_reviews:
            for trust in trust_instances:
                trust.update_previous_reviews()


class RecruitProject(
    models.Model, Mixins, FlavourMixin, ReviewableMixin, ContentItemProxyMixin
):
    """What a recruit has done with a specific ContentItem"""

    content_item = models.ForeignKey(
        ContentItem, on_delete=models.PROTECT, related_name="projects"
    )
    complete_time = models.DateTimeField(null=True, blank=True)
    review_request_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    due_time = models.DateTimeField(null=True, blank=True)

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

    # class Meta:   # TODO: this is a dangerous thing to comment out
    # but when altering csard flavours things can get a bit strange
    #     unique_together = [
    #         ["content_item", "repository"],
    #     ]

    def get_activity_log_summary_data(self):
        """This is used by the activityLog serializer"""
        try:
            card = self.agile_card
            card_id = card.id
        except AgileCard.DoesNotExist:
            card_id = None

        return {
            "card": card_id,
            "title": self.content_item.title,
            "flavour_names": self.flavour_names,
        }

    def users_that_reviewed_since_last_review_request(self):
        if self.review_request_time is None:
            return []

        reviews = RecruitProjectReview.objects.filter(recruit_project=self)

        reviews = reviews.filter(timestamp__gte=self.review_request_time)

        return [review.reviewer_user for review in reviews]

    @property
    def repo_url(self):
        if not self.repository:
            return None
        return self.repository.ssh_url

    @property
    def open_pr_count(self):
        repo = self.repository
        if repo:
            return repo.pull_requests.filter(state=git_models.PullRequest.OPEN).count()
        return 0

    @property
    def oldest_open_pr_updated_time(self):
        repo = self.repository
        if repo:
            pr = (
                repo.pull_requests.filter(state=git_models.PullRequest.OPEN)
                .order_by("updated_at")
                .first()
            )
            if pr:
                return pr.updated_at

    def get_users_with_permission(self, permissions):
        from guardian.shortcuts import get_users_with_perms

        teams = self.get_teams()
        result = []
        for team in teams:
            users = get_users_with_perms(obj=team)
            for user in users:
                if user.active and user not in result:
                    result.append(user)
        return result

    def get_teams(self, assignees_only=False):
        """return the teams of the users invoved in this project"""
        user_ids = [user.id for user in self.recruit_users.all()]
        if not assignees_only:
            user_ids.extend([user.id for user in self.reviewer_users.all()])
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
        from social_auth.models import SocialProfile
        from git_real.helpers import add_collaborator, list_collaborators

        api = Api(GIT_REAL_BOT_USERNAME)
        repo = self.repository
        existing_collaborators = list_collaborators(api, repo.full_name)

        collaborator_users = {
            "reviewer users": list(self.reviewer_users.filter(active=True)),
            "assigned users": list(self.recruit_users.filter(active=True)),
            "users with explicit permission": self.get_users_with_permission(
                Team.PERMISSION_REPO_COLLABORATER_AUTO_ADD
            ),
        }

        for list_name, users in collaborator_users.items():
            logger.info(f"Adding github collaborators from list: {list_name}")
            for user in users:
                logger.info(f"adding user {user} to repo...")
                if not user.active:
                    logger.info("user not active. Skipping")
                    continue
                try:
                    social_profile = user.social_profile

                except SocialProfile.DoesNotExist:
                    logger.info("user has no social profile. Skipping")
                    pass
                else:
                    github_name = social_profile.github_name
                    if not github_name:
                        logger.info("user has no github name. Skipping")
                    elif github_name in existing_collaborators:
                        logger.info("user is already a collaborator. Skipping")
                    else:
                        logger.info(f"adding github user {social_profile.github_name}")
                        add_collaborator(
                            api, repo.full_name, social_profile.github_name
                        )

    def get_recruit_user_github_name(self):
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
        return github_name

    def _get_or_create_repo(self, api):
        from git_real.constants import ORGANISATION
        from git_real.helpers import create_org_repo

        if self.content_item.project_submission_type == ContentItem.REPOSITORY:
            assert (
                self.recruit_users.count() == 1
            ), f"Expected only one user, got: {self.recruit_users.all()}"
            recruit_user = self.recruit_users.first()
            repo_name = self._generate_repo_name_for_project(
                user=recruit_user,
                flavour_names=self.flavour_names,
                content_item=self.content_item,
            )

            repo_full_name = f"{ORGANISATION}/{repo_name}"

            repo = create_org_repo(
                api=api, repo_full_name=repo_full_name, exists_ok=True, private=True
            )
            return repo
        if self.content_item.project_submission_type == ContentItem.CONTINUE_REPO:
            return self.agile_card._get_repo_to_continue_from()

        raise Exception(
            f"Cannot get or create a repo for content with submission_type {self.content_item.project_submission_type}"
        )

    def setup_repository(self, add_collaborators=True):
        from git_real.constants import GIT_REAL_BOT_USERNAME, ORGANISATION
        from git_real.helpers import (
            upload_readme,
            protect_master,
        )
        from social_auth.github_api import Api

        github_auth_login = GIT_REAL_BOT_USERNAME

        github_name = self.get_recruit_user_github_name()
        assert (
            self.recruit_users.count() == 1
        ), f"There should be 1 assignee. No more and no less: {self.assignees.all()}"
        recruit_user = self.recruit_users.first()

        assert self.flavour_names == self.agile_card.flavour_names

        readme_text = "\n".join(
            [
                f"{self.content_item.title} ({self.content_item.id})",
                f"For raw project instructions see: {self.content_item.url}",
            ]
        )

        api = Api(github_auth_login)

        repo = self._get_or_create_repo(api)
        # assert (
        #     repo.user == recruit_user
        # ), f"RecruitProject {self.id}: {repo.user} != {recruit_user}"

        assert (
            repo != None
        ), f"repo not created for project: {self.id} {self.content_item.title} {self.flavour_names} {self.recruit_users}"

        upload_readme(api=api, repo_full_name=repo.full_name, readme_text=readme_text)
        if self.protect_main_branch:
            protect_master(api, repo.full_name)
        self.repository = repo
        self.save()
        if add_collaborators:
            self.invite_github_collaborators_to_repo()

    def __str__(self):
        users = ", ".join([str(o) for o in self.recruit_users.all()])
        s = f"{self.id} {self.content_item} - {users}"
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
        # we import it from here because the broker needs to be set up.
        from long_running_request_actors import automark_single_project

        assert (
            self.start_time
        ), f"cannot request a review if the project isn't started - {self}"

        self.review_request_time = force_timestamp or timezone.now()

        self.code_review_competent_since_last_review_request = 0
        self.code_review_excellent_since_last_review_request = 0
        self.code_review_ny_competent_since_last_review_request = 0
        self.code_review_red_flag_since_last_review_request = 0
        self.save()
        self.update_associated_card_status()

        automark_single_project.send_with_options(
            kwargs={"project_id": self.id},
        )

    @property
    def recruit_user_names(self):
        return [o.email for o in self.recruit_users.all()]

    @property
    def reviewer_user_names(self):
        return [o.email for o in self.reviewer_users.all()]

    @property
    def agile_card_status(self):
        return self.agile_card.status

    @property
    def get_total_duration(self):
        return helpers.get_blant_duration(self.id, self.agile_card_status)


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

    # if a user leaves a negative review and then another review is requested then two things can happen:
    # either the next review is negative (meaning the previous review was incomplete or incompletely implemented) or
    # the card is closed (meaning the previous negative review was complete and completely implemented)
    complete_review_cycle = models.BooleanField(null=True, blank=True)

    def __str__(self):
        # feel free to edit this
        return f"{self.recruit_project} = {self.status}"

    def get_activity_log_summary_data(self):
        """This is used by the activityLog serializer"""
        project = self.recruit_project
        try:
            card = project.agile_card
            card_id = card.id
        except AgileCard.DoesNotExist:
            card_id = None

        return {
            "recruit_project": project.id,
            "card": card_id,
            "title": project.content_item.title,
            "flavour_names": project.flavour_names,
        }

    @property
    def reviewer_user_email(self):
        return self.reviewer_user.email

    def update_recent_validation_flags_for_project(self):
        """this review was just added. Look at recent reviews to see if there is agreement or contradiction"""
        reviews = RecruitProjectReview.objects.filter(
            recruit_project=self.recruit_project
        ).filter(timestamp__lt=self.timestamp)

        last_review_request_time = self.recruit_project.review_request_time

        # take a look at all the reviews that happened since the last review request

        recent_reviews = (
            reviews.filter(timestamp__gte=last_review_request_time)
            if last_review_request_time
            else reviews
        ).exclude(reviewer_user=self.reviewer_user)

        for review in recent_reviews:
            if review.id != self.id:
                review._update_validated_from(self)

        # now grab all the negative reviews that happened before the last review request (if any)
        # update the flag to say if the review was an incomplete review cycle

        if last_review_request_time:
            previous_negative_reviews = reviews.filter(
                timestamp__lte=last_review_request_time
            ).filter(Q(status=NOT_YET_COMPETENT) | Q(status=RED_FLAG))
            # breakpoint()

            for review in previous_negative_reviews:
                review._update_incomplete_cycle_from(self)

    def _update_incomplete_cycle_from(self, other):
        """other is a review that happened after self"""

        # sanity checks

        assert self.timestamp < other.timestamp
        assert self.recruit_project == other.recruit_project
        assert self.timestamp <= self.recruit_project.review_request_time
        assert self.status in NEGATIVE_REVIEW_STATUS_CHOICES

        if other.status in POSITIVE_REVIEW_STATUS_CHOICES and other.trusted:
            # the feedback given was sufficient because the next time a review was requested, the card got closed off
            self.complete_review_cycle = True
            self.save()

        if other.status in NEGATIVE_REVIEW_STATUS_CHOICES:
            # the feedback given was insufficient or only partially applied because the next time a review was requested, the card got bounced back
            self.complete_review_cycle = False
            self.save()

    def _update_validated_from(self, other):
        """other is a review that happened after self"""

        if other.reviewer_user == self.reviewer_user:
            # otherwise people can mark their own stuff as complete
            return

        # sanity checks
        assert self.timestamp < other.timestamp
        assert self.recruit_project == other.recruit_project
        if self.recruit_project.review_request_time != None:
            assert self.timestamp > self.recruit_project.review_request_time

        if self.status in POSITIVE_REVIEW_STATUS_CHOICES:
            if other.status in POSITIVE_REVIEW_STATUS_CHOICES:
                if other.trusted:
                    self.validated = RecruitProjectReview.CORRECT
            else:
                assert other.status in NEGATIVE_REVIEW_STATUS_CHOICES
                if other.trusted:
                    self.validated = RecruitProjectReview.INCORRECT
                else:
                    self.validated = RecruitProjectReview.CONTRADICTED

        if self.status in NEGATIVE_REVIEW_STATUS_CHOICES:
            if other.status in POSITIVE_REVIEW_STATUS_CHOICES:
                if other.trusted:
                    self.validated = RecruitProjectReview.INCORRECT
                else:
                    self.validated = RecruitProjectReview.CONTRADICTED

        self.save()


class TopicProgress(
    models.Model, Mixins, ContentItemProxyMixin, ReviewableMixin, FlavourMixin
):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    content_item = models.ForeignKey(ContentItem, on_delete=models.PROTECT)
    due_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    complete_time = models.DateTimeField(blank=True, null=True)
    review_request_time = models.DateTimeField(blank=True, null=True)
    flavours = TaggableManager(blank=True)

    def reviews_queryset(self):
        return self.topic_reviews

    def __str__(self) -> str:
        s = f"{self.content_item} - {self.user}"
        flavours = [o.name for o in self.flavours.all()]
        if flavours:
            return f"{s} [{flavours}]"
        return s

    def get_activity_log_summary_data(self):
        """This is used by the activityLog serializer"""
        try:
            card = self.agile_card
            card_id = card.id
        except AgileCard.DoesNotExist:
            card_id = None
        return {
            "topic_progress": self.id,
            "card": card_id,
            "title": self.content_item.title,
            "flavour_names": self.content_item.flavour_names,
        }

    @property
    def get_total_duration(self):
        return helpers.get_blant_duration(self.id, self.agile_card.status)


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

    def get_activity_log_summary_data(self):
        """This is used by the activityLog serializer"""
        topic = self.topic_progress
        try:
            card = topic.agile_card
            card_id = card.id
        except AgileCard.DoesNotExist:
            card_id = None
        return {
            "topic_progress": topic.id,
            "card": card_id,
            "title": topic.content_item.title,
            "flavour_names": topic.content_item.flavour_names,
        }


class WorkshopAttendance(models.Model, Mixins, ContentItemProxyMixin, FlavourMixin):
    timestamp = models.DateTimeField()
    content_item = models.ForeignKey(ContentItem, on_delete=models.PROTECT)
    attendee_user = models.ForeignKey(User, on_delete=models.PROTECT)
    flavours = TaggableManager(blank=True)


class AgileCard(
    models.Model, Mixins, FlavourMixin, ContentItemProxyMixin, ReviewableMixin
):
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

    __original_status = None

    def get_activity_log_summary_data(self):
        """This is used by the activityLog serializer"""
        return {
            "title": self.content_item.title,
            "flavour_names": self.flavour_names,
        }

    @property
    def progress_instance(self):
        if self.recruit_project_id:
            return self.recruit_project
        if self.topic_progress_id:
            return self.topic_progress
        if self.workshop_attendance_id:
            return self.workshop_attendance

    def __init__(self, *args, **kwargs):
        super(AgileCard, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, *args, **kwargs):
        if self.content_item.project_submission_type == ContentItem.NO_SUBMIT:
            raise ValidationError(
                f"Nosubmit Project cannot be converted to a card. {self.content_item}"
            )
        super(AgileCard, self).save(*args, **kwargs)

        if (
            AgileCard.COMPLETE in [self.status, self.__original_status]
            and self.status != self.__original_status
        ):
            for user in self.assignees.all():
                BurndownSnapshot.create_snapshot(user)

    def status_ready_or_blocked(self):
        """if there was no progress on this card, would the status be READY or BLOCKED?It would be blocked if the prerequisites are not met"""
        from django.db.models import Q

        if self.requires_cards.filter(~Q(status=self.COMPLETE)).count():
            return self.BLOCKED
        return self.READY

    def get_teams(self, assignees_only=False):
        """return the teams of the users involved in this project"""
        user_ids = [user.id for user in self.assignees.all()]
        if not assignees_only:
            user_ids.extend([user.id for user in self.reviewers.all()])
        return Team.get_teams_from_user_ids(user_ids)

    @property
    def repo_url(self):
        if not self.recruit_project:
            return None
        return self.recruit_project.repo_url

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
        return self.recruit_project.link_submission

    def __str__(self):
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

        # we might still be regenerating the card so there might be a matching progress item already

        project = self.find_progress_item()
        if project:
            self.recruit_project = project
            self.status = self.derive_status_from_project(project)
            self.save()
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
        - set up the repo if needed
        """
        from .helpers import create_or_update_single_project_card
        from long_running_request_actors import (
            recruit_project_setup_repository,
            recruit_project_invite_github_collaborators_to_repo,
        )

        assert (
            self.assignees.count() == 1
        ), f"There should be 1 assignee. No more and no less: {self.assignees.all()}"

        self._create_project_progress_if_not_exists()

        if self.content_item.project_submission_type == ContentItem.REPOSITORY:
            # self.recruit_project.create_repo_and_assign_collaborators(
            #     card_flavour_names=self.flavour_names
            # )
            self.recruit_project.setup_repository(add_collaborators=False)
            # assert self.recruit_project.repository
            # retry it just in case of github having eventual consistency issues
            recruit_project_invite_github_collaborators_to_repo.send_with_options(
                kwargs={"project_id": self.recruit_project.id},
            )
            recruit_project_setup_repository.send_with_options(
                kwargs={"project_id": self.recruit_project.id},
                delay=30000,  # 30 seconds
            )

        elif self.content_item.project_submission_type == ContentItem.CONTINUE_REPO:
            self.recruit_project.repository = self._get_repo_to_continue_from()
            recruit_project_invite_github_collaborators_to_repo.send_with_options(
                kwargs={"project_id": self.recruit_project.id},
            )

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

    def find_progress_item(self):
        """return the progress item that matches this card if it exists"""
        content_type = self.content_item.content_type
        user = self.assignees.first()

        if content_type == ContentItem.PROJECT:
            unfiltered_progress = RecruitProject.objects.filter(
                content_item=self.content_item, recruit_users__in=[user]
            )

        elif content_type == ContentItem.TOPIC:
            unfiltered_progress = TopicProgress.objects.filter(
                content_item=self.content_item, user=user
            )
        else:
            raise NotImplemented(
                f"Can't find progress item for content of type {content_type}"
            )
        flavours = sorted([o.name for o in self.flavours.all()])

        filtered_progress = [
            o
            for o in unfiltered_progress
            if sorted([o.name for o in o.flavours.all()]) == flavours
        ]
        if len(filtered_progress) == 1:
            return filtered_progress[0]
        assert (
            len(filtered_progress) == 0
        ), f"Found {len(filtered_progress)} progress items for {self}"

    def _create_topic_progress_if_not_exists(self):
        if self.topic_progress:
            return

        # we might still be regenerating the card so there might be a matching progress item already

        topic = self.find_progress_item()
        if topic:
            self.topic_progress = topic
            self.status = self.derive_status_from_topic(progress=topic, card=self)
            self.save()
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
        assert self.status in [
            AgileCard.IN_PROGRESS,
            AgileCard.REVIEW_FEEDBACK,
        ], f"invalid status: {self.status}"
        assert self.topic_progress != None, f"Topic hasn't been started"
        assert (
            self.content_item.content_type == ContentItem.TOPIC
        ), f"{self.content_item.content_type}"
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

    def stop_project(self):
        assert self.status == AgileCard.IN_PROGRESS
        assert (
            self.content_item.content_type == ContentItem.PROJECT
        ), f"Expected content_type to be 'project', but got {self.content_item.content_type}"
        assert self.recruit_project != None, f"Project hasn't been started"

        self.recruit_project.review_request_time = None
        self.recruit_project.start_time = None
        self.recruit_project.save()

        self.status = self.derive_status_from_project(self.recruit_project)
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
    def open_pr_count(self):
        if not self.recruit_project:
            return None
        return self.recruit_project.open_pr_count

    @property
    def oldest_open_pr_updated_time(self):
        if not self.recruit_project:
            return None
        return self.recruit_project.oldest_open_pr_updated_time

    @property
    def repository(self):
        if not self.recruit_project:
            return None
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

    def add_collaborator(self, user, add_as_project_reviewer):
        from git_real.constants import GIT_REAL_BOT_USERNAME, ORGANISATION
        from git_real.helpers import add_collaborator
        from social_auth.github_api import Api

        if self.recruit_project and self.repository:
            if self.repository.full_name.startswith(ORGANISATION):
                github_name = user.social_profile.github_name
                api = Api(GIT_REAL_BOT_USERNAME)
                add_collaborator(api, self.repository.full_name, github_name)
        self.save()
        if add_as_project_reviewer:
            if user not in self.assignees.all():
                self.reviewers.add(user)
                if self.recruit_project:
                    self.recruit_project.reviewer_users.add(user)
        self.save()

    def get_users_that_reviewed_since_last_review_request(self):
        if self.review_request_time is None:
            return []

        if self.content_item.content_type == ContentItem.PROJECT:
            reviews = RecruitProjectReview.objects.filter(
                recruit_project=self.recruit_project
            )

        elif self.content_item.content_type == ContentItem.TOPIC:
            reviews = TopicReview.objects.filter(topic_progress=self.topic_progress)

        reviews = reviews.filter(timestamp__gte=self.review_request_time)

        return [review.reviewer_user for review in reviews]

    def get_users_that_reviewed_open_prs(self):
        reviews = (
            git_models.PullRequestReview.objects.filter(
                pull_request__repository__recruit_projects__agile_card=self
            )
            .filter(pull_request__state=git_models.PullRequest.OPEN)
            .filter(user__isnull=False)
        )

        return [review.user for review in reviews]

    def request_user_can_start(self, user=None):
        """
        Check if current user can start this card

        This function is only used in template rendering and we are using threadlocals,
        that is why we need to avoid argument parameters unless they're for testing purposes
        """
        from threadlocal_middleware import get_current_user

        user = user or get_current_user()

        if not user:
            return False

        return (self.request_user_is_assignee(user) and self.can_start()) or (
            self.user_has_permission(user, Team.PERMISSION_MANAGE_CARDS)
            and (self.can_start() or self.can_force_start())
        )

    def request_user_is_assignee(self, user):
        """
        Checks if current user is assignee.
        """
        from threadlocal_middleware import get_current_user

        user = user or get_current_user()

        if not user:
            return False

        return self.assignees.first() == user

    def request_user_can_request_review(self, user=None):
        """
        Check if current user can request review for this card
        """
        from threadlocal_middleware import get_current_user

        if self.content_type_nice != "project":
            return False

        if self.status not in [AgileCard.IN_PROGRESS, AgileCard.REVIEW_FEEDBACK]:
            return False

        user = user or get_current_user()

        if not user:
            return False

        return self.request_user_is_assignee(user) or self.user_has_permission(
            user, Team.PERMISSION_MANAGE_CARDS
        )

    def request_user_can_cancel_review_request(self, user=None):
        """
        Check if current user can cancel review request for this card
        """
        from threadlocal_middleware import get_current_user

        if self.content_type_nice != "project":
            return False

        if self.status != AgileCard.IN_REVIEW:
            return False

        user = user or get_current_user()

        if not user:
            return False

        return self.request_user_is_assignee(user) or self.user_has_permission(
            user, Team.PERMISSION_MANAGE_CARDS
        )

    def request_user_can_finish_topic(self, user=None):
        """
        Check if current user can finish topic
        """
        from threadlocal_middleware import get_current_user

        if self.content_type_nice != "topic":
            return False

        if self.status != AgileCard.IN_PROGRESS:
            return False

        user = user or get_current_user()

        if not user:
            return False

        return self.request_user_is_assignee(user) or self.user_has_permission(
            user, Team.PERMISSION_MANAGE_CARDS
        )

    def request_user_can_stop_card(self, user=None):
        """
        Check if current user can stop card
        """
        from threadlocal_middleware import get_current_user

        if self.status != AgileCard.IN_PROGRESS:
            return False

        user = user or get_current_user()

        if not user:
            return False

        return self.request_user_is_assignee(user) or self.user_has_permission(
            user, Team.PERMISSION_MANAGE_CARDS
        )

    def user_has_permission(self, user, permissions):
        return any((user.has_perm(permissions, team) for team in self.get_teams()))

    def request_user_is_trusted(self, user=None):
        """
        Check if current user is trusted on a card
        """
        from threadlocal_middleware import get_current_user

        user = user or get_current_user()

        if not user:
            return False

        all_trusts = (
            ReviewTrust.objects.filter(content_item=self.content_item)
            .filter(user=user)
            .prefetch_related("user")
        )

        all_trusts = [t for t in all_trusts if t.flavours_match(self.flavour_names)]

        return len(all_trusts) > 0


class BurndownSnapshot(models.Model):
    MIN_HOURS_BETWEEN_SNAPSHOTS = 4
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    cards_total_count = models.SmallIntegerField()
    project_cards_total_count = models.SmallIntegerField()
    cards_in_complete_column_total_count = models.SmallIntegerField()
    project_cards_in_complete_column_total_count = models.SmallIntegerField()

    @classmethod
    def create_snapshot(Cls, user):
        match = Cls.objects.filter(
            user=user,
            timestamp__gte=timezone.now()
            - timedelta(hours=Cls.MIN_HOURS_BETWEEN_SNAPSHOTS),
        ).first()

        cards = AgileCard.objects.filter(assignees=user)
        project_cards = cards.filter(content_item__content_type=ContentItem.PROJECT)

        complete_cards = cards.filter(status=AgileCard.COMPLETE)
        complete_project_cards = project_cards.filter(status=AgileCard.COMPLETE)

        snapshot_values = {
            "cards_total_count": cards.count(),
            "project_cards_total_count": project_cards.count(),
            "cards_in_complete_column_total_count": complete_cards.count(),
            "project_cards_in_complete_column_total_count": complete_project_cards.count(),
        }

        if match:
            # there was a snapshot taken recently, it will be updated
            return Cls.objects.filter(pk=match.id).update(**snapshot_values)

        return Cls.objects.create(user=user, **snapshot_values)


class ContentItemAgileWeight(models.Model, FlavourMixin, ContentItemProxyMixin):
    content_item = models.ForeignKey(
        ContentItem, on_delete=models.PROTECT, related_name="agile_weights"
    )
    flavours = TaggableManager(blank=True)
    weight = models.IntegerField()
