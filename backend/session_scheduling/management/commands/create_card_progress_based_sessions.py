"""
TODO: Change the data source. We need to work from accurate data

using https://airtable.com/appkr1uRo6nZXyeZb/tblStRQEBcQmJBDVn/viwgATZ10rBZdAZBq?blocks=hide

"""

from django.core.management.base import BaseCommand
from session_scheduling.models import Session, SessionType
from pyairtable import Api
import pandas as pd
from django.utils import timezone
from django.contrib.auth import get_user_model
from session_scheduling.session_types import SESSION_PROJECT_PROGRESS

DUE_DAYS = 7

User = get_user_model()


# TODO, put this somewhere better
import os

AIRTABLE_DT_FORMAT = "%Y-%m-%dT%H:%M:00.000Z"  # 2022-04-28T08:40:00.000Z
AIRTABLE_ACCESS_TOKEN = os.environ.get("AIRTABLE_ACCESS_TOKEN")

CUTTOFF_RED = 0.5
CUTTOFF_ORANGE = 0.25
CUTOFF_YELLOW = 0.15


def get_users_and_progress():
    df = get_progress_df()

    df_red = df[
        df["priority"] > CUTTOFF_RED
    ]  # these people need 1/1 sessions with experts

    df_orange = df[df["priority"] <= CUTTOFF_RED]  # these can be in group sessions
    df_orange = df_orange[df_orange["priority"] > CUTTOFF_ORANGE]

    df_yellow = df[
        df["priority"] <= CUTTOFF_ORANGE
    ]  # these people dont get included if they have another session coming up
    df_yellow = df_yellow[df_yellow["priority"] > CUTOFF_YELLOW]

    schedule_red_sessions(df_red.to_dict("records"))
    schedule_orange_sessions(df_orange.to_dict("records"), df_yellow.to_dict("records"))


def hydrate_learner_data(learner_dicts):
    """for each row, fetch the extra data we will need. Return a new list of dicts"""
    for d in learner_dicts:
        user = User.objects.get(email=d["email"])
        if not user.is_active:
            continue

        session_type = SessionType.objects.get(name=SESSION_PROJECT_PROGRESS)
        existing_sessions = (
            Session.objects.filter(attendees__in=[user])
            .filter(session_type=session_type)
            .filter(is_cancelled=False)
            .filter(is_complete=False)
            .count()
        )

        if existing_sessions:
            continue

        upcomming_sessions = (
            Session.objects.filter(attendees__in=[user])
            .filter(is_cancelled=False)
            .filter(is_complete=False)
            .count()
        )

        cohort_name = d["group_for_reporting"].lower()
        if (
            "web" in cohort_name xxx
        ):  # TODO!! DATA. We need to rely on configuration rather than shit I can't control.
            stream = "Web dev"
        elif "data eng" in cohort_name:
            stream = "Data eng"
        elif "data sci" in cohort_name:
            stream = "Data sci"
        else:
            print(f"Unknown stream for cohort: '{cohort_name}'")
            breakpoint()

        d["user"] = user
        d["stream"] = stream
        d["upcomming_sessions"] = upcomming_sessions

        yield d


def schedule_red_sessions(learner_dicts):
    """these learners are in a bad way. They need a session with someone who really knows what's up"""
    learner_dicts = hydrate_learner_data(learner_dicts)

    session_type = SessionType.objects.get(name=SESSION_PROJECT_PROGRESS)

    for d in learner_dicts:
        user = d["user"]

        for _ in range(2):  # red learners get 2 sessions
            session = Session.objects.create(
                session_type=session_type,
                due_date=timezone.now() + timezone.timedelta(days=DUE_DAYS),
                extra_title_text=f"{d['stream']} - RED",
            )
            session.attendees.add(user)


def schedule_orange_sessions(orange_learner_dicts, yellow_learner_dicts):
    orange_learner_dicts = hydrate_learner_data(orange_learner_dicts)
    yellow_learner_dicts = hydrate_learner_data(yellow_learner_dicts)
    yellow_learner_dicts = [
        d for d in yellow_learner_dicts if d["upcomming_sessions"] == 0
    ]

    learner_dicts = list(orange_learner_dicts) + yellow_learner_dicts

    session_type = SessionType.objects.get(name=SESSION_PROJECT_PROGRESS)

    streams = set([d["stream"] for d in learner_dicts])

    for stream in streams:
        stream_learner_dicts = [d for d in learner_dicts if d["stream"] == stream]
        stream_learner_dicts.sort(key=lambda d: d["agile_percent_core_complete"])

        groups = [
            stream_learner_dicts[x : x + 2]
            for x in range(0, len(stream_learner_dicts), 2)
        ]
        for group in groups:
            session = Session.objects.create(
                session_type=session_type,
                due_date=timezone.now() + timezone.timedelta(days=DUE_DAYS),
                extra_title_text=stream,
            )
            for d in group:
                session.attendees.add(d["user"])


def get_progress_df():
    """
    get a df with all the users who are behind on their work
    """
    assert AIRTABLE_ACCESS_TOKEN
    api = Api(AIRTABLE_ACCESS_TOKEN)
    table = api.table("appkr1uRo6nZXyeZb", "tblStRQEBcQmJBDVn")
    rows = table.all()
    # TODO: filter while we query airtable. This will return fewer rows and make the script run faster

    df = pd.DataFrame.from_records([x["fields"] for x in rows])

    df["end_date"] = pd.to_datetime(df["end_date"])
    df = df[df["end_date"] > timezone.now()]

    df["Created"] = pd.to_datetime(df["Created"])
    df = df[df["Created"] > timezone.now() - timezone.timedelta(days=7)]
    df = df.sort_values(by="Created")
    df = df.drop_duplicates(subset=["email"], keep="last")

    # filter out prov and dpd groups

    df = df[
        [
            "email",
            "how_far_in_program",
            "agile_percent_core_complete",
            "group_for_reporting",
        ]
    ]
    for s in [
        "strat",
        "design",
        "prov",
        "bridge",
        "devops",
    ]:
        df = df[~df["group_for_reporting"].str.contains(s, case=False)]

    df = df[df["how_far_in_program"] > df["agile_percent_core_complete"]]

    df["target"] = df.apply(
        lambda row: row["agile_percent_core_complete"] / row["how_far_in_program"],
        axis=1,
    )

    df["time_left"] = df.apply(lambda row: 1 - row["how_far_in_program"], axis=1)
    df["priority"] = df.apply(
        lambda row: (1 - row["target"]) / row["time_left"], axis=1
    )
    df["priority"] = pd.to_numeric(df["priority"])
    df = df.sort_values(by="priority", ascending=False)

    return df


def create_card_progress_based_sessions():
    """
    Get card progress data from airtable

    Look at duration data. If people are finished with us then skip them
    Find peeople who are falling behind in each stream

    Order people by urgency:
    - The further behind a person is, the more urgent it is
    - The further a person is in their time with us, the less time we have with them

    Group people according to where they are in their progress.
    """
    users_and_progress = get_users_and_progress()


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_card_progress_based_sessions()
        print("Done")
