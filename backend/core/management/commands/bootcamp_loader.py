from django.core.management.base import BaseCommand


from google_helpers.utils import fetch_sheet


from core.models import Curriculum, User, Team
from social_auth.models import SocialProfile
from curriculum_tracking.models import CourseRegistration


# from curriculum_tracking.card_generation_helpers import (
#     generate_and_update_all_cards_for_user,
# )
import requests
from pprint import pprint

FIRST_NAME = "Name"
LAST_NAME = "Surname"
EMAIL = "Gmail Address"
GIT = "Link to your github profile, eg https://github.com/[YOUR_VERY_OWN_USERNAME]"
COURSE = "Course"
BOOTCAMP_NAME = "bootcamp_name"
SKIP = "BROKEN DATA"


BOOTCAMP_INTRO = "Introduction to Bootcamp and Learnership"

POST_BOOTCAMP_SOFT_SKILLS = "Post Bootcamp Soft Skills"
POST_BOOT_COURSES = [POST_BOOTCAMP_SOFT_SKILLS]

COMMON_TECH_BOOT_REQUIREMENTS = "Common tech bootcamp requirements"
TILDE_INTRO = "Intro to Tilde for tech bootcamps"
PRE_BOOT_COURSES_ALUMNI = [TILDE_INTRO, COMMON_TECH_BOOT_REQUIREMENTS]
PRE_BOOT_COURSES_NORMAL = [TILDE_INTRO, BOOTCAMP_INTRO, COMMON_TECH_BOOT_REQUIREMENTS]
PRE_BOOT_COURSES_EXTERNAL = [TILDE_INTRO, COMMON_TECH_BOOT_REQUIREMENTS]


COURSE_ALUMNI_WEB = "WD Alumni"  # these are values in the sheet
COURSE_ALUMNI_DATA_ENG = "DE Alumni"
COURSE_ALUMNI_JAVA = "Java Alumni"
COURSE_WEB = "WD"
COURSE_DATA_SCI = "DS"
COURSE_DATA_ENG = "DE"
COURSE_JAVA = "Java"
COURSE_IT = "IT"
COURSE_EXTERNAL_WEB = "WD - Ext"

TEAM_COURSE_NAME_PARTS = {  # these strings end up in the Team names
    COURSE_ALUMNI_WEB: "alumni web dev",
    COURSE_ALUMNI_DATA_ENG: "alumni data eng",
    COURSE_ALUMNI_JAVA: "alumni java",
    COURSE_WEB: "web dev",
    COURSE_DATA_ENG: "data eng",
    COURSE_JAVA: "java",
    COURSE_IT: "it support",
    COURSE_EXTERNAL_WEB: "web dev",
    COURSE_DATA_SCI: "data sci",
}

STANDARD_BOOTCAMPS = [
    COURSE_WEB,
    COURSE_DATA_ENG,
    COURSE_DATA_SCI,
    COURSE_JAVA,
    COURSE_IT,
]

SPECIFIC_BOOTCAMPS = {
    COURSE_ALUMNI_WEB: "Alumni Web developement Bootcamp",
    COURSE_ALUMNI_DATA_ENG: "Alumni Data Engineering Bootcamp",
    COURSE_ALUMNI_JAVA: "Alumni Java Bootcamp",
    COURSE_WEB: "Web development boot camp",
    COURSE_DATA_ENG: "Data Engineering boot camp",
    COURSE_DATA_SCI: "Data Science boot camp",
    COURSE_JAVA: "Java boot camp",
    COURSE_IT: None,
    COURSE_EXTERNAL_WEB: "Web development boot camp",
}


def get_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/11_Z0avz-Ca2rpA5wsPoHc75ut6tCN8M5tfsOsbKyhhE/edit#gid=0"
    )
    df = df.dropna(subset=[EMAIL])
    df = df.dropna(subset=[COURSE])
    df = df[df[COURSE] != ""]
    if SKIP in df.columns:
        df = df[df[SKIP] == ""]

    # df = df[df[EMAIL].str.contains("gmail")]
    df.columns = [s.strip() for s in df.columns]
    return df


def set_course_reg(user, course_names):
    curriculums = []
    for name in course_names:
        print(name)
        curriculums.append(Curriculum.objects.get(name=name))

    course_ids = [curriculum.id for curriculum in curriculums]
    existing = CourseRegistration.objects.filter(user=user)
    for o in existing:
        if o.curriculum_id not in course_ids:
            o.delete()
    for i, curriculum_id in enumerate(course_ids):
        o, created = CourseRegistration.objects.get_or_create(
            user=user, curriculum_id=curriculum_id, defaults={"order": i}
        )
        if not created:
            o.order = i
            o.save()


def clean_github_username(name):
    name = name.strip().strip("/")
    if name.startswith("https://"):
        name = name[19:]
    if name.startswith("http://"):
        name = name[18:]
    return name


def check_email(row):
    email = row[EMAIL].strip()
    if email.endswith("@gmail.com"):
        return True
    if email.endswith("@umuzi.org"):
        return True
    print(f"INVALID EMAIL ERROR {row[EMAIL]}")

    return False


def check_github(row):
    github = clean_github_username(row[GIT].strip())
    final_url = f"https://github.com/{github}"
    if requests.get(final_url).status_code == 404:
        print(f"GITHUB 404 ERROR: {row[EMAIL]} {row[GIT]} => final_url = {final_url}")
        return False
    return True


def get_team(course, title):

    name = f"Boot {TEAM_COURSE_NAME_PARTS[course]} {title}"
    return Team.objects.get_or_create(name=name)[0]


def process_row(row):

    email = row[EMAIL].strip()
    first_name = row[FIRST_NAME].strip()
    last_name = row[LAST_NAME].strip()
    github = clean_github_username(row[GIT].strip())
    course = row[COURSE].strip()

    user = User.objects.get_or_create(
        email=email, defaults={"first_name": first_name, "last_name": last_name}
    )[0]
    user.active = True
    user.save()

    profile = SocialProfile.objects.get_or_create(user=user)[0]
    profile.github_name = github
    profile.save()

    team = get_team(course, row[BOOTCAMP_NAME])
    team.user_set.add(user)

    # return
    courses = []
    if course in STANDARD_BOOTCAMPS:
        courses.extend(PRE_BOOT_COURSES_NORMAL)
    elif course == COURSE_EXTERNAL_WEB:
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

    set_course_reg(user, courses)


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = get_df()
        # df.apply(check_github, axis=1)
        # df.apply(check_email, axis=1)
        df.apply(process_row, axis=1)
