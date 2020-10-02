from core.models import User, Cohort, RecruitCohort, UserGroup, UserGroupMembership
import csv
from copy import copy

default = {
    "cohort": None,
    "groups": [],
    "sponsor_organisation": None,
    "school_organisation": None,
    "employed_by_organisation": None,
    "course_registrations": [],
}


def get_export_data():
    d = {}
    for o in RecruitCohort.objects.all():
        user = o.user
        cohort = o.cohort

        d[user.email] = d.get(user.email, copy(default))


class Command(BaseCommand):
    def handle(self, *args, **options):
        l = get_export_data()
