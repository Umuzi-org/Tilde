"""
This script gets run after a bunch of people get accepted from a bootcamp. They get some umuzi email addresses, rocketchat users, etc
"""

from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Team
from ..rocketchat import Rocketchat, GROUP
from core.models import User
from google_helpers.utils import fetch_sheet
from curriculum_tracking.models import ContentItem, Curriculum, CourseRegistration
import os

from ..course_streams import COURSES_BY_STREAM

OLD_EMAIL = "Old Email"
NEW_EMAIL = "New Email"
TEAM_NAME = "Team"
DEPARTMENT = "department"
BROKEN = "broken"


comment_intro = """Don't take this personally, I'm just a robot.
I'm marking your code as Not Yet Competent because our standards are actually pretty high.

You gave us code that was good enough to get you through bootcamp, we can see you have the aptitude for this stuff. But for now on you will need to be writing professional level code.

That means your code must be sparkley and clean, neat and tidy, well named and well formatted. One day when you are working on a team of rock star professional developers they'll all think you are a friggin ninja because your code will be the most beautiful code they've seen.

Please go through everything and make sure that:

- there are no global variables used in functions
- all variable names make sense
- all names are consistent with the style of your language
- you don't have any comments that just rewrite the code in English
"""
python_comments = f"""{comment_intro}
Since you are working in Python:

- Make sure you use the `black` formatter to make your code nice and pretty. You can install it and then set up vscode so it auto-formats your code every time you hit save
- use python naming conventions:
    - this_is_how_variables_are_named
    - functions_as_well
    - dontDoThis
    - definitely_Dont_Do_This
    - ClassesAreNamedLikeThis

"""
js_comments = f"""{comment_intro}
Since you are working in Javascript:

- Make sure you use the `eslint` to make your code nice and pretty. You can install Prettier in vscode and set it up to auto-format your code every time you hit save.
- use Javascript naming conventions:
    - thisIsHowVariablesAreNamed
    - functionsToo
    - dont_do_this
    - definitely_Dont_Do_This
    - ClassesAreNamedLikeThis

"""


def update_user_email(row):
    print(f"{row[OLD_EMAIL]} => {row[NEW_EMAIL]}")
    try:
        user = User.objects.get(email=row[OLD_EMAIL])
    except User.DoesNotExist:
        user = User.objects.get(email=row[NEW_EMAIL])

    user.email = row[NEW_EMAIL]
    user.save()
    print()


def set_up_course_registrations(row):
    # print(row)

    user = User.objects.get(email=row[NEW_EMAIL])
    course_names = COURSES_BY_STREAM[row[DEPARTMENT]]
    set_course_reg(user, course_names)


def set_course_reg(user, course_names):
    curriculums = []
    for name in course_names:
        # print(name)
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


def add_user_to_group(row):
    team, _ = Team.objects.get_or_create(name=row[TEAM_NAME].strip())
    user = User.objects.get(email=row[NEW_EMAIL])
    team.users.add(user)

    team = Team.objects.get(name="Problem Solving Foundation 1")
    team.users.add(user)


def create_rocketchat_user_and_add_to_channel(client, managment_usernames):
    managment_user_ids = [
        client.get_existing_user(username=username).user_id
        for username in managment_usernames
    ]

    def _create_rocketchat_user_and_add_to_channel(row):

        username = row[NEW_EMAIL].split("@")[0]
        name = " ".join([s.capitalize() for s in username.split(".")])
        channel_name = row[TEAM_NAME].replace(" ", "-").lower()

        user = client.create_user_if_not_exists(
            name=name, username=username, email=row[NEW_EMAIL], password=row[NEW_EMAIL]
        )

        channel = client.create_channel_if_not_exists(
            name=channel_name,
            channel_type=GROUP,
        )

        client.add_user_to_channnel(user.user_id, channel.channel_id)

        for user_id in managment_user_ids:
            client.add_user_to_channnel(user_id, channel.channel_id)

    return _create_rocketchat_user_and_add_to_channel


def setup_rocketchat_users(df):
    rocketchat_user = os.environ["ROCKETCHAT_USER"]
    rocketchat_pass = os.environ["ROCKETCHAT_PASS"]
    client = Rocketchat()
    client.login(rocketchat_user, rocketchat_pass)
    try:
        df.apply(
            create_rocketchat_user_and_add_to_channel(
                client, ["ryan", "asanda", "sheena"]
            ),
            axis=1,
        )
    except:
        import traceback

        print(traceback.format_exc())
    finally:
        client.logout()


def re_review_cards(row):
    # user = User.objects.get(email=row[NEW_EMAIL])
    from curriculum_tracking.models import AgileCard, RecruitProjectReview
    from django.db.models import Q
    from backend.settings import CURRICULUM_TRACKING_REVIEW_BOT_EMAIL
    from django.utils import timezone

    from curriculum_tracking.constants import NOT_YET_COMPETENT

    cards = (
        AgileCard.objects.filter(assignees__email__in=[row[NEW_EMAIL]])
        .filter(
            Q(content_item__project_submission_type=ContentItem.REPOSITORY)
            | Q(content_item__project_submission_type=ContentItem.CONTINUE_REPO)
            | Q(content_item__project_submission_type=ContentItem.LINK)
        )
        .filter(status=AgileCard.COMPLETE)
    )

    bot, _ = User.objects.get_or_create(email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL)

    for card in cards:
        # print(card)
        if "Tilde project tutorial" in card.content_item.title:
            continue
        flavours = card.flavour_names
        if "markdown" in flavours:
            continue
        if flavours == []:
            continue
        elif "python" in flavours:
            comments = python_comments
        elif "javascript" in flavours:
            comments = js_comments
        else:
            raise Exception(f"Can't handle: {flavours}")
        RecruitProjectReview.objects.create(
            status=NOT_YET_COMPETENT,
            timestamp=timezone.now(),
            comments=comments,
            recruit_project=card.recruit_project,
            reviewer_user=bot,
        )

        card.refresh_from_db()
        if card.status == AgileCard.COMPLETE:
            breakpoint()
            pass


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        path = options["path"]

        df = fetch_sheet(url=path)
        df[OLD_EMAIL] = df[OLD_EMAIL].str.strip()
        df[NEW_EMAIL] = df[NEW_EMAIL].str.strip()
        df = df.dropna(subset=[OLD_EMAIL])
        df = df[df[BROKEN] != 1]
        df = df[df[BROKEN] != "1"]
        df = df[df[OLD_EMAIL] != ""]
        # df = pd.read_csv(path)

        df.apply(update_user_email, axis=1)
        df.apply(add_user_to_group, axis=1)
        df.apply(set_up_course_registrations, axis=1)
        setup_rocketchat_users(df)

        df.apply(re_review_cards, axis=1)
