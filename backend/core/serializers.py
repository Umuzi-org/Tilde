from . import models
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.conf import settings

from dj_rest_auth.serializers import (
    PasswordResetSerializer as PasswordResetSerializerBase,
)
from django.contrib.auth import (
     get_user_model,
)
from django.contrib.auth.forms import PasswordResetForm,_unicode_ci_compare

User = get_user_model()

class _PasswordResetForm(PasswordResetForm):

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = User.get_email_field_name()
        active_users = User._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and
            _unicode_ci_compare(email, getattr(u, email_field_name))
        )

class PasswordResetSerializer(PasswordResetSerializerBase):
    def get_email_options(self):

        return {"domain_override": settings.FRONTEND_URL}

    @property
    def password_reset_form_class(self):
        return _PasswordResetForm

    def save(self):
        from django.contrib.auth.tokens import default_token_generator

        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        # Default templates at:
        # https://github.com/mozilla/captain/blob/master/vendor/lib/python/django/contrib/admin/templates/registration/password_reset_email.html
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'token_generator': default_token_generator,
            'html_email_template_name': 'core/emails/password_reset.html',
            'email_template_name': 'core/emails/password_reset.txt'
        }
        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


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

    def get_permissions(self, instance: Token):
        return instance.user.get_permissions()

    # def get_teams(self, instance):
    #     return instance.user.teams

    # def get_is_student(self, instance):
    #     return int(instance.user.is_student)


class UserErrorSerialiser(serializers.Serializer):
    class Meta:
        fields = ["message"]

    message = serializers.CharField()


class BulkSetDueTimeSerializer(serializers.Serializer):
    class Meta:
        fields = [
            "due_time"
            "flavours",
            "content_item"
        ]

    due_time = serializers.DateTimeField()
    flavours = serializers.ListField(child=serializers.IntegerField())
    content_item = serializers.IntegerField()


class StreamRegistrationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.StreamRegistration
        fields = [
            'id',
            'name',
            'user',
            'stream'
        ]

    user = serializers.SerializerMethodField("get_user_name")
    stream = serializers.SerializerMethodField("get_stream_name")

    def get_user_name(self, instance):
        return instance.user.email

    def get_stream_name(self, instance):
        return instance.stream.name