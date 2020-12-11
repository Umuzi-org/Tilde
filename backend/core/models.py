from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.core.mail import send_mail
# import secrets
import re
from model_mixins import Mixins
from django_countries.fields import CountryField
from django.contrib.auth.models import Group as AuthGroup


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


class Group(AuthGroup):
    class Meta:
        proxy = True
        app_label = "core"
        verbose_name = "Group"


from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    active = models.BooleanField(default=True)
    # staff = models.BooleanField(default=False)
    # admin = models.BooleanField(default=False)

    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    preferred_name = models.CharField(max_length=25, blank=True, null=True)

    is_student = models.BooleanField("is student", default=False)
    is_staff = models.BooleanField("is staff", default=False)  # ACN staff member
    is_superuser = models.BooleanField("is superuser", default=False)

    is_reviewer = models.BooleanField(
        "is reviewer", default=False
    )  # can review anyone's code
    is_trusted_reviewer = models.BooleanField(
        "is trusted reviewer", default=False
    )  # competent and excellent reviews move cards always

    # groups = models.ManyToManyField(Group)

    USERNAME_FIELD = "email"
    # The fields required when user is created. Email and password are required by default
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     from django.contrib.auth.models import _user_has_perm

    #     if self.is_active and self.is_superuser:
    #         return True

    #     # Otherwise we need to check the backends.
    #     return _user_has_perm(self, perm, obj)

    # def has_module_perms(self, app_labels):
    #     from django.contrib.auth.models import _user_has_module_perms

    #     if self.is_active and self.is_superuser:
    #         return True

    #     return _user_has_module_perms(self, app_label)

    @property
    def is_active(self):
        return self.active


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


PERMISSION_MOVE_CARDS = "MOVE_CARDS"
PERMISSION_VIEW_ALL = "VIEW_ALL"
PERMISSION_ASSIGN_REVIEWERS = "ASSIGN_REVIEWERS"


class Team(models.Model, Mixins):

    PERMISSION_MOVE_CARDS = PERMISSION_MOVE_CARDS
    PERMISSION_VIEW_ALL = PERMISSION_VIEW_ALL
    PERMISSION_ASSIGN_REVIEWERS = PERMISSION_ASSIGN_REVIEWERS

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

    name = models.CharField(max_length=50, unique=True)
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    users = models.ManyToManyField(User, related_name="teams", through="TeamMembership")

    class Meta:

        permissions = (
            (PERMISSION_MOVE_CARDS, "Can move cards"),
            (PERMISSION_VIEW_ALL, "View all"),
            (PERMISSION_ASSIGN_REVIEWERS, "Assign Reviewers"),
        )

    def __str__(self):
        return self.name

    @property
    def active_student_users(self):
        l = TeamMembership.objects.filter(
            group=self, permission_student=True, user__active=True
        )
        return [o.user for o in l]

    @property
    def members(self):
        """return a dictionary describing the group members. This is exposed via the api. See serialisers.TeamSerializer"""
        for membership in self.team_memberships.all():
            yield {
                "user_id": membership.user_id,
                "user_email": membership.user.email,
                "permission_student": membership.permission_student,
                "permission_view": membership.permission_view,
                "permission_manage": membership.permission_manage,
            }


class TeamMembership(models.Model, Mixins):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="team_memberships"
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team_memberships"
    )

    permission_student = models.BooleanField(
        default=True
    )  # this user is a student to be managed. They can see their own things
    permission_view = models.BooleanField(default=False)  # can look at all the things
    permission_manage = models.BooleanField(default=False)  # can take managment actions

    class Meta:
        unique_together = ["user", "team"]


class Cohort(models.Model, Mixins):
    start_date = models.DateField()
    end_date = models.DateField()

    cohort_number = models.IntegerField()
    cohort_curriculum = models.ForeignKey(
        Curriculum, on_delete=models.PROTECT, related_name="cohorts"
    )
    label = models.CharField(
        max_length=10, blank=True, null=True
    )  # eg for C14 web BBD this value would be "BBD"

    active = models.BooleanField(default=True)
    suppress_card_generation = models.BooleanField(default=False)

    def __str__(self):
        s = f"C{self.cohort_number} {self.cohort_curriculum.short_name}"
        if self.label:
            return f"{s} ({self.label})"
        return s

    def get_member_users(self):
        return [o.user for o in RecruitCohort.objects.filter(cohort=self)]

    @property
    def cohort_recruit_users(self):
        """return a list of ids for use by api"""
        # return [o.user_id for o in RecruitCohort.objects.filter(cohort=self)]
        return [o.user_id for o in self.cohort_recruits.all()]

    @property
    def cohort_recruit_user_emails(self):
        return [o.user.email for o in self.cohort_recruits.all()]

    @property
    def curriculum_short_name(self):
        return self.cohort_curriculum.short_name

    @property
    def curriculum_name(self):
        return self.cohort_curriculum.name

    @classmethod
    def get_from_short_name(cls, name):
        if name.startswith("C"):
            name = name[1:]
        found = re.search("^(\d+) (.+)$", name)
        assert (
            found
        ), "badly formed name. Should be something like C21 web dev, where 'web dev' would be the short_name of the cohort"
        (number, short_name) = found.groups()
        return cls.objects.get(
            cohort_number=int(number), cohort_curriculum__short_name=short_name.strip()
        )


class RecruitCohort(models.Model, Mixins):
    # depricated
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="recruit_cohorts"
    )

    cohort = models.ForeignKey(
        Cohort, on_delete=models.PROTECT, related_name="cohort_recruits"
    )
    employer_partner = models.ForeignKey(
        EmployerPartner,
        on_delete=models.PROTECT,  # TODO blank=True, null=True
    )
    start_date = models.DateField()  # TODO blank=True, null=True
    end_date = models.DateField()  # TODO blank=True, null=True

    def __str__(self):
        return f"{self.cohort} - {self.user}"

    @property
    def email(self):
        return user.email


class ProductTeam(models.Model, Mixins):
    name = models.CharField(max_length=50)

    users = models.ManyToManyField(
        User, related_name="product_teams", through="ProductTeamMembership"
    )

    def __str__(self):
        return self.name

    def get_member_users(self):
        return self.users.all()


class ProductTeamMembership(models.Model, Mixins):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_team = models.ForeignKey(ProductTeam, on_delete=models.CASCADE)
