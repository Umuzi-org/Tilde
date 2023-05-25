from .utils import fetch_sheet, timestamp_to_datetime
from collections import namedtuple

AM_SHEET_NAME = "Good Morning (Responses)"
DAY_SHEET_NAME = "Good Afternoon (Responses)"
PM_SHEET_NAME = "End of Day  (Responses)"

COL_TIMESTAMP = "Timestamp"
COL_EMAIL = "Email Address"
COL_DATE = "date"


DATE_FORMAT = "%a %d %b %Y"


MORNING = "morning"
AFTERNOON = "afternoon"
EVENING = "evening"

SheetConfig = namedtuple("SheetConfig", "sheet get_score clean_sheet")


def _morning_score(row):
    if row[COL_TIMESTAMP].hour < 9:
        return 2
    return 1


def _afternoon_score(row):
    if 12 <= row[COL_TIMESTAMP].hour < 14:
        return 2
    return 1


def _evening_score(row):
    if row[COL_TIMESTAMP].hour == 16 and row[COL_TIMESTAMP].minute >= 30:
        return 2
    if row[COL_TIMESTAMP].hour > 16:
        return 2
    return 1


def _yes_no_to_bool_or_original(column_name):
    def inner(row):
        print(column_name)
        print(row)

        value = row[column_name]
        if type(value) is str:
            value = value.lower().strip()
        return {
            "yes": True,
            "yep": True,
            "no": False,
            "not yet": False,
            "none yet": False,
        }.get(value, value)

    return inner


def _get_problem_bool_from_columns(col1, col2):
    def inner(row):
        value1, value2 = row[col1], row[col2]
        if type(value1) is bool:
            return value1
        if type(value2) is bool:
            return value2
        return bool("".join(s for s in (value1, value2) if type(s) is str))

    return inner


def _get_problem_string_from_columns(col1, col2):
    def inner(row):
        values = row[col1], row[col2]
        return " ".join([s for s in values if type(s) is str])

    return inner


def _clean_morning(df):
    column_translations = {
        "What do you plan to get done today? What do you plan to start? What do you plan to FINISH/COMPLETE?".lower(): "plan_of_action",
        "Do you forsee any problems?".lower(): "problems_forseen_1",
        "If yes, how can we help?".lower(): "requests_1",
        "If you are late: Please state your reason".lower(): "late_reason",
    }

    df.columns = [column_translations.get(s.lower(), s) for s in df.columns]
    df["requests_1"] = df.apply(_yes_no_to_bool_or_original("requests_1"), axis=1)
    df["problems_forseen_1"] = df.apply(
        _yes_no_to_bool_or_original("problems_forseen_1"), axis=1
    )
    df["problems_forseen"] = df.apply(
        _get_problem_bool_from_columns("requests_1", "problems_forseen_1"), axis=1
    )
    df["requests"] = df.apply(
        _get_problem_string_from_columns("requests_1", "problems_forseen_1"), axis=1
    )
    return df


def _clean_afternoon(df):
    column_translations = {
        "Do you have any questions, requests or suggestions about the content you covered today?".lower(): "comments",
        "If you are late or early: Please state your reason".lower(): "late_reason",
        "Do you think you'll do everything that you said you would for the day?".lower(): "still_on_track_1",
        "If not, please tell us what you might not be able to do and why".lower(): "reason_for_not_on_track_1",
    }
    df.columns = [column_translations.get(s.lower(), s) for s in df.columns]
    df["still_on_track_1"] = df.apply(
        _yes_no_to_bool_or_original("still_on_track_1"), axis=1
    )
    df["reason_for_not_on_track_1"] = df.apply(
        _yes_no_to_bool_or_original("reason_for_not_on_track_1"), axis=1
    )

    df["still_on_track"] = df.apply(
        _get_problem_bool_from_columns("still_on_track_1", "reason_for_not_on_track_1"),
        axis=1,
    )
    df["reason_for_not_on_track"] = df.apply(
        _get_problem_string_from_columns(
            "still_on_track_1", "reason_for_not_on_track_1"
        ),
        axis=1,
    )

    return df


def plan_completed_sucessfully_mapper(row):
    value = row["plan_completed_sucessfully_1"]
    if type(value) is str:
        return "i completed everything" in value.lower()
    return value


def _clean_evening(df):
    column_translations = {
        "Did you do everything that you said you would do? Or is there anything else you missed?".lower(): "plan_completed_sucessfully_1",
        "Please justify the above answer. There is no reason to repeat what you said in the afternoon form".lower(): "reason_not_completed_1",
        "Do you have any questions, requests or suggestions about the content you covered today?".lower(): "comments",
        "If you are late or early: Please state your reason".lower(): "late_reason",
    }

    df.columns = [column_translations.get(s.lower(), s) for s in df.columns]
    df["plan_completed_sucessfully_1"] = df.apply(
        plan_completed_sucessfully_mapper, axis=1
    )
    df["reason_not_completed_1"] = df.apply(
        _yes_no_to_bool_or_original("reason_not_completed_1"), axis=1
    )
    df["plan_completed_sucessfully"] = df.apply(
        _get_problem_bool_from_columns(
            "plan_completed_sucessfully_1", "reason_not_completed_1"
        ),
        axis=1,
    )
    df["reason_not_completed"] = df.apply(
        _get_problem_string_from_columns(
            "plan_completed_sucessfully_1", "reason_not_completed_1"
        ),
        axis=1,
    )

    return df


SHEET_CONFIG = {
    MORNING: SheetConfig(AM_SHEET_NAME, _morning_score, _clean_morning),
    AFTERNOON: SheetConfig(DAY_SHEET_NAME, _afternoon_score, _clean_afternoon),
    EVENING: SheetConfig(PM_SHEET_NAME, _evening_score, _clean_evening),
}


def _common_cleaning(df, label):
    df[COL_TIMESTAMP] = df.apply(
        lambda row: timestamp_to_datetime(row[COL_TIMESTAMP]), axis=1
    )
    df = df.dropna(subset=[COL_TIMESTAMP])
    df.columns = [s.strip() for s in df.columns]

    df[COL_DATE] = df.apply(
        lambda row: row[COL_TIMESTAMP].strftime(DATE_FORMAT), axis=1
    )

    df = df.drop_duplicates(subset=[COL_EMAIL, COL_DATE], keep="last")

    df["score"] = df.apply(SHEET_CONFIG[label].get_score, axis=1)
    return df


def get_sheet_as_df(label):
    config = SHEET_CONFIG[label]
    df = fetch_sheet(config.sheet)
    df = _common_cleaning(df, label)
    df = config.clean_sheet(df)
    df = df.sort_values(by=[COL_TIMESTAMP], ascending=False)
    return df
