from django.core.management.base import BaseCommand
from google_helpers.utils import fetch_sheet
from core.models import Curriculum, User, Team
from social_auth.models import SocialProfile
from curriculum_tracking.models import CourseRegistration
import requests
from pprint import pprint

# from curriculum_tracking.card_generation_helpers import (
#     generate_and_update_all_cards_for_user,
# )


POST_BOOT_COURSES = [POST_BOOTCAMP_SOFT_SKILLS]


STANDARD_BOOTCAMPS = [
    SEQUENCE_WEB,
    SEQUENCE_DATA_ENG,
    SEQUENCE_DATA_SCI,
    SEQUENCE_JAVA,
    SEQUENCE_IT,
]

SPECIFIC_BOOTCAMPS = {
    SEQUENCE_ALUMNI_WEB: "Alumni Web developement Bootcamp",
    SEQUENCE_ALUMNI_DATA_ENG: "Alumni Data Engineering Bootcamp",
    SEQUENCE_ALUMNI_JAVA: "Alumni Java Bootcamp",
    SEQUENCE_WEB: "Web development boot camp",
    SEQUENCE_DATA_ENG: "Data Engineering boot camp",
    SEQUENCE_DATA_SCI: "Data Science boot camp",
    SEQUENCE_JAVA: "Java boot camp",
    SEQUENCE_IT: None,
    SEQUENCE_EXTERNAL_WEB: "Web development boot camp",
}

SPECIFIC_BOOTCAMP_QUICK_WINS = {
    SEQUENCE_WEB: "Web development boot camp - quick wins",
    SEQUENCE_DATA_ENG: "Data Engineering boot camp - quick wins",
    SEQUENCE_DATA_SCI: "Data Science boot camp - quick wins",
    SEQUENCE_JAVA: "Java boot camp - quick wins",
}


def process_row(row):

    courses = []
    if course in STANDARD_BOOTCAMPS:
        courses.extend(PRE_BOOT_COURSES_NORMAL)
    elif course == SEQUENCE_EXTERNAL_WEB:
        courses.extend(PRE_BOOT_COURSES_EXTERNAL)

    else:
        courses.extend(PRE_BOOT_COURSES_ALUMNI)

    courses.append(SPECIFIC_BOOTCAMPS[course])
    courses.extend(POST_BOOT_COURSES)
    courses = [s for s in courses if s]

    print(user)
    print(course)
    pprint(courses)
    print()
