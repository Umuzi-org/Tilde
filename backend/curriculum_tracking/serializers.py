from django.forms import CharField
from git_real.models import PullRequest, PullRequestReview
from . import models
from rest_framework import serializers
from django.db.models import Q
from core import models as core_models
from datetime import timedelta
from django.utils import timezone
from config.models import NameSpace
from taggit.models import Tag
from git_real import models as git_models


class RecruitProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProject
        fields = [
            "id",
            "content_item",
            "due_time",
            "complete_time",
            "repository",
            "project_reviews",
            "title",
            "content_url",
            "tag_names",
            "recruit_users",
            "recruit_user_names",
            "reviewer_users",
            "reviewer_user_names",
            "agile_card",
            "agile_card_status",
            "submission_type_nice",
            "link_submission",
            # "deadline_status",
            # "latest_project_review_status",
            # "latest_project_review_timestamp",
            # "latest_project_review_comments",
            # "latest_project_reviewer_email",
        ]


class TopicProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TopicProgress
        fields = [
            "id",
            "user",
            "content_item",
            "due_time",
            "start_time",
            "complete_time",
            "review_request_time",
            "topic_reviews",
            "topic_needs_review",
            "flavours",
        ]

    flavours = serializers.CharField(help_text="comma separated list of flavours")


class PullRequestReviewQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = git_models.PullRequestReview
        fields = [
            "id",
            "state",
            "submitted_at",
            "flavour_names",
            "content_item",
            "title",
            "content_item_agile_weight",
            "agile_card",
            "user",
            "validated",
        ]

    agile_card = serializers.SerializerMethodField("get_agile_card")
    flavour_names = serializers.SerializerMethodField("get_flavour_names")
    content_item = serializers.SerializerMethodField("get_content_item")
    title = serializers.SerializerMethodField("get_title")
    content_item_agile_weight = serializers.SerializerMethodField(
        "get_content_item_agile_weight"
    )

    def get_project(self, instance):
        return instance.pull_request.repository.recruit_projects.order_by("id").last()

    def get_agile_card(self, instance):
        project = self.get_project(instance)
        try:
            card = project.agile_card
        except models.AgileCard.DoesNotExist:
            return None

        return card.id

    def get_flavour_names(self, instance):
        return self.get_project(instance).flavour_names

    def get_title(self, instance):
        return self.get_project(instance).content_item.title

    def get_content_item(self, instance):
        return self.get_project(instance).content_item.id

    def get_content_item_agile_weight(self, instance):
        project = instance.pull_request.repository.recruit_projects.order_by(
            "id"
        ).last()
        weights = project.content_item.agile_weights.all()
        flavour_names = project.flavour_names
        for weight in weights:
            if weight.flavours_match(flavour_names):
                return weight.weight


class RecruitProjectReviewQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProjectReview
        fields = [
            "id",
            "flavour_names",
            "content_item",
            "title",
            "trusted",
            "validated",
            "agile_card",
            "status",
            "timestamp",
            "reviewer_user",
            "content_item_agile_weight",
            "complete_review_cycle",
        ]

    agile_card = serializers.SerializerMethodField("get_agile_card")
    flavour_names = serializers.SerializerMethodField("get_flavour_names")
    content_item = serializers.SerializerMethodField("get_content_item")
    title = serializers.SerializerMethodField("get_title")
    content_item_agile_weight = serializers.SerializerMethodField(
        "get_content_item_agile_weight"
    )

    def get_flavour_names(self, instance):
        return instance.recruit_project.flavour_names

    def get_content_item(self, instance):
        return instance.recruit_project.content_item.id

    def get_agile_card(self, instance):
        try:
            return instance.recruit_project.agile_card.id
        except models.AgileCard.DoesNotExist:
            return

    def get_title(self, instance):
        return instance.recruit_project.content_item.title

    def get_content_item_agile_weight(self, instance):
        weights = instance.recruit_project.content_item.agile_weights.all()
        flavour_names = instance.recruit_project.flavour_names
        for weight in weights:
            if weight.flavours_match(flavour_names):
                return weight.weight


class RecruitProjectReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProjectReview
        fields = [
            "id",
            "status",
            "timestamp",
            "comments",
            "recruit_project",
            "reviewer_user",
            "reviewer_user_email",
            # the below fields are not used when navigting a user's board.
            # there should probably be 2 seperate serialisers for the different displays
            "title",
            "reviewed_user_emails",
            "reviewed_user_ids",
            "trusted",
            "validated",
            "agile_card",
        ]

    agile_card = serializers.SerializerMethodField("get_agile_card")
    title = serializers.SerializerMethodField("get_title")
    reviewed_user_emails = serializers.SerializerMethodField("get_reviewed_user_emails")
    reviewed_user_ids = serializers.SerializerMethodField("get_reviewed_user_ids")

    def get_agile_card(self, instance):
        try:
            return instance.recruit_project.agile_card.id
        except models.AgileCard.DoesNotExist:
            return

    def get_title(self, instance):
        return instance.recruit_project.content_item.title

    def get_reviewed_user_emails(self, instance):
        return [o.email for o in instance.recruit_project.recruit_users.all()]

    def get_reviewed_user_ids(self, instance):
        return [o.id for o in instance.recruit_project.recruit_users.all()]


class TopicReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TopicReview
        fields = [
            "id",
            "status",
            "timestamp",
            "comments",
            "topic_progress",
            "reviewer_user",
            "reviewer_user_email",
        ]


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContentItem
        fields = [
            "id",
            "content_type",
            "content_type_nice",
            "title",
            "slug",
            "url",
            "tag_names",
            "post_ordered_content",
            "pre_ordered_content",
            "flavour_names",
            "topic_needs_review",
            "project_submission_type_nice",
            "continue_from_repo",
            "template_repo",
        ]


class ContentItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContentItemOrder
        fields = ["id", "pre", "post", "hard_requirement", "pre_title", "post_title"]


class AgileCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgileCard
        fields = [
            "id",
            "content_item",
            "content_item_url",
            "status",
            "recruit_project",
            "assignees",
            "reviewers",
            "assignee_names",
            "reviewer_names",
            "is_hard_milestone",
            "is_soft_milestone",
            "title",
            "content_type",
            "content_type_nice",
            "tag_names",
            "order",
            "code_review_competent_since_last_review_request",
            "code_review_excellent_since_last_review_request",
            "code_review_red_flag_since_last_review_request",
            "code_review_ny_competent_since_last_review_request",
            "requires_cards",
            "required_by_cards",
            "flavour_names",
            "project_submission_type_nice",
            "project_link_submission",
            "topic_needs_review",
            "topic_progress",
            "due_time",
            "complete_time",
            "review_request_time",
            "start_time",
            "can_start",
            "can_force_start",
            "open_pr_count",
            "oldest_open_pr_updated_time",
            "repo_url",
            "users_that_reviewed_since_last_review_request",
            "users_that_reviewed_since_last_review_request_emails",
            "users_that_reviewed_open_prs",
            "users_that_reviewed_open_prs_emails",
        ]

    users_that_reviewed_since_last_review_request = serializers.SerializerMethodField(
        "get_users_that_reviewed_since_last_review_request"
    )

    users_that_reviewed_since_last_review_request_emails = (
        serializers.SerializerMethodField(
            "get_users_that_reviewed_since_last_review_request_emails"
        )
    )

    users_that_reviewed_open_prs = serializers.SerializerMethodField(
        "get_users_that_reviewed_open_prs"
    )
    users_that_reviewed_open_prs_emails = serializers.SerializerMethodField(
        "get_users_that_reviewed_open_prs_emails"
    )

    def get_users_that_reviewed_since_last_review_request_emails(self, instance):
        return [
            o.email
            for o in instance.get_users_that_reviewed_since_last_review_request()
        ]

    def get_users_that_reviewed_since_last_review_request(self, instance):
        return [
            o.id for o in instance.get_users_that_reviewed_since_last_review_request()
        ]

    def get_users_that_reviewed_open_prs(self, instance):
        return [o.id for o in instance.get_users_that_reviewed_open_prs()]

    def get_users_that_reviewed_open_prs_emails(self, instance):
        return [o.email for o in instance.get_users_that_reviewed_open_prs()]


class CardSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgileCard
        fields = [
            "id",
            "order",
            "content_item",
            "content_item_url",
            "title",
            "status",
            # "nice_status",
            # "project_due_time",
            "recruit_project",
            # "project_review_request_time",
            "due_time",
            "complete_time",
            "review_request_time",
            "start_time",
            "assignees",
            "assignee_names",
            "code_review_competent_since_last_review_request",
            "code_review_excellent_since_last_review_request",
            "code_review_red_flag_since_last_review_request",
            "code_review_ny_competent_since_last_review_request",
            "open_pr_count",
            "oldest_open_pr_updated_time",
            "repo_url",
        ]


class NewReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProjectReview
        fields = ["status", "comments"]


class WorkshopAttendanceTime(serializers.ModelSerializer):
    class Meta:
        model = models.WorkshopAttendance
        fields = ["timestamp"]


class SetDueTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProject
        fields = ["due_time"]


class AddReviewerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgileCard
        fields = ["reviewers"]


class TeamField(serializers.RelatedField):
    queryset = core_models.Team.objects.filter(active=True).order_by("name")

    def to_representation(self, value):
        return value.id


class UserField(serializers.RelatedField):
    queryset = core_models.User.objects.filter(active=True).order_by("email")

    def to_representation(self, value):
        return value.id


class ProjectContentItemField(serializers.RelatedField):
    queryset = (
        models.ContentItem.objects.filter(content_type=models.ContentItem.PROJECT)
        .filter(~Q(project_submission_type=models.ContentItem.NO_SUBMIT))
        .order_by("title")
    )

    def to_representation(self, value):
        return value.id


class GroupSelfReviewSerialiser(serializers.Serializer):
    class Meta:
        fields = ["group", "content_item", "flavours"]

    content_item = ProjectContentItemField()
    flavours = serializers.CharField(help_text="comma seperated list of flavours")
    group = TeamField()


class TeamReviewByOtherSerialiser(serializers.Serializer):
    class Meta:
        fields = ["group", "content_item", "reviewer_group", "flavours"]

    content_item = ProjectContentItemField()
    flavours = serializers.CharField(help_text="comma seperated list of flavours")
    group = TeamField()
    reviewer_group = TeamField()


class TeamReviewByUserSerialiser(serializers.Serializer):
    class Meta:
        fields = [
            "group",
            "content_item",
            "reviewer_user",
            "flavours",
            "assign_to_cards",
        ]

    assign_to_cards = serializers.BooleanField(
        default=True,
        help_text="if this is false then the user is only assigned to the github repos. If it is True then the user is listed as a reviewer on the agile cards",
    )

    content_item = ProjectContentItemField()
    flavours = serializers.CharField(help_text="comma seperated list of flavours")
    group = TeamField()
    reviewer_user = serializers.EmailField()


class ProjectSubmitLink(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProject
        fields = ["link_submission"]

    # TODO: validators based on model validators (look inside save method)


class WorkshopAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkshopAttendance
        fields = ["id", "timestamp", "content_item", "attendee_user"]


class UserDetailedStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "cards_assigned_with_status_complete",
            "cards_assigned_with_status_in_review",
            "cards_assigned_with_status_review_feedback",
            "cards_assigned_with_status_in_progress",
            "cards_assigned_with_status_blocked",
            "cards_assigned_with_status_ready",
            "cards_completed_last_7_days_as_assignee",
            "cards_started_last_7_days_as_assignee",
            "total_tilde_reviews_done",
            "tilde_reviews_done_last_7_days",
            "total_pr_reviews_done",
            "pr_reviews_done_last_7_days",
            "tilde_cards_reviewed_in_last_7_days",
            # "tilde_review_disagreements_in_last_7_days",
        ]

    cards_assigned_with_status_complete = serializers.SerializerMethodField(
        "get_cards_assigned_with_status_complete"
    )
    cards_assigned_with_status_in_review = serializers.SerializerMethodField(
        "get_cards_assigned_with_status_in_review"
    )
    cards_assigned_with_status_review_feedback = serializers.SerializerMethodField(
        "get_cards_assigned_with_status_review_feedback"
    )
    cards_assigned_with_status_in_progress = serializers.SerializerMethodField(
        "get_cards_assigned_with_status_in_progress"
    )

    cards_assigned_with_status_blocked = serializers.SerializerMethodField(
        "get_cards_assigned_with_status_blocked"
    )

    cards_assigned_with_status_ready = serializers.SerializerMethodField(
        "get_cards_assigned_with_status_ready"
    )

    cards_completed_last_7_days_as_assignee = serializers.SerializerMethodField(
        "get_cards_completed_last_7_days_as_assignee"
    )
    cards_started_last_7_days_as_assignee = serializers.SerializerMethodField(
        "get_cards_started_last_7_days_as_assignee"
    )
    total_tilde_reviews_done = serializers.SerializerMethodField(
        "get_total_tilde_reviews_done"
    )
    tilde_reviews_done_last_7_days = serializers.SerializerMethodField(
        "get_tilde_reviews_done_last_7_days"
    )
    tilde_cards_reviewed_in_last_7_days = serializers.SerializerMethodField(
        "get_tilde_cards_reviewed_in_last_7_days"
    )

    # tilde_review_disagreements_in_last_7_days = serializers.SerializerMethodField(
    #     "get_tilde_review_disagreements_in_last_7_days"
    # )

    total_pr_reviews_done = serializers.SerializerMethodField(
        "get_total_pr_reviews_done"
    )
    pr_reviews_done_last_7_days = serializers.SerializerMethodField(
        "get_pr_reviews_done_last_7_days"
    )

    def get_cards_assigned_with_status_complete(self, user):

        cards_assigned_with_status_complete_amount = models.AgileCard.objects.filter(
            status=models.AgileCard.COMPLETE, assignees=user.id
        ).count()

        return cards_assigned_with_status_complete_amount

    def get_cards_assigned_with_status_in_review(self, user):

        cards_assigned_with_status_in_review_amount = models.AgileCard.objects.filter(
            status=models.AgileCard.IN_REVIEW, assignees=user.id
        ).count()

        return cards_assigned_with_status_in_review_amount

    def get_cards_assigned_with_status_review_feedback(self, user):
        cards_assigned_with_status_review_feedback_amount = (
            models.AgileCard.objects.filter(
                status=models.AgileCard.REVIEW_FEEDBACK, assignees=user.id
            ).count()
        )

        return cards_assigned_with_status_review_feedback_amount

    def get_cards_assigned_with_status_in_progress(self, user):

        cards_assigned_with_status_in_progress = models.AgileCard.objects.filter(
            status=models.AgileCard.IN_PROGRESS, assignees=user.id
        ).count()

        return cards_assigned_with_status_in_progress

    def get_cards_assigned_with_status_blocked(self, user):

        cards_assigned_with_status_blocked = models.AgileCard.objects.filter(
            status=models.AgileCard.BLOCKED, assignees=user.id
        ).count()

        return cards_assigned_with_status_blocked

    def get_cards_assigned_with_status_ready(self, user):

        cards_currently_ready_as_assignee = models.AgileCard.objects.filter(
            status=models.AgileCard.READY, assignees=user.id
        ).count()

        return cards_currently_ready_as_assignee

    def get_cards_completed_last_7_days_as_assignee(self, user):
        cards_completed_past_seven_days = models.AgileCard.objects.filter(
            status=models.AgileCard.COMPLETE,
            assignees=user.id,
            recruit_project__complete_time__gte=timezone.now() - timedelta(days=7),
        ).count()

        return cards_completed_past_seven_days

    def get_cards_started_last_7_days_as_assignee(self, user):
        cards_started_past_seven_days = models.AgileCard.objects.filter(
            assignees=user.id,
            recruit_project__start_time__gte=timezone.now() - timedelta(days=7),
        ).count()

        return cards_started_past_seven_days

    def get_total_tilde_reviews_done(self, user):
        project_reviews_done_to_date = models.RecruitProjectReview.objects.filter(
            reviewer_user_id=user.id
        ).count()

        topic_reviews_done_to_date = models.TopicReview.objects.filter(
            reviewer_user_id=user.id
        ).count()

        return project_reviews_done_to_date + topic_reviews_done_to_date

    def get_tilde_cards_reviewed_in_last_7_days(self, user):

        tilde_project_reviews_done_in_past_seven_days = (
            models.RecruitProjectReview.objects.filter(
                reviewer_user_id=user.id,
                timestamp__gte=timezone.now() - timedelta(days=7),
            )
        )

        tilde_topic_reviews_done_in_past_seven_days = models.TopicReview.objects.filter(
            reviewer_user_id=user.id, timestamp__gte=timezone.now() - timedelta(days=7)
        )

        return (
            models.AgileCard.objects.filter(
                Q(
                    recruit_project__project_reviews__in=tilde_project_reviews_done_in_past_seven_days
                )
                | Q(
                    topic_progress__topic_reviews__in=tilde_topic_reviews_done_in_past_seven_days
                )
            )
            .distinct()
            .count()
        )

    def get_tilde_reviews_done_last_7_days(self, user):
        project_reviews_done_last_7_days = models.RecruitProjectReview.objects.filter(
            reviewer_user_id=user.id, timestamp__gte=timezone.now() - timedelta(days=7)
        ).count()

        topic_reviews_done_last_7_days = models.TopicReview.objects.filter(
            reviewer_user_id=user.id, timestamp__gte=timezone.now() - timedelta(days=7)
        ).count()

        return project_reviews_done_last_7_days + topic_reviews_done_last_7_days

    def get_total_pr_reviews_done(self, user):
        pr_reviews_done_to_date = PullRequestReview.objects.filter(user=user).count()

        return pr_reviews_done_to_date

    def get_pr_reviews_done_last_7_days(self, user):
        pr_reviews_done_past_seven_days = PullRequestReview.objects.filter(
            user=user, submitted_at__gte=timezone.now() - timedelta(days=7)
        ).count()

        return pr_reviews_done_past_seven_days


class TeamStatsSerializer(serializers.ModelSerializer):
    CONFIGURATION_NAMESPACE = "curriculum_tracking/serializers/TeamStatsSerializer"

    class Meta:
        model = core_models.Team
        fields = [
            "id",
            "name",  # TODO: remove this field once api accessable via gui
            "oldest_open_pr_time",
            "total_open_prs",
            "oldest_card_in_review_time",
            "total_cards_in_review",
        ]

    oldest_open_pr_time = serializers.SerializerMethodField("get_oldest_open_pr_time")
    total_open_prs = serializers.SerializerMethodField("get_total_open_prs")
    oldest_card_in_review_time = serializers.SerializerMethodField(
        "get_oldest_card_in_review_time"
    )
    total_cards_in_review = serializers.SerializerMethodField(
        "get_total_cards_in_review"
    )

    def _get_config_EXCLUDE_TAGS_FROM_REVIEW_STATS(self):
        config = NameSpace.get_config(self.CONFIGURATION_NAMESPACE)
        tag_names = config.EXCLUDE_TAGS_FROM_REVIEW_STATS
        return [
            instance
            for instance, _ in [
                Tag.objects.get_or_create(name=name) for name in tag_names
            ]
        ]

    def _get_open_prs(self, instance):
        users = instance.user_set.filter(active=True)
        return PullRequest.objects.filter(state=PullRequest.OPEN).filter(
            repository__recruit_projects__agile_card__assignees__in=users
        )

    def _get_review_agile_cards(self, instance):
        skip_tags = self._get_config_EXCLUDE_TAGS_FROM_REVIEW_STATS()

        users = instance.user_set.filter(active=True)
        result = models.AgileCard.objects.filter(
            status=models.AgileCard.IN_REVIEW
        ).filter(assignees__in=users)
        return result.filter(~Q(content_item__tags__in=skip_tags))

    def get_oldest_open_pr_time(self, instance):
        pr = self._get_open_prs(instance).order_by("created_at").first()
        if pr is not None:
            return pr.created_at

    def get_total_open_prs(self, instance):
        return self._get_open_prs(instance).count()

    def get_oldest_card_in_review_time(self, instance):
        card = (
            self._get_review_agile_cards(instance)
            .order_by("recruit_project__review_request_time")
            .first()
        )
        if card is not None:
            if card.recruit_project is not None:
                return card.recruit_project.review_request_time
            if card.topic_progress is not None:
                return card.topic_progress.review_request_time
            raise Exception(
                f"card has no progress id:\n\tcard id: {card.id}\n\tcard: {card}"
            )

    def get_total_cards_in_review(self, instance):
        return self._get_review_agile_cards(instance).count()


class BurnDownSnapShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BurndownSnapshot
        fields = [
            "id",
            "user",
            "timestamp",
            "cards_total_count",
            "project_cards_total_count",
            "cards_in_complete_column_total_count",
            "project_cards_in_complete_column_total_count",
        ]


class ReviewTrustSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewTrust
        fields = ["id", "content_item", "content_item_title", "flavour_names", "user"]

    content_item_title = serializers.SerializerMethodField("get_content_item_title")

    def get_content_item_title(self, review_trust: object):
        return review_trust.content_item.title


class BulkSetDueDatesHumanFriendly(serializers.Serializer):
    class Meta:
        fields = [
            "due_time",
            "flavour_names",
            "content_item_title",
            "team_name",
            "email",
        ]

    due_time = serializers.DateTimeField()
    flavour_names = serializers.ListField(child=serializers.CharField(), required=False)
    content_item_title = serializers.CharField()
    team_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)


class RegisterNewLearnerSerializer(serializers.Serializer):
    class Meta:
        fields = [
            "email",
            "first_name",
            "last_name",
            "github_name",
            "stream_name",
            "team_name",
        ]

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    github_name = serializers.CharField(required=False)
    stream_name = serializers.CharField(required=True)
    team_name = serializers.CharField(required=True)


from rest_framework.exceptions import ValidationError


class ContentItemAgileWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContentItemAgileWeight
        fields = ["id", "flavour_names", "weight", "content_item"]

    flavour_names = serializers.ListField(CharField)

    def save(self, **kwargs):
        content_item = self.validated_data["content_item"]
        available_flavours = content_item.flavour_names
        flavour_names = self.initial_data.getlist("flavour_names")
        for flavour in flavour_names:
            if flavour not in available_flavours:
                raise ValidationError(
                    f"flavour '{flavour}' not allowed. Choose from {available_flavours}"
                )
        instance = super(ContentItemAgileWeightSerializer, self).save()
        instance.set_flavours(flavour_names)
        return instance


class CurriculumContentRequirementSerializer(serializers.ModelSerializer):

    curriculum_name = serializers.CharField(read_only=True)
    content_item_title = serializers.CharField(read_only=True)

    class Meta:
        model = models.CurriculumContentRequirement
        fields = [
            "id",
            "curriculum",
            "curriculum_name",
            "content_item",
            "content_item_title",
        ]

    curriculum_name = serializers.SerializerMethodField("get_curriculum_name")
    content_item_title = serializers.SerializerMethodField("get_content_item_title")

    def get_curriculum_name(self, instance):
        return instance.curriculum.name

    def get_content_item_title(self, instance):
        return instance.content_item.title


class CourseRegistrationSerialiser(serializers.ModelSerializer):

    user_email = serializers.CharField(read_only=True)
    curriculum_name = serializers.CharField(read_only=True)

    class Meta:
        model = models.CourseRegistration
        fields = ["id", "user", "curriculum", "user_email", "curriculum_name"]

    user_email = serializers.SerializerMethodField("get_user_email")

    curriculum_name = serializers.SerializerMethodField("get_curriculum_name")

    def get_user_email(self, instance):
        return instance.user.email

    def get_curriculum_name(self, instance):
        return instance.curriculum.name


class ProjectReviewQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProject
        fields = [
            "id",
            "agile_card",
            "status",
            "content_item_title",
            "review_request_time",
            "start_time",
            "due_time",
            "flavour_names",
            "tag_names",
            "code_review_competent_since_last_review_request",
            "code_review_excellent_since_last_review_request",
            "code_review_red_flag_since_last_review_request",
            "code_review_ny_competent_since_last_review_request",
            "open_pr_count",
            "oldest_open_pr_updated_time",
            "repo_url",
            "recruit_users",
            "reviewer_users",
            "recruit_user_emails",
            "reviewer_user_emails",
            "users_that_reviewed_since_last_review_request",
            "users_that_reviewed_since_last_review_request_emails",
        ]

    content_item_title = serializers.SerializerMethodField("get_content_item_title")

    recruit_user_emails = serializers.SerializerMethodField("get_recruit_user_emails")

    reviewer_user_emails = serializers.SerializerMethodField("get_reviewer_user_emails")

    users_that_reviewed_since_last_review_request_emails = (
        serializers.SerializerMethodField(
            "get_users_that_reviewed_since_last_review_request_emails"
        )
    )

    users_that_reviewed_since_last_review_request = serializers.SerializerMethodField(
        "get_users_that_reviewed_since_last_review_request"
    )

    status = serializers.SerializerMethodField("get_status")

    def get_users_that_reviewed_since_last_review_request_emails(self, instance):
        return [
            o.email for o in instance.users_that_reviewed_since_last_review_request()
        ]

    def get_users_that_reviewed_since_last_review_request(self, instance):
        return [o.id for o in instance.users_that_reviewed_since_last_review_request()]

    def get_content_item_title(self, instance):
        return instance.content_item.title

    def get_recruit_user_emails(self, instance):
        return [o.email for o in instance.recruit_users.all()]

    def get_reviewer_user_emails(self, instance):
        return [o.email for o in instance.reviewer_users.all()]

    def get_status(self, instance):
        try:
            return instance.agile_card.status
        except models.AgileCard.DoesNotExist:
            return None


class OutstandingCompetenceReviewSerializer(serializers.ModelSerializer):
    """This is use for showing which cards a user needs to review."""

    class Meta:
        model = models.AgileCard
        fields = [
            "id",
            "title",
            "assignees",
            "assignee_names",
            "reviewer_names",
            "reviewers",
            "tag_names",
            "flavour_names",
            "review_request_time",
        ]
