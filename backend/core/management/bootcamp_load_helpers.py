from core.models import (
    User,
    UserProfile,
    Curriculum,
    Cohort,
    RecruitCohort,
    EmployerPartner,
)
from curriculum_tracking.models import CourseRegistration
from social_auth.models import SocialProfile
from django.core.management.base import BaseCommand

from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)
from google_helpers.utils import fetch_sheet

CURRICULUM_SHORT_NAME_DS_PRE_BOOT = "data sci prebootcamp"
CURRICULUM_SHORT_NAME_DS_BOOT = "data sci boot"
CURRICULUM_SHORT_NAME_WEB_PRE_BOOT = "web dev pre boot"
CURRICULUM_SHORT_NAME_WEB_BOOT = "web dev boot"

DEPT_WEB = "Web Development"
DEPT_DS = "Data Science"


def data_science_curriculums():
    return [
        Curriculum.objects.get(short_name=CURRICULUM_SHORT_NAME_DS_PRE_BOOT),
        Curriculum.objects.get(short_name=CURRICULUM_SHORT_NAME_DS_BOOT),
    ]


def web_dev_curriculums():
    return [
        Curriculum.objects.get(short_name=CURRICULUM_SHORT_NAME_WEB_PRE_BOOT),
        Curriculum.objects.get(short_name=CURRICULUM_SHORT_NAME_WEB_BOOT),
    ]


data_science_curriculums = data_science_curriculums()
web_dev_curriculums = web_dev_curriculums()
