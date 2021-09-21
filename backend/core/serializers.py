# from rest_framework.decorators import permission_classes
from . import models
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "preferred_name",
            "team_memberships",
            "is_active",
            "is_staff",
            "is_superuser",
            "github_name",
        ]

    team_memberships = serializers.SerializerMethodField("get_team_memberships")

    def get_team_memberships(self, instance):

        return {
            team.id: {"id": team.id, "name": team.name} for team in instance.teams()
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ["id", "user"]


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Curriculum
        fields = [
            "id",
            "name",
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = [
            "id",
            "name",
            # "kind",
            "active",
            "members",
        ]


class WhoAmISerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            "email",
            "token",
            # "id",
            "user_id",
            "active",
            "first_name",
            "last_name",
            "preferred_name",
            "is_staff",
            "is_superuser",
            "permissions",
            # "teams",
        ]

    preferred_name = serializers.SerializerMethodField("get_preferred_name")
    email = serializers.SerializerMethodField("get_email")
    token = serializers.SerializerMethodField("get_token")
    active = serializers.SerializerMethodField("get_active")
    first_name = serializers.SerializerMethodField("get_first_name")
    last_name = serializers.SerializerMethodField("get_last_name")
    is_staff = serializers.SerializerMethodField("get_is_staff")
    is_superuser = serializers.SerializerMethodField("get_is_superuser")
    permissions = serializers.SerializerMethodField("get_permissions")
    # teams = serializers.SerializerMethodField("get_teams")
    # is_student = serializers.SerializerMethodField("get_is_student")

    def get_role(self, instance):
        roles = list(models.UserRole.objects.filter(user=instance.user).all())
        assert len(roles) in [0, 1], "too many roles for user"
        if roles:
            return roles[0]

    def get_token(self, instance):
        return instance.key

    def get_email(self, instance):
        return instance.user.email

    def get_active(self, instance):
        return instance.user.active

    def get_first_name(self, instance):
        return instance.user.first_name

    def get_last_name(self, instance):
        return instance.user.last_name

    def get_preferred_name(self, instance):
        return instance.user.preferred_name

    def get_is_staff(self, instance):
        return int(instance.user.is_staff)

    def get_is_superuser(self, instance):
        return int(instance.user.is_superuser)

    def get_permissions(self, instance):
        return instance.user.get_permissions()

    # def get_teams(self, instance):
    #     return instance.user.teams

    # def get_is_student(self, instance):
    #     return int(instance.user.is_student)


class UserErrorSerialiser(serializers.Serializer):
    class Meta:
        fields = ["message"]

    message = serializers.CharField()


class UserStatsSerializer(serializers.Serializer):
    class Meta:
        fields = []

"""
class UserStatsPerWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "cards_in_completed_column",
            "cards_in_review_column",
            "cards_in_review_feedback_column",
            "cards_in_progress_column",
            "cards_completed_last_7_days",
            "cards_started_last_7_days",
            "total_number_of_tilde_reviews",
            "tilde_reviews_done_last_7_days",
            "total_number_of_pr_reviews",
            "pr_reviews_done_last_7_days",
        ]

    cards_in_completed_column = serializers.SerializerMethodField("get_cards_in_completed_column")
    cards_in_review_column = serializers.SerializerMethodField("get_cards_in_review_column")
    cards_in_review_feedback_column = serializers.SerializerMethodField("get_cards_in_review_feedback_column")
    cards_in_progress_column = serializers.SerializerMethodField("get_cards_in_progress_column")
    cards_completed_last_7_days = serializers.SerializerMethodField("get_cards_completed_last_7_days")
    cards_started_last_7_days = serializers.SerializerMethodField("get_cards_started_last_7_days")
    total_number_of_tilde_reviews = serializers.SerializerMethodField("get_total_number_of_tilde_reviews")
    tilde_reviews_done_last_7_days = serializers.SerializerMethodField("get_tilde_reviews_done_last_7_days")
    total_number_of_pr_reviews = serializers.SerializerMethodField("get_total_number_of_pr_reviews")
    pr_reviews_done_last_7_days = serializers.SerializerMethodField("get_pr_reviews_done_last_7_days")

    def get_cards_in_completed_column(self, instance):
        return instance.user_cards_in_completed_column

    def get_cards_in_review_column(self, instance):
        return instance.user_cards_in_review_column

    def get_cards_in_review_feedback_column(self, instance):
        return instance.user_cards_in_review_feedback_column

    def get_cards_in_progress_column(self, instance):
        return instance.user_cards_in_progress_column

    def get_cards_completed_last_7_days(self, instance):
        return instance.user_cards_completed_in_past_seven_days

    def get_cards_started_last_7_days(self, instance):
        return instance.user_cards_started_in_past_seven_days

    def get_total_number_of_tilde_reviews(self, instance):
        return instance.total_tilde_reviews_done_to_date

    def get_tilde_reviews_done_last_7_days(self, instance):
        return instance.tilde_reviews_done_in_past_seven_days

    def get_total_number_of_pr_reviews(self, instance):
        return instance.total_pr_reviews_done_to_date

    def get_pr_reviews_done_last_7_days(self, instance):
        return instance.pr_reviews_done_in_past_seven_days
"""