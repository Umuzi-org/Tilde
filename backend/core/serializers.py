from . import models
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["email", "first_name", "last_name"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ["id", "user"]


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Curriculum
        fields = ["id"]


class EmployerPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmployerPartner
        fields = ["id"]


class RecruitCohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitCohort
        fields = [
            "id",
            "user",
            "cohort",
            "employer_partner",
            "start_date",
            "end_date",
            # "email",
        ]


class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cohort
        fields = [
            "id",
            "start_date",
            "end_date",
            "cohort_number",
            "cohort_curriculum",
            "curriculum_short_name",
            "curriculum_name",
            "label",
            "cohort_recruit_users",
            "cohort_recruit_user_emails",
            "active",
        ]


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
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
            "user_id",
            "active",
            "first_name",
            "last_name",
            "preferred_name",
            "is_staff",
            "is_superuser",
            "is_student",
        ]

    preferred_name = serializers.SerializerMethodField("get_preferred_name")
    email = serializers.SerializerMethodField("get_email")
    token = serializers.SerializerMethodField("get_token")
    active = serializers.SerializerMethodField("get_active")
    first_name = serializers.SerializerMethodField("get_first_name")
    last_name = serializers.SerializerMethodField("get_last_name")
    is_staff = serializers.SerializerMethodField("get_is_staff")
    is_superuser = serializers.SerializerMethodField("get_is_superuser")
    is_student = serializers.SerializerMethodField("get_is_student")

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

    def get_is_student(self, instance):
        return int(instance.user.is_student)


class UserErrorSerialiser(serializers.Serializer):
    class Meta:
        fields = ["message"]

    message = serializers.CharField()

