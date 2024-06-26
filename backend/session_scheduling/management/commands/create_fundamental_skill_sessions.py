"""
Run this script every 2 weeks

These sessions cover things like for loops, return statements and that sort of thing.

There are 2 types of sessions here:

SESSION_FUNDAMENTAL_SKILL_ASSISTANCE: This is for people who are clearly struggling and need help
SESSION_FUNDAMENTAL_SKILL_SPOT_CHECK: This is for people who seem to be doing ok. We are simply validating our own mechanisms 

If our spot checks tend to pass, then we can rethink assessment cards

TODO: skip learners who have upcoming sessions? 
TODO: if people are failing our spot checks, make the strength measure more accurate. Eg only look people who have been pod leaders and take peer reviews into account
"""

from django.core.management.base import BaseCommand
from session_scheduling.models import Session, SessionType
from session_scheduling.session_types import (
    SESSION_FUNDAMENTAL_SKILL_SPOT_CHECK,
    SESSION_FUNDAMENTAL_SKILL_ASSISTANCE,
)
from django.db.models import Q
from curriculum_tracking.models import AgileCard
from google_helpers.utils import fetch_sheet
import pandas as pd
from django.contrib.auth import get_user_model
import random
from django.utils import timezone
from ..helpers import (
    group_learners,
    card_name_skill_name_mapping,
    get_skill_name_from_pod_column_name,
)


User = get_user_model()

DUE_DAYS = 21
ASSISTANCE_GROUP_SIZE = 3  
SPOT_CHECK_GROUP_SIZE = 3


def get_score(raw_value: str) -> int:
    """Learners capture scores in the format:
    `{score}. description`
    eg: `2. I have some idea what it is`

    This function takes that string and just gets the actual score from it
    """
    return int(raw_value.split(".")[0])


def get_learner_pod_self_report():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/1WMWI9YkEb8CtOFP3YGTTL0N4OPWlwoFdKMkZz6vXdlg"
    )

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    df["Email Address"] = df["Email Address"].str.lower().str.strip()
    df = df.drop_duplicates(keep="last", subset=["Email Address"])
    for column in df.columns:
        if column.startswith("How skilled do you think you are?"):
            df[column] = df[column].apply(get_score)
    return df


def get_weak_learners(df, pod_skill_name):
    df = df[df[pod_skill_name] == 2]
    return df


def get_strong_learners(df, pod_skill_name):
    df = df[df[pod_skill_name] >= 3]
    return df


def schedule_session(
    session_type,
    user_ids,
    flavour_names,
    skill_name,
):
    assert skill_name
    session = Session.objects.create(
        session_type=SessionType.objects.get(name=session_type),
        due_date=timezone.now() + timezone.timedelta(days=DUE_DAYS),
    )
    session.set_flavours(flavour_names)
    session.extra_title_text = skill_name
    session.save()

    for user_id in user_ids:
        session.attendees.add(User.objects.get(pk=user_id))


def create_assistance_sessions_for_weak_learners(df_self_report):

    needs = {
        # skill_name_1 : {
        #    flavour_1 : [list of user ids],
        #    flavour_2 : [...],
        #    ...
        # },
        # skill_name_2 : ...
    }

    for card_title, pod_skill_name in card_name_skill_name_mapping.items():
        nice_skill_name = get_skill_name_from_pod_column_name(pod_skill_name)
        needs[nice_skill_name] = {}

        weak_learners = get_weak_learners(df_self_report, pod_skill_name)

        for email in weak_learners["Email Address"].tolist():

            user = User.objects.filter(email=email).filter(active=True).first()
            if user == None:
                continue

            card = (
                AgileCard.objects.filter(content_item__title=card_title)
                .filter(assignees=user)
                .first()
            )
            if card == None:
                continue

            flavour = " ".join(card.flavour_names)

            needs[nice_skill_name][flavour] = needs[nice_skill_name].get(flavour, [])
            needs[nice_skill_name][flavour].append(user.id)

    # now group people up and add some sessions

    for skill_name in needs:
        for flavour in needs[skill_name]:
            users = needs[skill_name][flavour]
            groups = group_learners(users, ASSISTANCE_GROUP_SIZE)

            for group in groups:
                schedule_session(
                    session_type=SESSION_FUNDAMENTAL_SKILL_ASSISTANCE,
                    user_ids=group,
                    flavour_names=flavour.split(),
                    skill_name=skill_name,
                )


def create_spot_check_sessions_for_strong_learners(df_self_report):

    needs = {}

    for card_title, pod_skill_name in card_name_skill_name_mapping.items():
        nice_skill_name = get_skill_name_from_pod_column_name(pod_skill_name)
        needs[nice_skill_name] = {}

        strong_learners = get_strong_learners(df_self_report, pod_skill_name)

        for email in strong_learners["Email Address"].tolist():

            user = User.objects.filter(email=email).filter(active=True).first()
            if user == None:
                continue
            if user.is_staff: # the staff are already competent
                continue

            card = (
                AgileCard.objects.filter(content_item__title=card_title)
                .filter(assignees=user)
                .filter(~Q(status=AgileCard.COMPLETE))
                .filter(~Q(status=AgileCard.BLOCKED))
                .filter(
                    recruit_project__code_review_competent_since_last_review_request=0
                )
                .first()
            )
            if card == None:
                continue

            flavour = " ".join(card.flavour_names)

            needs[nice_skill_name][flavour] = needs[nice_skill_name].get(flavour, [])
            needs[nice_skill_name][flavour].append(user.id)

    # now group them up and add them to sessions
    for skill_name in needs:
        for flavour in needs[skill_name]:
            users = needs[skill_name][flavour]
            random.shuffle(users)
            groups = group_learners(users, SPOT_CHECK_GROUP_SIZE)

            for group in groups[:1]:  # just do one of each card type for now
                schedule_session(
                    session_type=SESSION_FUNDAMENTAL_SKILL_SPOT_CHECK,
                    user_ids=group,
                    flavour_names=flavour.split(),
                    skill_name=skill_name,
                )


def create_fundamental_skill_sessions():
    df_self_report = get_learner_pod_self_report()
    create_assistance_sessions_for_weak_learners(df_self_report)
    # create_spot_check_sessions_for_strong_learners(df_self_report)


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_fundamental_skill_sessions()
        print("Done")
