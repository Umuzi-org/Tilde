"""
Learners can be at risk of not completing their programme for many reasons. For example, maybe they are falling behind on their coursework, or they could be struggling with their coderbyte tests. There could be other reasons as well.

This script grabs data about the learners who are struggling in different ways.

We then export the data as a spreadsheet so that we can get a picture of what is needed at every point.
"""

from typing import Any
from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand
from pyairtable import Api
import pandas as pd
from django.utils import timezone
from django.contrib.auth import get_user_model
from session_scheduling.session_types import SESSION_PROJECT_PROGRESS

User = get_user_model()

import os

AIRTABLE_DT_FORMAT = "%Y-%m-%dT%H:%M:00.000Z"  # 2022-04-28T08:40:00.000Z
AIRTABLE_ACCESS_TOKEN = os.environ.get("AIRTABLE_ACCESS_TOKEN")

CUTTOFF_RED = 0.5
CUTTOFF_ORANGE = 0.25
CUTOFF_YELLOW = 0.15


PSF_LEVEL_0_RED = "PSF_LEVEL_0_RED"
PSF_LEVEL_0_ORANGE = "PSF_LEVEL_0_ORANGE"
PSF_LEVEL_0_YELLOW = "PSF_LEVEL_0_YELLOW"
PSF_LEVEL_1_RED = "PSF_LEVEL_1_RED"
PSF_LEVEL_1_ORANGE = "PSF_LEVEL_1_ORANGE"
PSF_LEVEL_1_YELLOW = "PSF_LEVEL_1_YELLOW"
CARD_PROGRESS_RED = "CARD_PROGRESS_RED"
CARD_PROGRESS_ORANGE = "CARD_PROGRESS_ORANGE"
CARD_PROGRESS_YELLOW = "CARD_PROGRESS_YELLOW"


risk_priority_order = [
    PSF_LEVEL_0_RED,
    PSF_LEVEL_0_ORANGE,
    PSF_LEVEL_0_YELLOW,
    CARD_PROGRESS_RED,
    PSF_LEVEL_1_RED,
    CARD_PROGRESS_ORANGE,
    PSF_LEVEL_1_ORANGE,
    CARD_PROGRESS_YELLOW,
    PSF_LEVEL_1_YELLOW,
]


def get_card_progress_df():
    """
    get a df with all the users who are behind on their work. This data comes from airtable
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
    ]:
        df = df[~df["group_for_reporting"].str.contains(s, case=False)]

    # df = df[df["how_far_in_program"] > df["agile_percent_core_complete"]]

    # df["target"] = df.apply(
    #     lambda row: row["agile_percent_core_complete"] / row["how_far_in_program"],
    #     axis=1,
    # )

    # df["time_left"] = df.apply(lambda row: 1 - row["how_far_in_program"], axis=1)
    # df["progress_priority"] = df.apply(
    #     lambda row: (1 - row["target"]) / row["time_left"], axis=1
    # )
    # df["progress_priority"] = pd.to_numeric(df["progress_priority"])
    # df = df.sort_values(by="progress_priority", ascending=False)

    return df


def get_problem_solving_level(row):
    email = row["email"]
    user = User.objects.get(email=email)
    from coderbyte_tests.management.utils import get_current_psf_level_for_user

    return get_current_psf_level_for_user(user)


def user_is_active(row):
    email = row["email"]
    user = User.objects.get(email=email)
    return user.is_active


def calculate_progress_based_risk_score(row):
    how_far_is_the_learner = row["agile_percent_core_complete"]
    how_far_should_they_be = row["how_far_in_program"]

    risk_score = (how_far_should_they_be - how_far_is_the_learner) / (
        1 - how_far_should_they_be
    )
    return risk_score


def get_psf_risk(row):
    level = row["problem_solving_level"]
    time_elapsed = row["how_far_in_program"]

    if level >= 2:
        return

    if level == 0:
        if time_elapsed > 0.3:
            return PSF_LEVEL_0_RED

        if time_elapsed > 0.2:
            return PSF_LEVEL_0_ORANGE

        if time_elapsed > 0.1:
            return PSF_LEVEL_0_YELLOW

    if level == 1:
        if time_elapsed > 0.8:
            return PSF_LEVEL_1_RED

        if time_elapsed > 0.7:
            return PSF_LEVEL_1_ORANGE

        if time_elapsed > 0.6:
            return PSF_LEVEL_1_YELLOW


def get_progress_risk(row):
    progress_based_risk_score = row["progress_based_risk_score"]

    if progress_based_risk_score > 0.75:
        return CARD_PROGRESS_RED
    if progress_based_risk_score > 0.5:
        return CARD_PROGRESS_ORANGE
    if progress_based_risk_score > 0.1:
        return CARD_PROGRESS_YELLOW


def get_highest_priority_problem_to_address(row):
    risks = [s for s in [row["psf_risk"], row["progress_risk"]] if s]
    if len(risks):
        risks.sort(key=lambda s: risk_priority_order.index(s))
        return risks[0]


def get_learner_performance_data():
    df = get_card_progress_df()

    df["is_active"] = df.apply(user_is_active, axis=1)
    df = df[df["is_active"] == True]

    df["problem_solving_level"] = df.apply(get_problem_solving_level, axis=1)

    df["progress_based_risk_score"] = df.apply(
        calculate_progress_based_risk_score, axis=1
    )

    df["psf_risk"] = df.apply(get_psf_risk, axis=1)
    df["progress_risk"] = df.apply(get_progress_risk, axis=1)
    df["highest_priority_problem"] = df.apply(
        get_highest_priority_problem_to_address, axis=1
    )
    return df


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        df_performance = get_learner_performance_data()
        df_performance.to_csv("gitignore/learner_risk.csv")
