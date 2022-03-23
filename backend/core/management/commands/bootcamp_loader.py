from django.core.management.base import BaseCommand
from google_helpers.utils import fetch_sheet
from core.models import Curriculum, User, Team
from social_auth.models import SocialProfile
from curriculum_tracking.models import CourseRegistration
import requests

# from pprint import pprint

FIRST_NAME = "Name"
LAST_NAME = "Surname"
EMAIL = "Gmail Address"
GIT = "Link to your github profile, eg https://github.com/[YOUR_VERY_OWN_USERNAME]"
COURSE = "Course"
BOOTCAMP_NAME = "bootcamp_name"
SKIP = "BROKEN DATA"

SEQUENCE_ALUMNI_WEB = "WD Alumni"  # these are values in the sheet
SEQUENCE_ALUMNI_DATA_ENG = "DE Alumni"
SEQUENCE_ALUMNI_JAVA = "Java Alumni"
SEQUENCE_WEB = "WD"
SEQUENCE_DATA_SCI = "DS"
SEQUENCE_DATA_ENG = "DE"
SEQUENCE_JAVA = "Java"
SEQUENCE_SKILL_TEST_WEB = "Skills Test WD"
SEQUENCE_SKILL_TEST_DATA_SCI = "Skills Test DS"
SEQUENCE_SKILL_TEST_DATA_ENG = "Skills Test DE"
SEQUENCE_SKILL_TEST_JAVA = "Skills Test Java"
SEQUENCE_IT = "IT"
SEQUENCE_EXTERNAL_WEB = "WD - Ext"
SEQUENCE_DPD = "DPD"

TEAM_COURSE_NAME_PARTS = {  # these strings end up in the Team names
    SEQUENCE_ALUMNI_WEB: "alumni web dev",
    SEQUENCE_ALUMNI_DATA_ENG: "alumni data eng",
    SEQUENCE_ALUMNI_JAVA: "alumni java",
    SEQUENCE_SKILL_TEST_WEB: "skills test web dev",
    SEQUENCE_SKILL_TEST_DATA_SCI: "skills test data sci",
    SEQUENCE_SKILL_TEST_DATA_ENG: "skills test data eng",
    SEQUENCE_SKILL_TEST_JAVA: "skills test java",
    SEQUENCE_WEB: "web dev",
    SEQUENCE_DATA_ENG: "data eng",
    SEQUENCE_JAVA: "java",
    SEQUENCE_IT: "it support",
    SEQUENCE_EXTERNAL_WEB: "web dev",
    SEQUENCE_DATA_SCI: "data sci",
    SEQUENCE_DPD: "dpd",
}


TILDE_INTRO = "Intro to Tilde for tech bootcamps"
TILDE_INTRO_NON_TECH = "Intro to Tilde for non-coder bootcampers"
BOOTCAMP_INTRO = "Introduction to Bootcamp and Learnership"
COMMON_TECH_BOOT_REQUIREMENTS = "Common tech bootcamp requirements"
POST_BOOTCAMP_SOFT_SKILLS = "Post Bootcamp Soft Skills"
DPD_BOOTCAMP = "UX Strategy Syllabus"
SKILL_TEST_WEB = "Employed Web Development skills test"
SKILL_TEST_DATA_SCI = "Employed Data Science skills test"
SKILL_TEST_DATA_ENG = "Employed Data Engineering skills test"
SKILL_TEST_JAVA = "Employed Java skills test"
SKILLS_TEST_TILDE_1 = "Employed learnership intro to Tilde part 1"
SKILLS_TEST_TILDE_2 = "Employed learnership intro to Tilde part 2"
SKILLS_TEST_COMMON_TECH_BOOT_REQUIREMENTS = "Employed common tech reqirements"

# PRE_BOOT_COURSES_ALUMNI = [TILDE_INTRO, COMMON_TECH_BOOT_REQUIREMENTS]
# PRE_BOOT_COURSES_NORMAL = [TILDE_INTRO, BOOTCAMP_INTRO, COMMON_TECH_BOOT_REQUIREMENTS]
# PRE_BOOT_COURSES_EXTERNAL = [TILDE_INTRO, COMMON_TECH_BOOT_REQUIREMENTS]


SEQUENCE_COURSES = {
    SEQUENCE_JAVA: [
        TILDE_INTRO,
        BOOTCAMP_INTRO,
        "Java boot camp - quick wins",
        COMMON_TECH_BOOT_REQUIREMENTS,
        "Java boot camp",
        POST_BOOTCAMP_SOFT_SKILLS,
    ],
    SEQUENCE_DATA_SCI: [
        TILDE_INTRO,
        BOOTCAMP_INTRO,
        "Data Science boot camp - quick wins",
        COMMON_TECH_BOOT_REQUIREMENTS,
        "Data Science boot camp",
        POST_BOOTCAMP_SOFT_SKILLS,
    ],
    SEQUENCE_DATA_ENG: [
        TILDE_INTRO,
        BOOTCAMP_INTRO,
        "Data Engineering boot camp - quick wins",
        COMMON_TECH_BOOT_REQUIREMENTS,
        "Data Engineering boot camp",
        POST_BOOTCAMP_SOFT_SKILLS,
    ],
    SEQUENCE_WEB: [
        TILDE_INTRO,
        BOOTCAMP_INTRO,
        "Web development boot camp - quick wins",
        COMMON_TECH_BOOT_REQUIREMENTS,
        "Web development boot camp",
        POST_BOOTCAMP_SOFT_SKILLS,
    ],
    SEQUENCE_DPD: [
        TILDE_INTRO_NON_TECH,
        DPD_BOOTCAMP,
    ],
    SEQUENCE_SKILL_TEST_WEB: [
        SKILLS_TEST_TILDE_1,
        SKILL_TEST_WEB,
        SKILLS_TEST_TILDE_2,
        SKILLS_TEST_COMMON_TECH_BOOT_REQUIREMENTS,
    ],
    SEQUENCE_SKILL_TEST_DATA_SCI: [
        SKILLS_TEST_TILDE_1,
        SKILL_TEST_DATA_SCI,
        SKILLS_TEST_TILDE_2,
        SKILLS_TEST_COMMON_TECH_BOOT_REQUIREMENTS,
    ],
    SEQUENCE_SKILL_TEST_DATA_ENG: [
        SKILLS_TEST_TILDE_1,
        SKILL_TEST_DATA_ENG,
        SKILLS_TEST_TILDE_2,
        SKILLS_TEST_COMMON_TECH_BOOT_REQUIREMENTS,
    ],
    SEQUENCE_SKILL_TEST_JAVA: [
        SKILLS_TEST_TILDE_1,
        SKILL_TEST_JAVA,
        SKILLS_TEST_TILDE_2,
        SKILLS_TEST_COMMON_TECH_BOOT_REQUIREMENTS,
    ],
}


def get_df(url):
    df = fetch_sheet(url=url)
    df = df.dropna(subset=[EMAIL])
    df = df.dropna(subset=[COURSE])
    df = df[df[COURSE] != ""]
    if SKIP in df.columns:
        df = df[df[SKIP] == ""]

    df[EMAIL] = df[EMAIL].str.lower()
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
    if name.startswith("com/"):
        name = name[4:]

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
    # todo make use of github api user_exists function
    if GIT not in row:
        return True
    github = clean_github_username(row[GIT].strip())
    final_url = f"https://github.com/{github}"
    if requests.get(final_url).status_code == 404:
        print(f"GITHUB 404 ERROR: {row[EMAIL]} {row[GIT]} => final_url = {final_url}")
        return False
    return True


def get_team(sequence, title):

    name = f"Boot {TEAM_COURSE_NAME_PARTS[sequence]} {title}"
    return Team.objects.get_or_create(name=name)[0]


def setup_user(email, first_name, last_name, github, sequence, bootcamp_name):
    user = User.objects.get_or_create(
        email=email, defaults={"first_name": first_name, "last_name": last_name}
    )[0]
    user.active = True
    user.save()

    if github:
        profile = SocialProfile.objects.get_or_create(user=user)[0]
        profile.github_name = github
        profile.save()

    team = get_team(sequence, bootcamp_name)
    team.user_set.add(user)

    # add the user to github org

    print(f"User setup completed for: {user}")

    return user


def process_row(row):
    email = row[EMAIL].strip()
    first_name = row[FIRST_NAME].strip()
    last_name = row[LAST_NAME].strip()
    github = clean_github_username(row.get(GIT, "").strip())
    sequence = row[COURSE].strip()
    bootcamp_name = row[BOOTCAMP_NAME]

    user = setup_user(email, first_name, last_name, github, sequence, bootcamp_name)

    courses = SEQUENCE_COURSES[sequence]

    set_course_reg(user, courses)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("sheet_url", type=str)

    def handle(self, *args, **options):
        df = get_df(url=options["sheet_url"])
        df.apply(check_github, axis=1)
        print("GITHUB OK")
        df.apply(check_email, axis=1)
        print("Emails ok")
        df.apply(process_row, axis=1)
