Deprecated

#     - [ ] from card date export => avg, median, max min time per card per flavour (don't count C25s)
#     - [ ] add time to each card in ordered card list. Format in minutes
#     - [ ] check which cards have been completed by Telkom recruits

from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd
import json
import math


def get_sheet(sheet_name):
    path = Path("gitignore") / sheet_name
    return pd.read_csv(path)


def get_time_spent_so_far_for_cohort():
    dfs = [
        get_sheet(s)
        for s in [
            "card_export_Cohort 25 data eng alumni_Wed 05 May 2021.csv",
            "card_export_Cohort 25 data eng_Wed 05 May 2021.csv",
            "card_export_Cohort 25 data sci_Wed 05 May 2021.csv",
            "card_export_Cohort 25 it support_Wed 05 May 2021.csv",
            "card_export_Cohort 25 java alumni_Wed 05 May 2021.csv",
            "card_export_Cohort 25 java_Wed 05 May 2021.csv",
            "card_export_Cohort 25 web dev 1_Wed 05 May 2021.csv",
            "card_export_Cohort 25 web dev 2_Wed 05 May 2021.csv",
            "card_export_Cohort 25 web dev alumni_Wed 05 May 2021.csv",
            "card_export_Cohort 25 web dev_Wed 05 May 2021.csv",
        ]
    ]


def calculate_card_duration(row):
    start_time = row["card.start_time"]
    complete_time = row["card.complete_time"]
    if pd.isnull(start_time) or pd.isnull(complete_time):
        return 0
    delta = complete_time - start_time
    return delta.seconds


def clean_flavour_names(key):
    def _clean_flavour_names(row):
        names = json.loads(row[key].replace("'", '"'))
        names.sort()
        return ", ".join(names)

    return _clean_flavour_names


def get_time_stats_per_card():
    dfs = [
        get_sheet(s)
        for s in [
            "card_export_Cohort 22 + 24 web dev_Thu 15 Apr 2021.csv",
            "card_export_Cohort 22 + 24 web dev_Wed 05 May 2021.csv",
            "card_export_Cohort 22 + 24 web dev_Wed 07 Apr 2021.csv",
            "card_export_Cohort 23 data sci_Wed 05 May 2021.csv",
            "card_export_Cohort 24 data eng Old Mutual_Wed 05 May 2021.csv",
            "card_export_Cohort 24 data eng_Tue 20 Apr 2021.csv",
            "card_export_Cohort 24 data eng_Wed 05 May 2021.csv",
            "card_export_Cohort 24 data sci_Tue 20 Apr 2021.csv",
            "card_export_Cohort 24 data sci_Wed 05 May 2021.csv",
            "card_export_Cohort 24 web dev_Wed 05 May 2021.csv",
            "card_export_Cohort 26 data sci_Wed 05 May 2021.csv",
            "card_export_Cohort 26 java_Wed 05 May 2021.csv",
            "card_export_Cohort 27 web dev_Wed 05 May 2021.csv",
            "card_export_Data Science Recruits_Wed 07 Apr 2021.csv",
        ]
    ]

    df = dfs[0]
    for partial_df in dfs[1:]:
        df = df.append(partial_df)

    df["card.complete_time"] = pd.to_datetime(
        df["card.complete_time"], infer_datetime_format=True
    )
    df["card.start_time"] = pd.to_datetime(
        df["card.start_time"], infer_datetime_format=True
    )
    df["duration"] = df.apply(calculate_card_duration, axis=1)
    df = df[df["duration"] != 0]

    df["card.flavour_names"] = df.apply(
        clean_flavour_names("card.flavour_names"), axis=1
    )

    grouped = df.groupby(
        ["card.flavour_names", "card.content_item.id", "card.content_item.title"],
        as_index=False,
    )

    data = {
        "flavours": pd.DataFrame(grouped)
        .reset_index()
        .apply(lambda row: row[0][0], axis=1),
        "card.content_item.id": pd.DataFrame(grouped)
        .reset_index()
        .apply(lambda row: row[0][1], axis=1),
        "title": pd.DataFrame(grouped)
        .reset_index()
        .apply(lambda row: row[0][2], axis=1),
        "mean": grouped["duration"].mean()["duration"],
        "max": grouped["duration"].max()["duration"],
        "min": grouped["duration"].min()["duration"],
        "median": grouped["duration"].median()["duration"],
        "std": grouped["duration"].std()["duration"],
        # "card.flavour_names": grouped["card.flavour_names"],
        # "card.content_item.id": grouped["card.content_item.id"],
        # "card.content_item.title": grouped["card.content_item.title"],
    }

    df = pd.concat(data, axis=1)

    df["mean_hours_total"] = df.apply(lambda row: row["mean"] / (60 * 60), axis=1)
    # df["max_hours"] = df.apply(lambda row: row["max"] / (60 * 60), axis=1)
    # df["min_hours"] = df.apply(lambda row: row["min"] / (60 * 60), axis=1)
    # df["median_hours"] = df.apply(lambda row: row["median"] / (60 * 60), axis=1)
    # df["std_hours"] = df.apply(lambda row: row["std"] / (60 * 60), axis=1)
    df["mean_work_days"] = df.apply(
        lambda row: row["mean"] / (60 * 60 * 8),
        axis=1,
    )
    # df["max_days"] = df.apply(lambda row: row["max"] / (60 * 60 * 24), axis=1)
    # df["min_days"] = df.apply(lambda row: row["min"] / (60 * 60 * 24), axis=1)
    # df["median_days"] = df.apply(
    #     lambda row: row["median"] / (60 * 60 * 24), axis=1
    # )
    # df["std_days"] = df.apply(lambda row: row["std"] / (60 * 60 * 24), axis=1)

    df = df.sort_values("mean")
    df.to_csv("gitignore/temp.csv")

    return df


def get_curriculum_cards():
    dfs = [
        (s, get_sheet(s))
        for s in [
            "data eng alumni_curriculums.csv",
            "data eng_curriculums.csv",
            "data sci_curriculums.csv",
            "java alumni_curriculums.csv",
            "java_curriculums.csv",
            "web dev alumni_curriculums.csv",
            "web dev_curriculums.csv",
        ]
    ]
    for _, df in dfs:
        df["flavours"] = df.apply(clean_flavour_names("flavours"), axis=1)
    return dfs


class Command(BaseCommand):
    def handle(self, *args, **options):
        time_stats_df = get_time_stats_per_card()
        curriculum_dfs = get_curriculum_cards()
        for file_name, df in curriculum_dfs:
            df = df.merge(time_stats_df, on=["flavours", "title"], how="left")
            df = df.merge(
                time_stats_df,
                on=["title"],
                how="left",
                suffixes=("", "_flavourmismatch"),
            )

            df["final_mean_work_days"] = df.apply(
                lambda row: row["mean_work_days"]
                or row["mean_work_days_flavourmismatch"],
                axis=1,
            )
            df["final_mean_hours_total"] = df.apply(
                lambda row: row["mean_hours_total"]
                or row["mean_hours_total_flavourmismatch"],
                axis=1,
            )

            df = df[
                [
                    "course name",
                    "title",
                    "flavours",
                    "tags",
                    "url",
                    "final_mean_work_days",
                    "final_mean_hours_total",
                    # "max",
                    # "min",
                    # "median",
                    # "std",
                ]
                # + [s for s in df.columns if s.startswith("mean")]
            ]

            df = df.drop_duplicates(subset=["url"], keep="last")

            df.to_csv(Path("gitignore") / f"durations_{file_name}", index=False)
