from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.core.mail import send_mail
# import secrets
# import re

# from rest_framework.generics import RetrieveAPIView
from model_mixins import Mixins
from django_countries.fields import CountryField
from django.contrib.auth.models import Group as AuthGroup

from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        password=None,
        is_active=True,
        is_staff=False,
        is_admin=False,
    ):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("Name is required")
        if not last_name:
            raise ValueError("Surname is required")
        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_admin
        user_obj.active = is_active
        user_obj.save(using=self.db)
        return user_obj

    def create_staffuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email, first_name, last_name, password=password, is_staff=True
        )
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


# class Group(AuthGroup):
#     class Meta:
#         proxy = True
#         app_label = "core"
#         verbose_name = "Group"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    active = models.BooleanField(default=True)

    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    preferred_name = models.CharField(max_length=25, blank=True, null=True)

    is_staff = models.BooleanField("is staff", default=False)  # ACN staff member
    is_superuser = models.BooleanField("is superuser", default=False)

    USERNAME_FIELD = "email"
    # The fields required when user is created. Email and password are required by default
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def teams(self):
        # this is because we've overridden Django's default group behaviour. We work with teams, not groups
        return [o.team for o in self.groups.all().prefetch_related("team")]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.email

    def get_permissions(self):
        from guardian.shortcuts import (
            get_objects_for_user,
        )

        permissions = [t[0] for t in Team._meta.permissions]
        teams = get_objects_for_user(
            user=self,
            perms=permissions,
            klass=Team.objects.all(),
            with_superuser=False,
            any_perm=True,
        )

        team_permissions = {}
        for permission, nice in Team._meta.permissions:
            for team in get_objects_for_user(
                user=self,
                perms=permission,
                klass=teams,
                with_superuser=False,
            ):
                team_permissions[team.id] = team_permissions.get(
                    team.id, {"id": team.id, "name": team.name, "permissions": []}
                )
                # team_permissions.get(team.id, [])
                team_permissions[team.id]["permissions"].append(permission)

        return {"teams": team_permissions}

    @property
    def is_active(self):
        return self.active

    @property
    def github_name(self):
        if self.social_profile:
            return self.social_profile.github_name


class Curriculum(models.Model, Mixins):
    short_name = models.CharField(max_length=20)  # eg:data eng
    name = models.CharField(max_length=40)  # eg: data engineering

    def __str__(self):
        return self.name

    @classmethod
    def get_next_available_id(cls):
        """get the next available content item id"""
        from django.db.models import Max

        max_id = cls.objects.aggregate(Max("id"))["id__max"]
        return (max_id or 0) + 1


class EmployerPartner(models.Model, Mixins):
    # depricated
    name = models.CharField(max_length=40)  # eg: Investic

    def __str__(self):
        return self.name


class Organisation(models.Model, Mixins):
    SCHOOL = "S"
    EMPLOYER_PARTNER = "E"

    TYPE_CHOICES = [(SCHOOL, "School"), (EMPLOYER_PARTNER, "Employer Partner")]
    name = models.CharField(max_length=40)
    country = CountryField()
    organisation_type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} {self.organisation_type} {self.country}"


class UserProfile(models.Model, Mixins):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures", null=True, blank=True
    )
    rocketchat_name = models.CharField(max_length=30, null=True, blank=True)
    cellphone_number = PhoneNumberField(null=True, blank=True)
    whatsapp_number = PhoneNumberField(null=True, blank=True)
    personal_email = models.EmailField(
        null=True, blank=True, max_length=50, unique=True
    )

    sponsor_organisation = models.ForeignKey(
        Organisation,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="sponsored_user_profiles",
    )
    school_organisation = models.ForeignKey(
        Organisation, blank=True, null=True, on_delete=models.PROTECT
    )


class UserGroup(models.Model, Mixins):
    """Depricated. REmove after data is migrated!!"""

    sponsor_organisation = models.ForeignKey(
        Organisation,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="sponsored_user_groups",
    )
    school_organisation = models.ForeignKey(
        Organisation, blank=True, null=True, on_delete=models.PROTECT
    )

    name = models.CharField(max_length=50, unique=True)
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    users = models.ManyToManyField(
        User, related_name="user_groups", through="UserGroupMembership"
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            raise Exception("Depricated. Do not create user groups")


class UserGroupMembership(models.Model, Mixins):
    """Depricated. Remove after data is migrated!!"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_memberships"
    )
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, related_name="group_memberships"
    )

    permission_student = models.BooleanField(
        default=True
    )  # this user is a student to be managed. They can see their own things
    permission_view = models.BooleanField(default=False)  # can look at all the things
    permission_manage = models.BooleanField(default=False)  # can take managment actions

    class Meta:
        unique_together = ["user", "group"]

    def save(self, *args, **kwargs):
        if not self.pk:
            raise Exception("Depricated. Do not create user group memberships")


PERMISSION_MANAGE_CARDS = "MANAGE_CARDS"
PERMISSION_VIEW_ALL = "VIEW_ALL"
PERMISSION_ASSIGN_REVIEWERS = "ASSIGN_REVIEWERS"
PERMISSION_REVIEW_CARDS = "REVIEW_CARDS"
PERMISSION_TRUSTED_REVIEWER = "TRUSTED_REVIEWER"


class Team(AuthGroup, Mixins):

    PERMISSION_MANAGE_CARDS = PERMISSION_MANAGE_CARDS  # start cards, set due date,
    PERMISSION_VIEW_ALL = PERMISSION_VIEW_ALL  # look at anything
    PERMISSION_ASSIGN_REVIEWERS = PERMISSION_ASSIGN_REVIEWERS
    PERMISSION_REVIEW_CARDS = PERMISSION_REVIEW_CARDS
    PERMISSION_TRUSTED_REVIEWER = PERMISSION_TRUSTED_REVIEWER

    PERMISSION_VIEW = [
        PERMISSION_MANAGE_CARDS,
        PERMISSION_VIEW_ALL,
        PERMISSION_ASSIGN_REVIEWERS,
        PERMISSION_REVIEW_CARDS,
        PERMISSION_TRUSTED_REVIEWER,
    ]

    sponsor_organisation = models.ForeignKey(
        Organisation,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="sponsored_teams",
    )
    school_organisation = models.ForeignKey(
        Organisation, blank=True, null=True, on_delete=models.PROTECT
    )

    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        # Team._meta.permissions
        permissions = (
            (
                PERMISSION_MANAGE_CARDS,
                "frontend: team manager (can move cards. No reviewing)",
            ),
            (PERMISSION_VIEW_ALL, "frontend: view only"),
            (
                PERMISSION_REVIEW_CARDS,
                "frontend: reviewer (can add review any card. note, this does not imply trusted reviewer)",
            ),
            (
                PERMISSION_TRUSTED_REVIEWER,
                "frontend: TRUSTED reviewer (can review all, can move cards to complete)",
            ),
        )

    def __str__(self):
        return self.name

    @property
    def users(self):
        return self.user_set

    @property
    def active_users(self):
        return self.user_set.filter(active=True)

    @property
    def members(self):
        """return a dictionary describing the group members. This is exposed via the api. See serialisers.TeamSerializer"""
        # TODO put this in the TeamSerialiser instead
        for user in self.user_set.all():
            yield {
                "user_id": user.id,
                "user_email": user.email,
                "user_active": user.active,
            }
